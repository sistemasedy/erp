odoo.define(
  "account_invoice_due_mac5.account_payment_field_extension",
  function (require) {
    "use strict";

    var ShowPaymentLineWidget = require("account.ShowPaymentLineWidget");
    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var _t = core._t;

    ShowPaymentLineWidget.include({
      _onOutstandingCreditAssign: function (event) {
        var self = this;
        event.preventDefault();

        Dialog.confirm(
          this,
          _t("¿Está seguro que desea asignar este crédito a la factura?"),
          {
            confirm_callback: function () {
              // Llamar al método original después de la confirmación
              self._super.apply(self, arguments);
            },
            title: _t("Confirmar Asignación"),
          }
        );
      },
    });
  }
);
