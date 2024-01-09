odoo.define('pos_identification.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('res.partner', ['l10n_do_dgii_tax_payer_type',
                                          'l10n_do_expense_type']);


    models.load_models([{
        model: 'res.partner',
        loaded: function (self, _get_l10n_do_dgii_payer_types_selection) {
            self._get_l10n_do_dgii_payer_types_selection = _get_l10n_do_dgii_payer_types_selection;
        }
    }]);


     

}); 