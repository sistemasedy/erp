odoo.define('em_pos_credit.PosClient', function(require) {
    'use strict';
       const PosComponent = require('point_of_sale.PosComponent');
       const PaymentScreen = require('point_of_sale.PaymentScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       const models = require("point_of_sale.models");

       const { parse } = require('web.field_utils');
	   
	   const { useErrorHandlers, useAsyncLockedMethod } = require('point_of_sale.custom_hooks');
	   const NumberBuffer = require('point_of_sale.NumberBuffer');
	    
	    
	   const { onChangeOrder } = require('point_of_sale.custom_hooks');
	   const { isConnectionError } = require('point_of_sale.utils');



       models.load_fields("res.partner", ["credit", "credit_limit", "due_amount"]);
       //models.load_fields("res.partner", ["credit", "credit_limit", "due_amount", "l10n_do_dgii_tax_payer_type"]);


       const PosClient = PaymentScreen =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
               
                
            }


           



	        addNewPaymentLine({ detail: paymentMethod }) {
	            // original function: click_paymentmethods
	            let result = this.currentOrder.add_paymentline(paymentMethod);
	            if (result){
	                NumberBuffer.reset();
	                return true;
	            }
	            else{
	                this.showPopup('ErrorPopup', {
	                    title: this.env._t('Error'),
	                    body: this.env._t('There is already an electronic payment in progress.'),
	                });
	                return false;
	            }

	            console.log("test", currentClient)
	        }



         
        }
    Registries.Component.extend(PaymentScreen, PosClient);
    return PosClient;



      
       
});
