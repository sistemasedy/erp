// Copyright (C) 2021 - Initos Gmbh
// @author: Dhara Solanki (dhara.solanki@initos.com)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('pos_margin.product_create_popup', function(require) {
    'use strict';

    const {
        useState,
        useRef
    } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    const PosComponent = require('point_of_sale.PosComponent');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    
    const { parse } = require('web.field_utils');
    

    class ProductCreatePopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            //console.log(this.env.pos, '<<<<<<<<<<<<<<<')
            this.state = useState({
                typeValue: this.props.startingValue,
                productValue: this.props.startingValue,
                priceValue: this.props.priceValue,
                productRef: this.props.startingValue
            });
            useListener('click-product', this._clickProduct);


        }



        get currentOrder() {
            return this.env.pos.get_order();
        }
        showCashBoxOpening() {
            if(this.env.pos.config.cash_control && this.env.pos.pos_session.state == 'opening_control')
                return true;
            return false;
        }
        async _getAddProductOptions(product) {
            let price_extra = 0.0;
            let draftPackLotLines, weight, description, packLotLinesToEdit;

            if (this.env.pos.config.product_configurator && _.some(product.attribute_line_ids, (id) => id in this.env.pos.attributes_by_ptal_id)) {
                let attributes = _.map(product.attribute_line_ids, (id) => this.env.pos.attributes_by_ptal_id[id])
                                  .filter((attr) => attr !== undefined);
                let { confirmed, payload } = await this.showPopup('ProductConfiguratorPopup', {
                    product: product,
                    attributes: attributes,
                });

                if (confirmed) {
                    description = payload.selected_attributes.join(', ');
                    price_extra += payload.price_extra;
                } else {
                    return;
                }
            }

            // Gather lot information if required.
            if (['serial', 'lot'].includes(product.tracking) && (this.env.pos.picking_type.use_create_lots || this.env.pos.picking_type.use_existing_lots)) {
                const isAllowOnlyOneLot = product.isAllowOnlyOneLot();
                if (isAllowOnlyOneLot) {
                    packLotLinesToEdit = [];
                } else {
                    const orderline = this.currentOrder
                        .get_orderlines()
                        .filter(line => !line.get_discount())
                        .find(line => line.product.id === product.id);
                    if (orderline) {
                        packLotLinesToEdit = orderline.getPackLotLinesToEdit();
                    } else {
                        packLotLinesToEdit = [];
                    }
                }
                const { confirmed, payload } = await this.showPopup('EditListPopup', {
                    title: this.env._t('Lot/Serial Number(s) Required'),
                    isSingleItem: isAllowOnlyOneLot,
                    array: packLotLinesToEdit,
                });
                if (confirmed) {
                    // Segregate the old and new packlot lines
                    const modifiedPackLotLines = Object.fromEntries(
                        payload.newArray.filter(item => item.id).map(item => [item.id, item.text])
                    );
                    const newPackLotLines = payload.newArray
                        .filter(item => !item.id)
                        .map(item => ({ lot_name: item.text }));

                    draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                } else {
                    // We don't proceed on adding product.
                    return;
                }
            }

            // Take the weight if necessary.
            if (product.to_weight && this.env.pos.config.iface_electronic_scale) {
                // Show the ScaleScreen to weigh the product.
                if (this.isScaleAvailable) {
                    const { confirmed, payload } = await this.showTempScreen('ScaleScreen', {
                        product,
                    });
                    if (confirmed) {
                        weight = payload.weight;
                    } else {
                        // do not add the product;
                        return;
                    }
                } else {
                    await this._onScaleNotAvailable();
                }
            }

            return { draftPackLotLines, quantity: weight, description, price_extra };
        }
        async _clickProduct(event) {
            if (!this.currentOrder) {
                this.env.pos.add_new_order();
            }
            console.log("add ")

            const product = event.detail;
            const options = await this._getAddProductOptions(product);
            // Do not add product if options is undefined.
            if (!options) return;
            // Add the product after having the extra information.
            this.currentOrder.add_product(product, options);
            NumberBuffer.reset();
        }



        getPayload() {
            var selected_vals = [];
            var category = this.state.typeValue;
            var product = this.state.productValue;
            var product_reference = this.state.productRef;
            var price = this.state.priceValue;
            var unit = this.state.unitValue;
            var product_category = this.state.categoryValue;
            selected_vals.push(category);
            selected_vals.push(product);
            selected_vals.push(product_reference);
            selected_vals.push(price);
            selected_vals.push(unit);
            selected_vals.push(product_category);
            return selected_vals
        }
    }
    ProductCreatePopup.template = 'ProductCreatePopup';
    ProductCreatePopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        array: [],
        title: 'Create ?',
        body: '',
        startingValue: '',
        priceValue: 1,
        list: [],
    };

    Registries.Component.add(ProductCreatePopup);

    return ProductCreatePopup;
});