# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools, os
import json
from odoo.modules.module import get_module_resource 


class PosOrder(models.Model):
    _inherit = "pos.order"

    # Compute Section
    
    def search_ncf(self):
        #path = get_module_resource(pos_margin, "static\DGII_RNC\TMP\DGII_RNC.TXT")
        data = [
             {
               num: "1",
               desc: "desc"
             },
             {
               num: "2",
               desc: "desc2"
             }
        ]
        path = True #os.path.expanduser("C:\master\custom\mcf.txt")
         if path:
             with data as desc_file:
                 doc = desc_file
        return doc
