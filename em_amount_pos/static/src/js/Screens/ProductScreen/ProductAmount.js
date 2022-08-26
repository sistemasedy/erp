odoo.define('pos_margin.ProductAmount', function (require) {
    "use strict";


    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    var core = require('web.core');
    var _t = core._t;
    const balance = []

    const ProductScreens = ProductScreen =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
                //useListener('payment-direct', this.PaymentDirect);
                this.state = useState({ cashControl: status, numpadMode: 'price' });
               
                
            }

            _setValue(val) {
                if (this.currentOrder.get_selected_orderline()) {
                    
                    if (this.state.numpadMode === 'quantity') {
                        this.currentOrder.get_selected_orderline().set_quantity(val);
                    } else if (this.state.numpadMode === 'discount') {
                        this.currentOrder.get_selected_orderline().set_discount(val);
                        
                    } else if (this.state.numpadMode === 'price') {
                        
                        var selected_orderline = this.currentOrder.get_selected_orderline();
                        selected_orderline.price_manually_set = true;
                        var precio = selected_orderline.get_unit_price();
                        var cantidad = val/precio
                        console.log(cantidad)
                        this.currentOrder.get_selected_orderline().set_quantity(cantidad);
                        //selected_orderline.set_unit_price(val);
                        var valor = selected_orderline.get_display_price();

                    }
                    if (this.env.pos.config.iface_customer_facing_display) {
                        this.env.pos.send_current_order_to_customer_facing_display();
                    }
                }
            }

            

         
        }
    Registries.Component.extend(ProductScreen, ProductScreens);
    return ProductScreens;
});