odoo.define("pos_margin.OrderWidget", function (require) {
    "use strict";

    var OrderWidget = require("point_of_sale.OrderWidget");
    const Registries = require("point_of_sale.Registries");
    var field_utils = require("web.field_utils");

    const PosOrderWidget = (OrderWidget) =>
        class extends OrderWidget {
            _updateSummary() {
                super._updateSummary(...arguments);
                var order = this.env.pos.get_order();
                
                if (!order.get_orderlines().length) {
                    return;
                }
                var totalVal = order.get_total_without_tax();
                var totalTax = order.get_total_with_tax()
                var searchVal = $($(document).find("#superate-search"))[0].value;
                var balanc = $($(document).find("#resultado"))[0];
                if (searchVal > 0) {

                    //var base = (valSearch-(valSearch-total))
                    var tax = totalVal - searchVal//base * .18

                    
                    balanc.value = this.env.pos.format_currency(searchVal - totalTax);
                    /*
                    $($(document).find("#resultado"))[0].value = balanc.value
                    console.log("balan", balanc.value)
                    if (balanc.value < 0) {
                        $($(document).find("#resultado")).removeClass('targeta')
                        $($(document).find("#resultado")).addClass('targetaRed')
                    }
                    if (balanc.value >= 0) {
                        $($(document).find("#resultado")).removeClass('targetaRed')
                        $($(document).find("#resultado")).addClass('targeta')
                        
                    }
                    */
                }
            
            }
        };
    Registries.Component.extend(OrderWidget, PosOrderWidget);
    return OrderWidget;
});
