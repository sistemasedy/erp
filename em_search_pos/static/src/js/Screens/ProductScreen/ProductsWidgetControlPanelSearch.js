odoo.define('pos_margin.ProductsWidgetControlPanelSearch', function(require) {
    'use strict';

    const { useRef } = owl.hooks;
    const { debounce } = owl.utils;
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ProductsWidgetControlPanelSearch extends PosComponent {
        constructor() {
            super(...arguments);
            this.searchWordInput = useRef('search-word-input');
            this.updateSearch = debounce(this.updateSearch, 100);


        }
        clearSearch() {
            this.searchWordInput.el.value = '';
            this.trigger('clear-search');
        }
        updateSearch(event) {
            this.trigger('update-search', event.target.value);
            if (event.key === 'Enter') {
                // We are passing the searchWordInput ref so that when necessary,
                // it can be modified by the parent.
                this.trigger('try-add-product', { searchWordInput: this.searchWordInput });
            }
        }



        

        /*


        async _updateSelectedOrderline(event) {
            if(this.state.numpadMode === 'quantity' && this.env.pos.disallowLineQuantityChange()) {
                let order = this.env.pos.get_order();
                let selectedLine = order.get_selected_orderline();
                let lastId = order.orderlines.last().cid;
                let currentQuantity = this.env.pos.get_order().get_selected_orderline().get_quantity();

                if(selectedLine.noDecrease) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Invalid action'),
                        body: this.env._t('You are not allowed to change this quantity'),
                    });
                    return;
                }
                const parsedInput = event.detail.buffer && parse.float(event.detail.buffer) || 0;
                if(lastId != selectedLine.cid)
                    await this._showDecreaseQuantityPopup();
                else if(currentQuantity < parsedInput)
                    this._setValue(event.detail.buffer);
                else if(parsedInput < currentQuantity)
                    await this._showDecreaseQuantityPopup();
            } else {
                let { buffer } = event.detail;
                let val = buffer === null ? 'remove' : buffer;
                this._setValue(val);
            }
            if (this.env.pos.config.iface_customer_facing_display) {
                this.env.pos.send_current_order_to_customer_facing_display();
            }
        }

        */





    }
    ProductsWidgetControlPanelSearch.template = 'ProductsWidgetControlPanelSearch';

    Registries.Component.add(ProductsWidgetControlPanelSearch);

    return ProductsWidgetControlPanelSearch;
});
