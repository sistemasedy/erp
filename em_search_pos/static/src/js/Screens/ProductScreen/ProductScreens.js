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

            /*


            async _getProductByBarcode(code) {
                console.log("barra")
                let product = this.env.pos.db.get_product_by_barcode(code.base_code);
                if (!product) {
                    // find the barcode in the backend
                    let foundProductIds = [];
                    try {
                        foundProductIds = await this.rpc({
                            model: 'product.product',
                            method: 'search',
                            args: [[
                                ['barcode', '=', code.base_code],
                                ['sale_ok', '=', true],
                                ['available_in_pos', '=', true]
                            ]],
                            context: this.env.session.user_context,
                        });
                    } catch (error) {
                        if (isConnectionError(error)) {
                            return this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Network Error'),
                                body: this.env._t("Product is not loaded. Tried loading the product from the server but there is a network error."),
                            });
                        } else {
                            throw error;
                        }
                    }
                    if (foundProductIds.length) {
                        await this.env.pos._addProducts(foundProductIds, false);
                        // assume that the result is unique.
                        product = this.env.pos.db.get_product_by_id(foundProductIds[0]);
                    }
                }
                return product
            }


            */


            

           

            

         
        }
    Registries.Component.extend(ProductScreen, ProductScreenSearch);
    return ProductScreenSearch;
});