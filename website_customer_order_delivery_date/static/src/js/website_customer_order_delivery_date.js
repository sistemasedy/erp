odoo.define('website_customer_order_delivery_date.payment', function(require) {
    "use strict";

    var ajax = require('web.ajax');


    const data_json = [];

   


    $(document).ready(function() {

        

        


        try {
            $("#delivery_date").datepicker({
                minDate: new Date()
            });
        } catch (e) {}

        $("#delivery_date_icon").click(function(){
            $('#delivery_date').datepicker('show');
        });


        $('button[name="o_transfer_submit_button"]').bind("click", function(ev) {

            
            data_json.push({
                date : $('#delivery_date').val();,
                comment : $('#delivery_comment').val();,
                time : $('#up_time').val();
            });
            customer_order_delivery_date = $('#delivery_date').val();
            customer_order_delivery_comment = $('#delivery_comment').val();
            customer_order_time = $('#up_time').val();

            
            

            console.log(data_json);
        });

       

        

        $('button[name="o_payment_submit_button"]').bind("click", function(ev) {

            var list = []
            
            if (data_json.length > 0) {
                for (var i = 0; i < data_json.length; i++) {
                  list.push(data_json[i])
                }
            }




            ajax.jsonRpc('/shop/customer_order_delivery', 'call', {
                'delivery_date': list[0].date;,
                'delivery_comment': list[0].comment;,
                'up_time': list[0].time;
            });

            console.log(list);
        });
    });

});