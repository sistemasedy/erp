odoo.define('web_sitets.screens', function (require) {
    'use strict';

    require('web.dom_ready')


    var button = $('#ver')

    var _onButton = function(e) {
        alert('otro mas')
    }

    button.click(_onButton)
});