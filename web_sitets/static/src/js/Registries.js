odoo.define('web_sitets.Registries', function(require) {
    'use strict';

    /**
     * This definition contains all the instances of ClassRegistry.
     */

    const ComponentRegistry = require('web_sitets.ComponentRegistry');

    return { Component: new ComponentRegistry() };
});
