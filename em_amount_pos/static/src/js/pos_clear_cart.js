odoo.define('pos_margin.ClearCart', function(require) {
    'use strict';
       const PosComponent = require('point_of_sale.PosComponent');
       const ProductScreen = require('point_of_sale.ProductScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       
       class ClearCart extends PosComponent {
           constructor() {
               super(...arguments);
               useListener('click', this.onClick);
                document.body.removeEventListener('keyup',this.hotkey_handler);
                this.hotkey_handler = function(event){
                    if(!$($(document).find("div.payment-screen.screen")[0]).hasClass('oe_hidden')){
                        if (event.which === 127) {
                            $($(document).find("div.control-button")[1]).trigger("click");
                        }
                    } 
                };
                document.body.addEventListener('keyup', this.hotkey_handler);
           }
           onClick() {
                var self = this;
                this.clear_button_fun();

           }


           
           clear_button_fun(){
                var self = this;
                var order = this.env.pos.get_order();
                while(order.get_selected_orderline()) {
                    order.remove_orderline(order.get_selected_orderline())
                }
                

                //self.rpc({
                //}).then(function (data) {
                //var res = rpc.query({
               /*
                self.rpc({
                    model: 'pos.order',
                    method: 'search_ncf',
                    args: [????]
                }).then(async function(ncf) {
                    console.log(ncf); });
                };

                */


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
