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

    vat = fields.Char(string='RNC ', index=True,
                      help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    grupo = fields.Char(string='Lote')
    localization = fields.Char(string='Localizacion')
    category_em = fields.Char(string='Categoria')
    medida = fields.Char(string='Medida')
    codigo = fields.Char(string='Codigo')
    numero_parte = fields.Char(string='Numero de Parte')
    numero = fields.Char(string='Numero')
    margen = fields.Float(string='Margen (%)', digits=(
        16, 2), compute='compute_margin', store=True)
    margen_valor = fields.Float(string='Margen Valor', digits=(
        16, 2), compute='compute_margin', store=True)
    calcular_venta = fields.Boolean(string='Recalcular', default=False)
    calcular_costo = fields.Boolean(string='Calcular el margen', default=False)
    # calcular_margen = fields.Boolean(string='Calcular el Margen' ,default=False)
    available_in_pos = fields.Boolean(
        string='Available in POS', help='Check if you want this product to appear in the Point of Sale.', default=True)

    calcular_venta_anterior = fields.Boolean(
        string='Precio Anterior', default=False)
    precio_venta_anterior = fields.Float(
        'Sales Price', default=1.0,
        digits=dp.get_precision('Product Price'),
        help="Price at which the product is sold to customers.")


    

    # Campo de selección para elegir el modo de cálculo
    calculation_mode = fields.Selection(
        [
            ('none', 'No Calcular'),
            ('price_to_margin', 'Calcular Margen desde Precio'),
            ('margin_to_price', 'Calcular Precio desde Margen')
        ],
        string="Modo de Cálculo",
        default='none',
        help="Define cómo se relacionan el precio de venta, el costo y el margen.\n"
             "- No Calcular: Comportamiento por defecto.\n"
             "- Calcular Margen desde Precio: Muestra el margen basado en el precio de venta y el costo.\n"
             "- Calcular Precio desde Margen: Calcula el precio de venta basado en el costo y un margen fijo."
    )

    # Campo para que el usuario ingrese el margen deseado para el cálculo del precio
    fixed_margin = fields.Float(
        string='Margen Fijo (%)',
        default=0.33,
        help="Introduzca el margen de beneficio deseado para calcular el precio de venta."
    )

    # Campo de margen calculado (funcionalidad original)
    product_margin = fields.Float(
        string='Margen de Producto (%)',
        compute='_compute_product_margin',
        store=True,
        help="Muestra el margen de beneficio basado en el Precio de Venta y el Costo."
    )



    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits=dp.get_precision('Product Price'),
        help="Price at which the product is sold to customers.")
    fecha_de_vencimiento = fields.Date(string='Fecha de Vencimiento')

    empaque = fields.Selection([
        ('caja', 'Caja'),
        ('saco', 'Saco'),
        ('paquete', 'Paquete'),
    ], string="Tipo de Empaque", help="Tipo de empaque del producto.")
    cantidad_por_empaque = fields.Char(
        string="Cantidad por Empaque", help="Ejemplo: 24/1")

    # standard_price = fields.Float(
    #   'Cost', compute='_compute_standard_price_costo', store=True,
    #  digits=dp.get_precision('Product Price'), groups="base.group_user",
    # help = "Cost used for stock valuation in standard price and as a first price to set in average/FIFO.")
    @ api.depends('list_price', 'standard_price', 'calcular_venta', 'margen')
    def compute_margin(self):
        """Method to compute the margin of the product."""
        for record in self:
            if record.standard_price > 0:
                if record.list_price > 1:
                    # Calcular los valores numéricos sin formato
                    record.margen_valor = record.list_price - record.standard_price
                    record.margen = (
                        (record.list_price - record.standard_price) / record.standard_price) * 100
                elif record.list_price == 1:
                    record.margen_valor = 0.0
                    record.margen = 0.0
            elif record.standard_price == 0:
                if record.list_price > 1:
                    record.margen_valor = record.list_price * 0.20
                    record.margen = 20.0
                elif record.list_price == 1:
                    record.margen_valor = 0.0
                    record.margen = 0.0

    @ api.depends('list_price', 'standard_price', 'calcular_venta')
    def compute_porcent(self):
        """Method to compute the margin of the product."""
        self.margen = 0
        for record in self:
            if record.list_price and record.standard_price:
                record.margen = (
                    record.list_price - record.standard_price) / record.list_price * 100

    @ api.depends('product_variant_ids', 'product_variant_ids.standard_price', 'list_price', 'margen')
    def _compute_standard_price_costo(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.standard_price = template.product_variant_ids.standard_price
        for template in (self - unique_variants):
            template.standard_price = 0.0
            # if self.calcular_costo:
        # self.standard_price = self.list_price *(1-self.margen/100)

    
    
    @api.depends('list_price', 'standard_price', 'calculation_mode')
    def _compute_product_margin(self):
        """
        Calcula el margen porcentual para cada producto.
        Este cálculo solo se activa si el modo es 'Calcular Margen desde Precio'.
        """
        for product in self:
            # Solo calcular si el modo es el correcto y el precio de venta no es cero
            if product.calculation_mode == 'price_to_margin' and product.list_price > 0:
                margin = ((product.list_price - product.standard_price) / product.list_price) * 100
                product.product_margin = margin
            else:
                # En cualquier otro caso, el margen calculado es 0
                product.product_margin = 0.0

    @api.onchange('calculation_mode', 'fixed_margin', 'standard_price')
    def _onchange_calculate_price_from_margin(self):
        """
        Calcula y actualiza el Precio de Venta en el formulario cuando cambia el modo,
        el margen fijo o el costo. Se activa solo si el modo es 'Calcular Precio desde Margen'.
        """
        if self.calculation_mode == 'margin_to_price':
            if self.fixed_margin >= 100 or self.fixed_margin < 0:
                # Si el margen es inválido, se podría mostrar una advertencia al usuario.
                # Por ahora, simplemente no se calcula un nuevo precio.
                return {
                     'warning': {
                         'title': "Advertencia de Margen",
                         'message': "El margen debe ser un valor entre 0 y 99.99%.",
                     }
                 }

            if self.standard_price > 0:
                # Fórmula: Precio de Venta = Costo / (1 - (Margen / 100))
                self.list_price = self.standard_price * (1 + (self.fixed_margin))
            else:
                self.list_price = 0.0
    
    
    
    # @api.onchange('standard_price','margen')
    # def _compute_costo(self):
        # lista = list(self.rango_valores_reales(0.0, 100.0, 0.1))
        # if self.calcular_venta:
        # self.list_price = self.standard_price /(1-self.margen/100)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @ api.model
    def name_search(self, name, args=None, operator='ilike', limit=5):
        if not args:
            args = []
        if name:
            args += [('name', operator, name)]
        products = self.search(args, limit=limit)
        return products.name_get()
