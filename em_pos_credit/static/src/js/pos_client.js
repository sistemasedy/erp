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

    const PosClient = PaymentScreen =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
            }

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

                if (currentClient && method > 0) {
                    if (!currentClient.active_limit) {
                        showErrorPopup('Control de Cuenta de Clientes', "El cliente no tiene crédito activado y no puede realizar compras a crédito.");
                        return;
                    }

                    if (currentClient.due_amount + method > currentClient.blocking_stage) {
                        const deudaPendiente = currentClient.due_amount;
                        const saldoDisponible = currentClient.blocking_stage - deudaPendiente;
                        
                        const mensajeError = `El Monto Excede el límite de Crédito. 
                                              Deuda pendiente: ${deudaPendiente.toFixed(2)}. 
                                              Saldo disponible: ${saldoDisponible.toFixed(2)}.`;
                        
                        showErrorPopup('Control de Cuenta de Clientes', mensajeError);
                        return;
                    }
                }

                await handleValidation();
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
