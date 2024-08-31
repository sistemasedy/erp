odoo.define('pos_l10n_ar_identification.screens', function(require) {
    'use strict';

    var rpc = require('web.rpc');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    
    // Load models to retrieve configuration and account move data
    // Load 'pos.config' model fields
    models.load_models([{
        model: 'pos.config',
        fields: ['is_customer_details', 'is_customer_name', 'is_customer_address', 'is_customer_mobile', 'is_customer_phone', 'is_customer_email', 'is_customer_vat', 'is_qr_code', 'is_invoice_number'],
        loaded: function(self, pos_config) {
            self.pos_config = pos_config;
        }
    }]);

    // Load 'account.move' model fields
    models.load_models([{
        model: 'account.move',
        fields: ['name'],
        loaded: function(self, account_move) {
            self.account_move = account_move;
        }
    }]);

    // Extend the Order model to include client and invoice information in the receipt
    models.Order = models.Order.extend({
        export_for_printing: function() {
            var receipt = this._super();
            var client = this.get_client();
            var invoice = this.get_invoice();
            
            receipt.client = client ? client.name : '';
            receipt.invoice_number = invoice ? invoice.name : '';

            return receipt;
        },
    });

    const FiscalReceip = OrderReceipt =>
        class extends OrderReceipt {
            setup() {
                super.setup();
            }
            // You can add more custom logic here if needed
        };

    Registries.Component.extend(OrderReceipt, FiscalReceip);

    return OrderReceipt;
});

