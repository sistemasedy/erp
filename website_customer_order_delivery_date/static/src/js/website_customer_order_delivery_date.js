odoo.define('website_customer_order_delivery_date.payment', function(require) {
    "use strict";

    var ajax = require('web.ajax');

    $(document).ready(function() {

        var customer_order_delivery_date = "";
        var customer_order_delivery_comment = "";
        var customer_order_time = "";


        try {
            $("#delivery_date").datepicker({
                minDate: new Date()
            });
        } catch (e) {}

        $("#delivery_date_icon").click(function(){
            $('#delivery_date').datepicker('show');
        });


        $('button[name="o_transfer_submit_button"]').bind("click", function(ev) {

            var customer_order_delivery_date = $('#delivery_date').val();
            var customer_order_delivery_comment = $('#delivery_comment').val();
            var customer_order_time = $('#up_time').val();
            

            console.log(customer_order_delivery_date,customer_order_delivery_comment,customer_order_time);
        });

       

        

        $('button[name="o_payment_submit_button"]').bind("click", function(ev) {
            ajax.jsonRpc('/shop/customer_order_delivery', 'call', {
                'delivery_date': customer_order_delivery_date,
                'delivery_comment': customer_order_delivery_comment,
                'up_time': customer_order_time
            });

            console.log(customer_order_delivery_date,customer_order_delivery_comment,customer_order_time);
        });
    });

});