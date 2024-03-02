odoo.define('pos_margin.ProductScreens', function (require) {
    "use strict";


    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    var core = require('web.core');
    var _t = core._t;
    const balance = []

    const ProductScreens = ProductScreen =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
               
                document.body.removeEventListener('keyup',this.hotkey_handler);
                
                this.hotkey_handler = function(event){

                    if(!$($(document).find("div.payment-screen.screen")[0]).hasClass('oe_hidden')){
                        if (event.which === 27) {
                            $($(document).find("#searchProducts")).trigger("click");  
                        }
                        
                        
                        if (event.which === 113) {
                            //$($(document).find("button.button.pay")).trigger("click");
                            $($(document).find("#direct")).trigger("click");
                        }

                        if (event.which === 119) {
                            //$($(document).find("button.button.pay")).trigger("click");
                            $($(document).find("#superate")).trigger("click");
                        }

                        if (event.which === 120) {                            
                            $($(document).find("button.button.pay")[0]).trigger("click");
                            $($(document).find("div.button.next")[0]).trigger("click");
                            $($(document).find("div.button.next.highlight")[0]).trigger("click");
                            //$($(document).find("#sefectivo")).trigger("click");
                            console.log("bus", NumberBuffer.getFloat()) 

                        }


                        if (event.which === 115) {
                            $($(document).find("button.button.pay")[0]).trigger("click");
                            $($(document).find("div.button.next")[0]).trigger("click");
                            $($(document).find("div.button.next.highlight")[0]).trigger("click");
                            console.log("bus", NumberBuffer.getFloat()) 
                        }
                    } 
                };
                document.body.addEventListener('keyup', this.hotkey_handler);
                //document.body.addEventListener('onload', this.changePad);
                this.payment_methods_from_config = this.env.pos.payment_methods.filter(method => this.env.pos.config.payment_method_ids.includes(method.id));
                
                
            }



          
            

         
        }
    Registries.Component.extend(ProductScreen, ProductScreens);
    return ProductScreens;
});