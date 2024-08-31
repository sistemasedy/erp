odoo.define('pos_extended.screens', function(require) {
    'use strict';
    var rpc = require('web.rpc');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    const OrderReceipt = require('point_of_sale.OrderReceipt');

    // Load models to retrieve configuration and account move data
    models.load_models([{
        model: 'pos.config',
        fields: ['is_customer_details', 'is_customer_name', 'is_customer_address', 'is_customer_mobile', 'is_customer_phone', 'is_customer_email', 'is_customer_vat', 'is_qr_code', 'is_invoice_number'],
        loaded: function(self, pos_config) {
            self.pos_config = pos_config;
        }
    }, {
        model: 'account.move',
        fields: ['name'],
        loaded: function(self, account_move) {
            self.account_move = account_move;
        }
    }]);

    // Extend the Order model
    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attributes, options) {
            _super_order.initialize.apply(this, arguments);
            this.client_name = this.client_name || "";
            this.client_vat = this.client_vat || "";
            this.client_address = this.client_address || "";
            this.invoice_number = this.invoice_number || "";
            this.invoice_date = this.invoice_date || "";
            this.invoice_total = this.invoice_total || 0.0;
        },
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            json.client_name = this.get_client_name();
            json.client_vat = this.get_client_vat();
            json.client_address = this.get_client_address();
            json.invoice_number = this.get_invoice_number();
            json.invoice_date = this.get_invoice_date();
            json.invoice_total = this.get_invoice_total();
            return json;
        },
        init_from_JSON: function(json) {
            _super_order.init_from_JSON.apply(this, arguments);
            this.client_name = json.client_name || "";
            this.client_vat = json.client_vat || "";
            this.client_address = json.client_address || "";
            this.invoice_number = json.invoice_number || "";
            this.invoice_date = json.invoice_date || "";
            this.invoice_total = json.invoice_total || 0.0;
        },
        export_for_printing: function() {
            var receipt = _super_order.export_for_printing.apply(this, arguments);
            receipt.client_name = this.get_client_name();
            receipt.client_vat = this.get_client_vat();
            receipt.client_address = this.get_client_address();
            receipt.invoice_number = this.get_invoice_number();
            receipt.invoice_date = this.get_invoice_date();
            receipt.invoice_total = this.get_invoice_total();
            return receipt;
        },
        set_client_name: function(client_name) {
            this.client_name = client_name;
            this.trigger('change', this);
        },
        get_client_name: function() {
            return this.client_name;
        },
        set_client_vat: function(client_vat) {
            this.client_vat = client_vat;
            this.trigger('change', this);
        },
        get_client_vat: function() {
            return this.client_vat;
        },
        set_client_address: function(client_address) {
            this.client_address = client_address;
            this.trigger('change', this);
        },
        get_client_address: function() {
            return this.client_address;
        },
        set_invoice_number: function(invoice_number) {
            this.invoice_number = invoice_number;
            this.trigger('change', this);
        },
        get_invoice_number: function() {
            return this.invoice_number;
        },
        set_invoice_date: function(invoice_date) {
            this.invoice_date = invoice_date;
            this.trigger('change', this);
        },
        get_invoice_date: function() {
            return this.invoice_date;
        },
        set_invoice_total: function(invoice_total) {
            this.invoice_total = invoice_total;
            this.trigger('change', this);
        },
        get_invoice_total: function() {
            return this.invoice_total;
        }
    });

    const ExtendedOrderReceipt = (OrderReceipt) =>
        class extends OrderReceipt {
            setup() {
                super.setup();
            }
            // You can add more custom logic here if needed
        };

    Registries.Component.extend(OrderReceipt, ExtendedOrderReceipt);

    return OrderReceipt;
});

