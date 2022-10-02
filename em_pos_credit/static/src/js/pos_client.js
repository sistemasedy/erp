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



       models.load_fields("res.partner", ["credit", "credit_limit", "due_amount", "blocking_stage", "active_limit"]);
       //models.load_fields("res.partner", ["credit", "credit_limit", "due_amount", "l10n_do_dgii_tax_payer_type"]);


       const PosClient = PaymentScreen =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
               
                
            }

	        async validateOrder(isForceValidate) {
	        	var method = 0
	        	const order = this.currentOrder;
	        	const currentClient = this.currentOrder.get_client();
	        	for (var i = 0; i < order.paymentlines.length; i++) {
	        		if (order.paymentlines.models[i].name == "Cuenta de cliente") {
	        			method = order.paymentlines.models[i].amount
	        		}
	        	}
	            if (method > 0 && currentClient.active_limit) {

	            	if (currentClient.due_amount + method > currentClient.blocking_stage) {
		            	this.showPopup('ErrorPopup', {
				            title: this.env._t('Control de Cuenta de Clientes'),
				            body: this.env._t("El Monto Excede el limite de Credito."),
				        });
				        return;
		            }else{
		            	if(this.env.pos.config.cash_rounding) {
			                if(!this.env.pos.get_order().check_paymentlines_rounding()) {
			                    this.showPopup('ErrorPopup', {
			                    	title: this.env._t('Rounding error in payment lines'),
			                        body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
			                    });
			                    return;
			                }
			            }
			            if (await this._isOrderValid(isForceValidate)) {
			                // remove pending payments before finalizing the validation
			                for (let line of this.paymentLines) {
			                    if (!line.is_done()) this.currentOrder.remove_paymentline(line);
			                }
			                await this._finalizeValidation();
			            }
		            }

	            	

	            }else{
		            	if(this.env.pos.config.cash_rounding) {
			                if(!this.env.pos.get_order().check_paymentlines_rounding()) {
			                    this.showPopup('ErrorPopup', {
			                    	title: this.env._t('Rounding error in payment lines'),
			                        body: this.env._t("The amount of your payment lines must be rounded to validate the transaction."),
			                    });
			                    return;
			                }
			            }
			            if (await this._isOrderValid(isForceValidate)) {
			                // remove pending payments before finalizing the validation
			                for (let line of this.paymentLines) {
			                    if (!line.is_done()) this.currentOrder.remove_paymentline(line);
			                }
			                await this._finalizeValidation();
			            }
	            }
	        }



	  






         
        }
    Registries.Component.extend(PaymentScreen, PosClient);
    return PosClient;



      
       
});
