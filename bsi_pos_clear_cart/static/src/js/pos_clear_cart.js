odoo.define('bsi_pos_clear_cart.ClearCart', function(require) {
    'use strict';
       const PosComponent = require('point_of_sale.PosComponent');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       var models = require("point_of_sale.models");



       

      
       class ClearCart extends PosComponent {
           constructor() {
               super(...arguments);
               useListener('click', this.onClick);
               this.state = {
                 query: null,
               };
           }

           get clients() {
               let res;
               if (this.state.query && this.state.query.trim() !== '') {
                   res = this.env.pos.db.search_partner(this.state.query.trim());
               } else {
                   res = this.env.pos.db.get_partners_sorted(1000);
               }
            return res.sort(function (a, b) { return (a.name || '').localeCompare(b.name || '') });
           }


           get clien() {
               
            return this.env.pos.get_client();
           }




           onClick() {
                var self = this;
                this.clear_button_fun();
           }
           clear_button_fun(){
                //const client = this.env.pos.get_client();
                var order = this.env.pos.get_order();
                while(order.get_selected_orderline()) {
                    order.remove_orderline(order.get_selected_orderline())
                }
                console.log(this.clients)
                console.log(this.clients[0].property_product_pricelist)
                console.log(this.clients[0].property_account_position_id)  
            }
            
       }
       ClearCart.template = 'ClearCart';
       ProductScreen.addControlButton({
           component: ClearCart,
           condition: function() {
               return this.env.pos;
           },
       });
       Registries.Component.add(ClearCart);
       return ClearCart;
    });
