odoo.define('pos_magnify_image.PaymenScreenPos', function (require) {
    "use strict";
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    var core = require('web.core');

    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { onChangeOrder } = require('point_of_sale.custom_hooks');


    var _t = core._t;

    const PaymenScreenPos = PaymentScreen =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);

                document.body.removeEventListener('keyup',this.hotkey_handler_pay);
                
                this.hotkey_handler_pay = function(event){

                    if(!$($(document).find("div.product-screen.screen")[0]).hasClass('oe_hidden')){
                      
                        if (event.which === 113) {
                            //$($(document).find("button.button.pay")).trigger("click");
                            //$($(document).find("#direct")).trigger("click");
                        }
                      
                    }
                    
                    
                };
                document.body.addEventListener('keyup', this.hotkey_handler_pay);
              
            }

       

            
            

         
        }
    Registries.Component.extend(PaymentScreen, PaymenScreenPos);
    return PaymenScreenPos;
});