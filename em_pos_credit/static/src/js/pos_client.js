odoo.define('em_pos_credit.PosClient', function(require) {
    'use strict';
       const PosComponent = require('point_of_sale.PosComponent');
       const PaymentScreen = require('point_of_sale.PaymentScreen');
       const { useListener } = require('web.custom_hooks');
       const Registries = require('point_of_sale.Registries');
       const models = require("point_of_sale.models");

       models.load_fields("res.partner", ["credit", "credit_limit", "due_amount"]);
       //models.load_fields("res.partner", ["credit", "credit_limit", "due_amount", "l10n_do_dgii_tax_payer_type"]);


       const PosClient = PaymentScreen =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
               
                
            }


            async selectClient() {
              // IMPROVEMENT: This code snippet is repeated multiple times.
              // Maybe it's better to create a function for it.
              const currentClient = this.currentOrder.get_client();
              const { confirmed, payload: newClient } = await this.showTempScreen(
                'ClientListScreen',
                { client: currentClient }
              );
              if (confirmed) {
                this.currentOrder.set_client(newClient);
                this.currentOrder.updatePricelist(newClient);
              }

              console.log("test", currentClient)
           }



         
        }
    Registries.Component.extend(PaymentScreen, PosClient);
    return PosClient;



      
       
});
