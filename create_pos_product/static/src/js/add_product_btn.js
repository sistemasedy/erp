odoo.define('pos_custom_buttons.RewardButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   const ajax = require('web.ajax');
   class CustomRewardButtons extends PosComponent {
       constructor() {
           super(...arguments);
           useListener('click', this.onClick);
       }
       is_available() {
           const order = this.env.pos.get_order();
           return order
       }
       async onClick() {
            var self = this;
            const {
                confirmed,
                payload
            } = await this.showPopup('Add_product_popup', {
                title: this.env._t(' Add Product'),
                body: this.env._t('Add New Product'),
            });
            if (confirmed) {
                var product_category = payload[0];
                var product_name = payload[1];
                var product_price = payload[2];
                var product_type = payload[3];
                var product_uom = payload[4];
                ajax.jsonRpc('/Add_Product', 'call', {
                    'category': product_category,
                    'name': product_name,
                    'price': product_price,
                    'uom': product_uom,
                    'type': product_type,
                }).then(function(response) {});
            }
        }
   }
   CustomRewardButtons.template = 'CustomRewardButtons';
   ProductScreen.addControlButton({
       component: CustomRewardButtons,
       condition: function() {
           return this.env.pos;
       },
   });
   Registries.Component.add(CustomRewardButtons);
   return CustomRewardButtons;
});