odoo.define('pos_margin.PaymentInput', function(require) {
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


    class PaymentInput extends PosComponent {
           constructor() {
                super(...arguments);
                //useListener('click', this.onClickEfectivo);

                NumberBuffer.use({
                    triggerAtInput: 'update-selected-paymentline',
                });
                onChangeOrder(this._onPrevOrder, this._onNewOrder);
                useErrorHandlers();
                this.payment_interface = null;
                this.error = false;
           }
           
          


    


    }



   PaymentInput.template = 'PaymentInput';
   ProductScreen.addControlButton({
       component: PaymentInput,
       condition: function() {
           return this.env.pos //&& this.env.pos.config.module_pos_discount;
       },
   });
    

    Registries.Component.add(PaymentInput);

    return PaymentInput;
});