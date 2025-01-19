"use strict";

odoo.define(
  "account_invoice_due_mac5.account_payment_field_extension",
  function (require) {
    "use strict";

    var ShowPaymentLineWidget = require("account.payment");
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
              // Llamar al método original
              var moveId = parseInt(event.currentTarget.dataset.id);
              self
                ._rpc({
                  model: "account.move",
                  method: "js_assign_outstanding_line",
                  args: [self.res_id, moveId],
                })
                .then(function () {
                  self.trigger_up("reload");
                });
            },
            cancel_callback: function () {
              return false;
            },
            title: _t("Confirmar Asignación"),
            buttons: [
              {
                text: _t("Confirmar"),
                classes: "btn-primary",
                close: true,
                click: function () {
                  this.confirm_callback();
                },
              },
              {
                text: _t("Cancelar"),
                close: true,
              },
            ],
          }
        );
      },
    });
  }
);
