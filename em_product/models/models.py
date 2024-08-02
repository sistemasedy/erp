# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp

from odoo.tools import float_compare, pycompat

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    
    _inherit = 'res.partner'

    vat = fields.Char(string='RNC ', index=True, help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    #otros_dias = fields.Char(string='Otros Dias', index=True)




class ProductTemplate(models.Model):
    _inherit = "product.template"

    grupo = fields.Char(string='Grupo')
    localization = fields.Char(string='Localizacion')
    category_em = fields.Char(string='Categoria')
    medida = fields.Char(string='Medida')
    codigo = fields.Char(string='Codigo')
    numero_parte = fields.Char(string='Numero de Parte')
    numero = fields.Char(string='Numero')
    margen = fields.Char(string='Margen-%', digits=(2, 2))
    margen_valor = fields.Char(string='Margen Valor', digits=(2, 2), compute='compute_margin', store=True)
    calcular_venta = fields.Boolean(string='Recalcular', default=False)
    calcular_costo = fields.Boolean(string='Calcular el margen', default=False)
    #calcular_margen = fields.Boolean(string='Calcular el Margen' ,default=False)
    available_in_pos = fields.Boolean(string='Available in POS', help='Check if you want this product to appear in the Point of Sale.', default=True)

    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits=dp.get_precision('Product Price'),
        help="Price at which the product is sold to customers.")

    #standard_price = fields.Float(
     #   'Cost', compute='_compute_standard_price_costo', store=True,
      #  digits=dp.get_precision('Product Price'), groups="base.group_user",
       # help = "Cost used for stock valuation in standard price and as a first price to set in average/FIFO.")
    @api.depends('list_price', 'standard_price', 'calcular_venta', 'margen')
    def compute_margin(self):
        """Method to compute the margin of the product."""
        #self.margen = 0
        for record in self:
            if record.list_price and record.standard_price:
                record.margen_valor = (record.list_price - record.standard_price)

    @api.depends('list_price', 'standard_price', 'calcular_venta')
    def compute_porcent(self):
        """Method to compute the margin of the product."""
        self.margen = 0
        for record in self:
            if record.list_price and record.standard_price:
                record.margen = (record.list_price - record.standard_price) / record.list_price * 100





    @api.depends('product_variant_ids', 'product_variant_ids.standard_price','list_price','margen')
    def _compute_standard_price_costo(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = 0.0
            #if self.calcular_costo:
        #self.standard_price = self.list_price *(1-self.margen/100)

    #@api.onchange('standard_price','margen')
    #def _compute_costo(self):
        #lista = list(self.rango_valores_reales(0.0, 100.0, 0.1))
        #if self.calcular_venta:
        #self.list_price = self.standard_price /(1-self.margen/100)



class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=5):
        if not args:
            args = []
        if name:
            args += [('name', operator, name)]
        products = self.search(args, limit=limit)
        return products.name_get()



