/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ShowPaymentLineWidget } from "@account/js/account_payment_field"; // Ajusta la ruta si es necesario
import { ConfirmPopup } from "@point_of_sale/static/src/app/popups/confirm_popup/confirm_popup"; // O el módulo de Dialog/Popup apropiado
import { useService } from "@web/core/utils/hooks"; // Para llamar a RPC

patch(
  ShowPaymentLineWidget.prototype,
  "your_module_name.ShowPaymentLineWidgetPatch",
  {
    setup() {
      this._super();
      this.rpc = useService("rpc"); // Hook para usar el servicio RPC
      this.popup = useService("popup"); // Hook para usar el servicio de popups
    },

    async _onOutstandingCreditAssign(event) {
      event.preventDefault();
      const confirmed = await this.popup.add(ConfirmPopup, {
        title: this.env._t("Confirmar Asignación"),
        body: this.env._t(
          "¿Está seguro que desea asignar este crédito a la factura?"
        ),
      });

      if (confirmed) {
        const moveId = parseInt(event.currentTarget.dataset.id);
        await this.rpc(
          "/web/dataset/call_kw/account.move/js_assign_outstanding_line",
          {
            model: "account.move",
            method: "js_assign_outstanding_line",
            args: [[this.props.moveId], moveId], // Asumiendo que this.props.moveId es el ID del movimiento actual
            kwargs: {},
          }
        );
        this.trigger("reload-payment-lines"); // Evento personalizado para recargar, o una recarga más general.
        // O podrías necesitar disparar algo en el componente padre para refrescar,
        // dependiendo de cómo se renderizan tus líneas de pago.
      }
    },
  }
);
