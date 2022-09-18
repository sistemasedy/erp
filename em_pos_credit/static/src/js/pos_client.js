odoo.define('em_pos_credit.PosClient', function(require) {
    'use strict';
       const PosComponent = require('point_of_sale.PosComponent');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       const models = require("point_of_sale.models");

       models.load_fields("res.partner", ["credit", "credit_limit", "due_amount", "l10n_do_dgii_tax_payer_type"]);



      
       
    });
