odoo.define('web_sitets.test', function (require) {
'use strict';

var PosBaseWidget = require('web_sitets.BaseWidget');
var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var ajax = require('web.ajax');

require('web.dom_ready')


var button = $('#ver2')

var _onButton = function(e) {
    alert('ver dos 2')
}

button.click(_onButton)

var buttonDElete = $('#btn-deletes')

var _onButtonDelete = function(e) {
    alert('nuevo reordenamiento')
}

buttonDElete.click(_onButtonDelete)




});