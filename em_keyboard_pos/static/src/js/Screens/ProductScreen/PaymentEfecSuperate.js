odoo.define('pos_margin.PaymenEfecSuperate', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const NumberBuffer = require('point_of_sale.NumberBuffer');

    const { parse } = require('web.field_utils');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const { onChangeOrder } = require('point_of_sale.custom_hooks');


    class PaymenEfecSuperate extends PosComponent {
           constructor() {
                super(...arguments);
                useListener('click', this.onClickEfectivo);

                NumberBuffer.use({
                    triggerAtInput: 'update-selected-paymentline',
                });
                
                this.payment_methods_from_config = this.env.pos.payment_methods.filter(method => this.env.pos.config.payment_method_ids.includes(method.id));
                this.selectClients = this.env.pos.db.get_partner_by_id(this.env.pos.config.default_partner_id[0]);
                

                onChangeOrder(this._onPrevOrder, this._onNewOrder);
                useErrorHandlers();
                this.payment_interface = null;
                this.error = false;
           }
           
           onClickEfectivo() {
              try{
                this.currentOrder.set_client(this.selectClients);
                this.currentOrder.add_paymentline(this.payment_methods_from_config[2]);
                //console.log($($(document).find("sefectivo")), "superate", $($(document).find("valor")))
                //$($(document).find("valor")).removeClass('hiddenSuperate')
                //$($(document).find("valor")).removeAttr("type")
                //$($(document).find("#rowProduct.rowsProduct")).prev().removeClass('rowsProduct')
                //$($(document).find("valor")).type
                //$($(document).find("sefectivo")).data("1650")

                //this.currentOrder.set_client(this.selectClients);
                //this.currentOrder.add_paymentline(this.payment_methods_from_config[2]);
                //this.validateOrder(false)
              }catch(error){
                console.log("error",error)
                console.log("control de errror pendiente de resorver / al 03 de julio 2022")
              }
              
           }



           




           get currentOrder() {
                return this.env.pos.get_order();
            }
            
            






    }



   PaymenEfecSuperate.template = 'PaymenEfecSuperate';
   ProductScreen.addControlButton({
       component: PaymenEfecSuperate,
       condition: function() {
           return this.env.pos;
       },
   });
    

    Registries.Component.add(PaymenEfecSuperate);

    return PaymenEfecSuperate;
});