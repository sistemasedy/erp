odoo.define('pos_margin.ProductSearch', function(require) {
    'use strict';

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const Ajax = require('web.ajax');

    const data_json = []


    class ProductSearch extends PosComponent {
           constructor() {
               super(...arguments);
               //useListener('click', this.onClickDir);

           }

           

           get searchWord() {
                return this.state.searchWord.trim();
            }

           get currentOrder() {
                return this.env.pos.get_order();
            }

           onClickDir() {
                console.log("file")
                //$($(document).find("div.search-box input")).focus()
            }


           
       }

   ProductSearch.template = 'ProductSearch';
   ProductScreen.addControlButton({
       component: ProductSearch,
       condition: function() {
           return this.env.pos;
       },
   });
    

    Registries.Component.add(ProductSearch);

    return ProductSearch;
});

