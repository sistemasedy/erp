# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2020-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Irfan (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
import pytz
from odoo import models, fields, api
from datetime import timedelta, datetime, date


class PosDashboard(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_department(self, option):
        company_id = self.env.company.id
        if option == 'pos_hourly_sales':

            user_tz = self.env.user.tz if self.env.user.tz else pytz.UTC
            query = '''select  EXTRACT(hour FROM date_order at time zone 'utc' at time zone '{}') 
                       as date_month,sum(amount_total) from pos_order where  
                       EXTRACT(month FROM date_order::date) = EXTRACT(month FROM CURRENT_DATE) 
                       AND pos_order.company_id = ''' + str(
                       company_id) + ''' group by date_month '''
            query = query.format(user_tz)
            label = 'HOURS'
        elif option == 'pos_monthly_sales':
            query = '''select  date_order::date as date_month,sum(amount_total) from pos_order where 
             EXTRACT(month FROM date_order::date) = EXTRACT(month FROM CURRENT_DATE) AND pos_order.company_id = ''' + str(
                company_id) + '''  group by date_month '''
            label = 'DAYS'
        else:
            query = '''select TO_CHAR(date_order,'MON')date_month,sum(amount_total) from pos_order where
             EXTRACT(year FROM date_order::date) = EXTRACT(year FROM CURRENT_DATE) AND pos_order.company_id = ''' + str(
                company_id) + ''' group by date_month'''
            label = 'MONTHS'

        self._cr.execute(query)
        docs = self._cr.dictfetchall()
        order = []
        for record in docs:
            order.append(record.get('sum'))
        today = []
        for record in docs:
            today.append(record.get('date_month'))
        final = [order, today, label]
        return final

    @api.model
    def get_details(self):
        company_id = self.env.company.id
        cr = self._cr

        cr.execute(
            """SELECT pos_payment_method.name, SUM(amount) 
            FROM pos_payment 
            INNER JOIN pos_payment_method ON pos_payment_method.id = pos_payment.payment_method_id 
            GROUP BY pos_payment_method.name 
            ORDER BY SUM(amount) DESC;"""
        )
        payment_details = cr.fetchall()

        cr.execute(
            """SELECT hr_employee.name, SUM(pos_order.amount_paid) AS total, COUNT(pos_order.amount_paid) AS orders 
            FROM pos_order 
            INNER JOIN hr_employee ON pos_order.user_id = hr_employee.user_id 
            WHERE pos_order.company_id = %s 
            GROUP BY hr_employee.name 
            ORDER BY total DESC;""",
            (company_id,)
        )
        salesperson = cr.fetchall()

        total_sales = []
        for rec in salesperson:
            rec = list(rec)
            sym_id = rec[1]
            company = self.env.company
            if company.currency_id.position == 'after':
                rec[1] = "%s %s" % (sym_id, company.currency_id.symbol)
            else:
                rec[1] = "%s %s" % (company.currency_id.symbol, sym_id)
            rec = tuple(rec)
            total_sales.append(rec)

        cr.execute(
            """SELECT DISTINCT(product_template.name) AS product_name, SUM(qty) AS total_quantity 
            FROM pos_order_line 
            INNER JOIN product_product ON product_product.id = pos_order_line.product_id 
            INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id  
            WHERE pos_order_line.company_id = %s 
            GROUP BY product_template.id 
            ORDER BY total_quantity DESC 
            LIMIT 10;""",
            (company_id,)
        )
        selling_product = cr.fetchall()

        sessions = self.env['pos.config'].search([])
        sessions_list = []
        dict = {
            'closing_control': 'Closed',
            'opened': 'Opened',
            'new_session': 'New Session',
            'opening_control': "Opening Control"
        }
        for session in sessions:
            sessions_list.append({
                'session': session.name,
                'status': dict.get(session.pos_session_state)
            })

        payments = []
        for rec in payment_details:
            rec = list(rec)
            sym_id = rec[1]
            company = self.env.company
            if company.currency_id.position == 'after':
                rec[1] = "%s %s" % (sym_id, company.currency_id.symbol)
            else:
                rec[1] = "%s %s" % (company.currency_id.symbol, sym_id)
            rec = tuple(rec)
            payments.append(rec)

        return {
            'payment_details': payments,
            'salesperson': total_sales,
            'selling_product': sessions_list,
        }

    


    @api.model
    def _get_reorder_quantity(self, product, start_date, end_date):
        stock_moves = self.env['stock.move'].search([
            ('product_id', '=', product.id),
            ('location_id.usage', '=', 'internal'),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('reference', 'ilike', 'WH/POS/%')
        ])
        return abs(sum(stock_moves.mapped('product_qty')))

 
    @api.model
    def get_refund_details(self, start_date=None, end_date=None):

        if not start_date:
            start_date = datetime.today().date() - timedelta(days=30)
        if not end_date:
            end_date = datetime.today().date()

        pos_order = self.env['pos.order'].search([
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date)
        ])

        venta = 0
        total_cost_with_standard_price = 0
        total_cost_with_assigned_price = 0
        total_profit = 0

        for rec in pos_order:
            venta += rec.amount_total
            
            for line in rec.lines:
                if line.product_id.standard_price > 0:
                    # Grupo 1: Productos con standard_price mayor que 0
                    total_cost_with_standard_price += line.product_id.standard_price * line.qty
                else:
                    # Grupo 2: Productos con standard_price igual a 0
                    assigned_cost = line.price_unit - (line.price_unit * 0.20)  # 20% del precio de venta
                    total_cost_with_assigned_price += assigned_cost * line.qty

        # Calcular el costo total sumando ambos grupos
        total_cost = total_cost_with_standard_price + total_cost_with_assigned_price

        # Calcular la ganancia total
        total_profit = venta - total_cost

        # La lógica existente que ya tenías

        default_date = datetime.today().date()
        pos_order = self.env['pos.order'].search([])
        orders_today = self.env['pos.order'].search([('date_order', '=', default_date)])
        pos_order_line = self.env['pos.order.line'].search([])
        total = 0
        today_refund_total = 0
        total_order_count = 0
        total_refund_count = 0
        today_sale = 0
        total_today = 0

        today_sale_amount = 0
        today_sale_product = 0
        a = 0

        

        for rec in pos_order:
            if rec.amount_total < 0.0 and rec.date_order.date() == default_date:
                today_refund_total = today_refund_total + 1
                total_sales_today = rec.amount_total
                total_today = total_today + total_sales_today
            total_order_count = total_order_count + 1
            if rec.date_order.date() == default_date:
                today_sale = today_sale + 1

            if rec.amount_total < 0.0:
                total_refund_count = total_refund_count + 1
            total_sales = rec.amount_total
            total = total + total_sales


        magnitudes = 0
        magnitude = 0
        while abs(total_today) >= 1000:
            magnitudes += 1
            total_today /= 1000.0

        while abs(total) >= 1000:
            magnitude += 1
            total /= 1000.0

        magnitude1 = 0
        while abs(venta) >= 1000:
            magnitude1 += 1
            venta /= 1000.0
        magnitude2 = 0
        while abs(total_cost) >= 1000:
            magnitude2 += 1
            total_cost /= 1000.0
        magnitude3 = 0
        while abs(total_profit) >= 1000:
            magnitude3 += 1
            total_profit /= 1000.0

        # add more suffixes if you need them

        val1 = '%.2f%s' % (venta, ['', 'K', 'M', 'G', 'T', 'P'][magnitude1])
        val2 = '%.2f%s' % (total_cost, ['', 'K', 'M', 'G', 'T', 'P'][magnitude2])
        val3 = '%.2f%s' % (total_profit, ['', 'K', 'M', 'G', 'T', 'P'][magnitude3])


        val = '%.2f%s' % (total, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])
        val5 = '%.2f%s' % (total_today, ['', 'K', 'M', 'G', 'T', 'P'][magnitudes])
        pos_session = self.env['pos.session'].search([])
        total_session = 0
        for record in pos_session:
            total_session = total_session + 1
        return {
            'total_sale_today': val5,
            'total_order_count': total_order_count,
            'total_refund_count': total_refund_count,
            'total_session': total_session,
            'today_refund_total': today_refund_total,
            'today_sale': today_sale,
            'venta': val1,
            'total_cost': val2,
            'total_profit': val3,
            'fecha': start_date,
            'fecha2': default_date,
        }


    @api.model
    def retrieve_out_invoice_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the invoice order views.
            :return: dictionary with the required values"""
        result = {
            'draft': 0,
            'posted': 0,
            'cancelled': 0,
            'paid': 0,
            'not_paid_amount': 0,
            'paid_amount': 0,
            'lost_amount': 0,
            'expected_amount': 0,
            'company_currency_symbol': self.env.company.currency_id.symbol
        }

        default_date = datetime.today().date()
        pos_order = self.env['pos.order'].search([])
        orders_today = self.env['pos.order'].search([('date_order', '=', default_date)])
        sum_amount = 0
        for line in pos_order:
            sum_amount = sum_amount + line.amount_total
        
        result['paid_amount'] = sum_amount
        #result['draft'] = account_move.search_count([('state', '=', 'draft'), ('move_type', '=', 'out_invoice')])
        return result




    @api.model
    def get_the_top_customer(self, ):
        company_id = self.env.company.id
        query = '''select res_partner.name as customer,pos_order.partner_id,sum(pos_order.amount_paid) as amount_total from pos_order 
        inner join res_partner on res_partner.id = pos_order.partner_id where pos_order.company_id = ''' + str(
            company_id) + ''' GROUP BY pos_order.partner_id,
        res_partner.name  ORDER BY amount_total  DESC LIMIT 10;'''
        self._cr.execute(query)
        docs = self._cr.dictfetchall()
        print(docs)

        order = []
        for record in docs:
            order.append(record.get('amount_total'))
        day = []
        for record in docs:
            day.append(record.get('customer'))
        final = [order, day]
        return final

    @api.model
    def get_the_top_products(self):
        company_id = self.env.company.id

        query = '''
        SELECT DISTINCT(product_template.name) AS product_name, SUM(qty) AS total_quantity
        FROM pos_order_line
        INNER JOIN product_product ON product_product.id = pos_order_line.product_id
        INNER JOIN product_template ON product_product.product_tmpl_id = product_template.id
        WHERE pos_order_line.company_id = %s AND product_product.default_code != '254466'
        GROUP BY product_template.id
        ORDER BY total_quantity DESC
        LIMIT 10;
        '''

        self._cr.execute(query, (company_id,))
        top_product = self._cr.dictfetchall()

        total_quantity = [record.get('total_quantity') for record in top_product]
        product_name = [record.get('product_name') for record in top_product]
        final = [total_quantity, product_name]

        return final


    @api.model
    def get_the_top_products_archivada(self):
        company_id = self.env.company.id

        query = '''select DISTINCT(product_template.name) as product_name,sum(qty) as total_quantity from 
       pos_order_line inner join product_product on product_product.id=pos_order_line.product_id inner join 
       product_template on product_product.product_tmpl_id = product_template.id where pos_order_line.company_id = ''' + str(
            company_id) + ''' group by product_template.id ORDER 
       BY total_quantity DESC Limit 10 '''

        self._cr.execute(query)
        top_product = self._cr.dictfetchall()

        total_quantity = []
        for record in top_product:
            # if record.get('total_quantity') != 0:
            #     print(total_quantity.append(record.get('total_quantity')))
            total_quantity.append(record.get('total_quantity'))
        product_name = []
        for record in top_product:
            product_name.append(record.get('product_name'))
        final = [total_quantity, product_name]
        return final

    @api.model
    def get_the_top_categories(self):
        company_id = self.env.company.id
        query = '''select DISTINCT(product_category.complete_name) as product_category,sum(qty) as total_quantity 
        from pos_order_line inner join product_product on product_product.id=pos_order_line.product_id  inner join 
        product_template on product_product.product_tmpl_id = product_template.id inner join product_category on 
        product_category.id =product_template.categ_id where pos_order_line.company_id = ''' + str(
            company_id) + ''' group by product_category ORDER BY total_quantity DESC '''
        self._cr.execute(query)
        top_product = self._cr.dictfetchall()
        total_quantity = []
        for record in top_product:
            total_quantity.append(record.get('total_quantity'))
        product_categ = []
        for record in top_product:
            product_categ.append(record.get('product_category'))
        final = [total_quantity, product_categ]
        return final
