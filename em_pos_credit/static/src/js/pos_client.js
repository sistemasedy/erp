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

            //RECATURY

            //VALIDATION, MENSAGE CONTROL, MENSAGE ERROR, ORDERVALIDATE

            async validateOrder(isForceValidate) {
			    const order = this.currentOrder;
			    const currentClient = order.get_client();
			    const method = this._getClientPaymentMethod(order);

			    const showErrorPopup = (title, body) => {
			        this.showPopup('ErrorPopup', { title: this.env._t(title), body: this.env._t(body) });
			    };

			    const handleValidation = async () => {
			        if (this.env.pos.config.cash_rounding && !this.env.pos.get_order().check_paymentlines_rounding()) {
			            showErrorPopup('Rounding error in payment lines', "The amount of your payment lines must be rounded to validate the transaction.");
			            return;
			        }
			        if (await this._isOrderValid(isForceValidate)) {
			            this._removePendingPayments();
			            await this._finalizeValidation();
			        }
			    };

			    if (currentClient && currentClient.active_limit) {
			        if (method > 0 && currentClient.due_amount + method > currentClient.blocking_stage) {
			            showErrorPopup('Control de Cuenta de Clientes', "El Monto Excede el limite de Credito.");
			            return;
			        }
			        await handleValidation();
			    } else {
			        await handleValidation();
			    }
			}

			_getClientPaymentMethod(order) {
			    for (let line of order.paymentlines.models) {
			        if (line.name === "Cuenta de cliente") {
			            return line.amount;
			        }
			    }
			    return 0;
			}

			_removePendingPayments() {
			    for (let line of this.paymentLines) {
			        if (!line.is_done()) {
			            this.currentOrder.remove_paymentline(line);
			        }
			    }
			}

         
        }
    Registries.Component.extend(PaymentScreen, PosClient);
    return PosClient;



      
       
});
