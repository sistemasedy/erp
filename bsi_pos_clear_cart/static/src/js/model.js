odoo.define('pos_identification.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_fields('res.partner', ['l10n_do_dgii_tax_payer_type',
                                          'l10n_do_expense_type']);


     

}); 