odoo.define('em_search_pos.ProductScreens', function (require) {
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

    const ProductScreenSearch = ProductScreen =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);

             
                
                
            }


            

           

            

         
        }
    Registries.Component.extend(ProductScreen, ProductScreenSearch);
    return ProductScreenSearch;
});