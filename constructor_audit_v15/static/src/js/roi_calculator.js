/* Constructor Audit – ROI calculator (Odoo 15) */
odoo.define('constructor_audit_v15.roi_calculator', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    publicWidget.registry.AuditRoiCalculator = publicWidget.Widget.extend({
        selector: '#audit-roi-result',
        start: function () {
            var el = this.el;
            var roi   = parseFloat(el.dataset.roi   || 0);
            var score = parseFloat(el.dataset.score || 0);
            var nivel = el.dataset.nivel || 'intermedio';
            var roiEl   = document.getElementById('audit-roi-amount');
            var scoreEl = document.getElementById('audit-score-number');
            if (roiEl)   { this._anim(roiEl,   0, roi,   1200, function(v){ return '$'+Math.round(v).toLocaleString('en-US'); }); }
            if (scoreEl) { this._anim(scoreEl,  0, score, 900,  function(v){ return Math.round(v); }); }
            document.querySelectorAll('.audit-bar-fill[data-pct]').forEach(function(b){
                setTimeout(function(){ b.style.width = b.dataset.pct+'%'; }, 400);
            });
            var badge = document.getElementById('audit-nivel-badge');
            if (badge) { badge.classList.add(nivel); }
            return this._super.apply(this, arguments);
        },
        _anim: function(el, from, to, dur, fmt) {
            var t0 = performance.now();
            (function step(now) {
                var p = Math.min((now-t0)/dur, 1), e = 1-Math.pow(1-p,3);
                el.textContent = fmt(from+(to-from)*e);
                if (p<1) requestAnimationFrame(step);
            })(t0);
        },
    });
    return publicWidget.registry.AuditRoiCalculator;
});
