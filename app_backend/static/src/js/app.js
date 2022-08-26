/* Copyright 2017 Openworx.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('app_backend.app', function (require) {
    "use strict";
    alert("test")
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var AppDashboardBase = AbstractAction.extend({

    })

    core.action_registry.add('app_dashboar_base', AppDashboardBase)
    return AppDashboardBase
    
     
});
