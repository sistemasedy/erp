# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ammu (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from odoo import fields, models



class PosConfig(models.Model):
    _inherit = "pos.config"

    def _search(self, args, offset=0, limit=None, order=None, count=False):
        # Obtener el usuario actual
        user = self.env.user

        # Verificar si el usuario es administrador
        if user.has_group('base.group_system'):
            # Los administradores pueden ver todos los puntos de venta
            return super(PosConfig, self)._search(args, offset=offset, limit=limit, order=order, count=count)
        else:
            # Para usuarios no-administradores
            if user.pos_conf_id:
                # Si el usuario tiene un PDV asignado, restringir la búsqueda a ese PDV
                domain = [('id', '=', user.pos_conf_id.id)]
                return super(PosConfig, self)._search(args + domain, offset=offset, limit=limit, order=order, count=count)
            else:
                # Si el usuario no tiene un PDV asignado, no mostrar nada
                domain = [('id', '=', False)]
                return super(PosConfig, self)._search(args + domain, offset=offset, limit=limit, order=order, count=count)

                


class ResUsers(models.Model):
    """User Inherit"""
    _inherit = "res.users"

    pos_conf_id = fields.Many2one('pos.config', string="POS Configuration")
