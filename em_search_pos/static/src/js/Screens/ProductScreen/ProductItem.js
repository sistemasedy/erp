odoo.define('pos_margin.ProiductItem', function (require) {
    "use strict";

    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const ProductItem = require('point_of_sale.ProductItem');
    var core = require('web.core');
    var _t = core._t;

    const ProiductItem = ProductItem =>
        class extends ProductItem {
            constructor() {
                super(...arguments);
            }
            
           

         
        }
    Registries.Component.extend(ProductItem, ProiductItem);
    return ProiductItem;
});