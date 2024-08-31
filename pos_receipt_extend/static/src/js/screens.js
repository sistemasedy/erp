odoo.define('pos_extended.order', function (require) {
    'use strict';

    var models = require('point_of_sale.models');
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
        set_client: function(client) {
            _super_order.set_client.apply(this, arguments);
            if (client) {
                this.set_client_name(client.name);
                this.set_client_vat(client.vat);
                this.set_client_address(client.address);
            }
        },
        set_client_name: function(name) {
            this.client_name = name;
            this.trigger('change', this);
        },
        get_client_name: function() {
            return this.client_name;
        },
        set_client_vat: function(vat) {
            this.client_vat = vat;
            this.trigger('change', this);
        },
        get_client_vat: function() {
            return this.client_vat;
        },
        set_client_address: function(address) {
            this.client_address = address;
            this.trigger('change', this);
        },
        get_client_address: function() {
            return this.client_address;
        },
        set_invoice_number: function(number) {
            this.invoice_number = number;
            this.trigger('change', this);
        },
        get_invoice_number: function() {
            return this.invoice_number;
        },
        set_invoice_date: function(date) {
            this.invoice_date = date;
            this.trigger('change', this);
        },
        get_invoice_date: function() {
            return this.invoice_date;
        },
        set_invoice_total: function(total) {
            this.invoice_total = total;
            this.trigger('change', this);
        },
        get_invoice_total: function() {
            return this.invoice_total;
        }
    });
});

