odoo.define('pos_identification.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc')

    models.load_fields('res.partner', ['l10n_do_dgii_tax_payer_type',
                                          'l10n_do_expense_type']);


    models.load_models([{
        model: 'res.partner',
        domain: async function(self){
            const result = await self.rpc({
                  model: 'res.partner',
                  method: '_get_l10n_do_dgii_payer_types_selection'
            });
            return result
        }
    }]);


     

}); 