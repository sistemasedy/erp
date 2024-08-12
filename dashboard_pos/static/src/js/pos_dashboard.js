odoo.define('dashboard_pos.Dashboard', function (require) {
"use strict";

  var AbstractAction = require('web.AbstractAction');
  var ajax = require('web.ajax');
  var core = require('web.core');
  var rpc = require('web.rpc');
  var session = require('web.session');
  var web_client = require('web.web_client');
  var _t = core._t;
  var QWeb = core.qweb;
  var datepicker = require('web.datepicker');
  var time = require('web.time');
  var framework = require('web.framework');
  var session = require('web.session');

  var PosDashboard = AbstractAction.extend({
      template: 'PosDashboard',
      events: {
              'click #fetch_data_btn': 'fetch_data2',
              'click #mes_actual_btn': 'fetch_actualmes',
              'click .pos_order_today':'pos_order_today',
              'click .pos_order':'pos_order',
              'click .pos_total_sales':'pos_order',
              'click .pos_session':'pos_session',
              'click .pos_refund_orders':'pos_refund_orders',
              'click .pos_refund_today_orders':'pos_refund_today_orders',
              'change #pos_sales': 'onclick_pos_sales',
      },

     

      init: function(parent, context) {
        this._super(parent, context);
        this.dashboards_templates = ['PosOrders', 'PosChart', 'PosCustomer'];
        this.payment_details = [];
        this.top_salesperson = [];
        this.selling_product = [];
        this.venta = [];
        this.total_order_count = [];
        this.total_refund_count = [];
        this.total_session = [];
        this.today_refund_total = [];
        this.today_sale = [];
        this.total_cost = [];
        this.total_profit = [];
    },



      willStart: function() {
          var self = this;
          return $.when(ajax.loadLibs(this), this._super()).then(function() {
              return self.fetch_data(),self.targeta2();
          });
      },

      start: function() {
          var self = this;
          this.set("title", 'Dashboard');

          

          return this._super().then(function() {
              self.render_dashboards();
              self.render_graphs();
              self.$el.parent().addClass('oe_background_grey');
          });
      },

      



      fetch_data: function() {
          var self = this;

          console.log("fecha");
          self.initial_render = false;

          var start_date = $('#start_date').val();  // Obtener fecha desde un campo de entrada
          var end_date = $('#end_date').val();

          // Si no se proporciona la fecha de inicio, se establece en 30 días atrás desde hoy
          if (!start_date) {
              var today = new Date();
              var pastDate = new Date();
              pastDate.setDate(today.getDate() - 7);
              start_date = pastDate.toISOString().split('T')[0];  // Formato YYYY-MM-DD
          }

          // Si no se proporciona la fecha de fin, se establece en la fecha de hoy
          if (!end_date) {
              var today = new Date();
              end_date = today.toISOString().split('T')[0];  // Formato YYYY-MM-DD
          }

          console.log("start", start_date);

          var def1 = this._rpc({
              model: 'pos.order',
              method: 'get_refund_details',
              args: [start_date, end_date],  // Pasar start_date y end_date aquí
          }).then(function(result) {
              console.log("Respuesta recibida de get_refund_details", result);
              self.venta = result['venta'];
              self.total_cost = result['total_cost'];
              self.total_profit = result['total_profit'];
              self.total_order_count = result['total_order_count'];
              self.total_refund_count = result['total_refund_count'];
              self.total_session = result['total_session'];
              self.today_refund_total = result['today_refund_total'];
              self.today_sale = result['today_sale'];
              self.fecha = result['fecha'];
              self.fecha2 = result['fecha2'];
              self.today_sale_today = result['today_sale_today'];
              
              
          });

          console.log("recibida", self.fecha);
          console.log("la default", self.fecha2);

          var def2 = self._rpc({
              model: "pos.order",
              method: "get_details",
          }).then(function(res) {
              self.payment_details = res['payment_details'];
              self.top_salesperson = res['salesperson'];
              self.selling_product = res['selling_product'];
          });

          return $.when(def1, def2);
      },



      fetch_data2: function() {
          var self = this;
          console.log("fecha");
          self.initial_render = false;

          var start_date = $('#start_date').val();
          var end_date = $('#end_date').val();

          if (!start_date) {
              var today = new Date();
              var pastDate = new Date();
              pastDate.setDate(today.getDate() - 30);
              start_date = pastDate.toISOString().split('T')[0];
          }

          if (!end_date) {
              var today = new Date();
              end_date = today.toISOString().split('T')[0];
          }

          console.log("start", start_date);

          var def1 = this._rpc({
              model: 'pos.order',
              method: 'get_refund_details2',
              args: [start_date, end_date],
          }).then(function(result) {
              console.log("Respuesta recibida de get_refund_details", result);
              self.venta = result['venta'];
              self.total_cost = result['total_cost'];
              self.total_profit = result['total_profit'];

              // Función para crear los widgets de estadísticas
              self.targeta(self.venta,self.total_cost,self.total_profit);
              self.targeta2();

          });

          var def2 = self._rpc({
              model: "pos.order",
              method: "get_details",
          }).then(function(res) {
              self.payment_details = res['payment_details'];
              self.top_salesperson = res['salesperson'];
              self.selling_product = res['selling_product'];
          });

          return $.when(def1, def2);
      },

      fetch_actualmes: function() {
          var self = this;
          console.log("fecha");
          self.initial_render = false;

          var start_date = $('#start_date').val();
          var end_date = $('#end_date').val();

          if (!start_date) {
              var today = new Date();
              var pastDate = new Date(today.getFullYear(), today.getMonth(), 1); // Primer día del mes actual
              start_date = pastDate.toISOString().split('T')[0];
          }

          if (!end_date) {
              var today = new Date();
              end_date = today.toISOString().split('T')[0];
          }

          console.log("start", start_date);

          var def1 = this._rpc({
              model: 'pos.order',
              method: 'get_refund_details2',
              args: [start_date, end_date],
          }).then(function(result) {
              console.log("Respuesta recibida de get_refund_details", result);
              self.venta = result['venta'];
              self.total_cost = result['total_cost'];
              self.total_profit = result['total_profit'];

              // Función para crear los widgets de estadísticas
              self.targeta(self.venta,self.total_cost,self.total_profit);
              self.targeta2();

          });

          var def2 = self._rpc({
              model: "pos.order",
              method: "get_details",
          }).then(function(res) {
              self.payment_details = res['payment_details'];
              self.top_salesperson = res['salesperson'];
              self.selling_product = res['selling_product'];
          });

          return $.when(def1, def2);
      },

      targeta: function(venta, total_cost, total_profit) {
          var self = this;

          // Función para crear los widgets de estadísticas
          function createStatWidget(title, iconClass, value, color) {
              var colDiv = document.createElement('div');
              colDiv.className = 'col-md-4 col-sm-6 pos_order_today oh-payslip';

              var cardDiv = document.createElement('div');
              cardDiv.className = 'oh-card';
              cardDiv.style.width = '288px';

              var cardBodyDiv = document.createElement('div');
              cardBodyDiv.className = 'oh-card-body';

              var widgetDiv = document.createElement('div');
              widgetDiv.className = 'stat-widget-one';

              var iconDiv = document.createElement('div');
              iconDiv.className = 'stat-icon';
              iconDiv.style.background = color;

              var iconElement = document.createElement('i');
              iconElement.className = iconClass;

              var contentDiv = document.createElement('div');
              contentDiv.className = 'stat-content';

              var headDiv = document.createElement('div');
              headDiv.className = 'stat-head';
              headDiv.textContent = title;
              headDiv.style.fontSize = '20px';  // Reducir tamaño de la fuente del título

              var countDiv = document.createElement('div');
              countDiv.className = 'stat_count';
              countDiv.textContent = value;
              countDiv.style.fontSize = '25px';  // Reducir tamaño de la fuente del valor

              iconDiv.appendChild(iconElement);
              contentDiv.appendChild(headDiv);
              contentDiv.appendChild(countDiv);
              widgetDiv.appendChild(iconDiv);
              widgetDiv.appendChild(contentDiv);
              cardBodyDiv.appendChild(widgetDiv);
              cardDiv.appendChild(cardBodyDiv);
              colDiv.appendChild(cardDiv);

              return colDiv;
          }

          // Crear y agregar los widgets al DOM
          var container = document.getElementById('main_container');  // Suponiendo que tienes un contenedor con id 'main_container'
          container.innerHTML = '';  // Limpiar el contenedor antes de agregar nuevos elementos

          var ventaWidget = createStatWidget('Total Venta', 'fa fa-shopping-bag', venta, '#5bcbd0');
          var costosWidget = createStatWidget('Total Costos', 'fa fa-shopping-bag', total_cost, '#5bcbd0');
          var gananciaWidget = createStatWidget('Ganancia Bruta', 'fa fa-money', total_profit, '#5bcbd0');

          container.appendChild(ventaWidget);
          container.appendChild(costosWidget);
          container.appendChild(gananciaWidget);
      },


      targeta2: function() {
          var self = this;

          // Función para crear los widgets de estadísticas
          // Obtener la fecha actual
          var today = new Date();

          // Obtener el nombre del mes actual en español
          var nombre_mes_actual = today.toLocaleString('es-ES', { month: 'long' });

          // Colocar el nombre del mes actual en el texto del botón
          $('#mes_actual_text').text("Mes actual: " + nombre_mes_actual.charAt(0).toUpperCase() + nombre_mes_actual.slice(1));
          
          // Crear el botón "Apply"
          var applyButton = document.createElement('button');
          applyButton.type = "button";
          applyButton.id = "mes_actual_btn";
          applyButton.className = "btn btn-primary";
          applyButton.style = "margin-right: 5px; padding: 4px; top: 0px; height: 42px; color: white; background-color: #7c7bad; border-color: #7c7bad;";
          applyButton.textContent = nombre_mes_actual.charAt(0).toUpperCase() + nombre_mes_actual.slice(1);

          // Obtener el contenedor con id "mes_actual"
          var mesActualDiv = document.getElementById('mes_actual');

          // Asegurarse de que el contenedor exista antes de agregar el botón
          if (mesActualDiv) {
              mesActualDiv.appendChild(applyButton);
          }
      },












      mes_actual: function(events) {
        var self = this;

        // Obtener las fechas de los campos de entrada
        var start_date = $('#start_date').val();
        var end_date = $('#end_date').val();

        var def1 = this._rpc({
            model: 'pos.order',
            method: 'get_mes_actual',
            args: [start_date, end_date],  // Puedes pasar start_date y end_date aquí
        }).then(function(result) {
            self.venta = result['venta'],
            self.total_cost = result['total_cost'],
            self.total_profit = result['total_profit'],
            self.total_order_count = result['total_order_count'],
            self.total_refund_count = result['total_refund_count'],
            self.total_session = result['total_session'],
            self.today_refund_total = result['today_refund_total'],
            self.today_sale = result['today_sale'],
            self.fecha = result['fecha'],
            self.fecha2 = result['fecha2'],
            self.today_sale_today = result['today_sale_today']
        });
        console.log("mes", self.fecha)
        console.log("la defauld", self.fecha2)

        var def2 = self._rpc({
            model: "pos.order",
            method: "get_details",
        }).then(function(res) {
            self.payment_details = res['payment_details'];
            self.top_salesperson = res['salesperson'];
            self.selling_product = res['selling_product'];
        });

        return $.when(def1, def2);
      },

      render_dashboards: function() {
          var self = this;
              _.each(this.dashboards_templates, function(template) {
                  self.$('.o_pos_dashboard').append(QWeb.render(template, {widget: self}));
              });
      },
        render_graphs: function(){
          var self = this;
           self.render_top_customer_graph();
           self.render_top_product_graph();
           self.render_product_category_graph();
      },
  //      get_emp_image_url: function(employee){
  //        return window.location.origin + '/web/image?model=pos.order&field=image&id='+employee;
  //    },




         pos_order_today: function(e){
          var self = this;
          var date = new Date();
          var yesterday = new Date(date.getTime());
          yesterday.setDate(date.getDate() - 1);
          console.log(yesterday)
          e.stopPropagation();
          e.preventDefault();

          session.user_has_group('hr.group_hr_user').then(function(has_group){
              if(has_group){
                  var options = {
                      on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                  };
                  self.do_action({
                      name: _t("Today Order"),
                      type: 'ir.actions.act_window',
                      res_model: 'pos.order',
                      view_mode: 'tree,form,calendar',
                      view_type: 'form',
                      views: [[false, 'list'],[false, 'form']],
                      domain: [['date_order','<=', date],['date_order', '>=', yesterday]],
                      target: 'current'
                  }, options)
              }
          });

      },


        pos_refund_orders: function(e){
          var self = this;
          var date = new Date();
  //        alert(date,"date")
          var yesterday = new Date(date.getTime());
          yesterday.setDate(date.getDate() - 1);
          console.log(yesterday)
          e.stopPropagation();
          e.preventDefault();

          session.user_has_group('hr.group_hr_user').then(function(has_group){
              if(has_group){
                  var options = {
                      on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                  };
                  self.do_action({
                      name: _t("Refund Orders"),
                      type: 'ir.actions.act_window',
                      res_model: 'pos.order',
                      view_mode: 'tree,form,calendar',
                      view_type: 'form',
                      views: [[false, 'list'],[false, 'form']],
                      domain: [['amount_total', '<', 0.0]],

  //                    domain: [['date_order', '=', date]],
                      target: 'current'
                  }, options)
              }
          });

      },
      pos_refund_today_orders: function(e){
          var self = this;
          var date = new Date();
  //        alert(date,"date")
          var yesterday = new Date(date.getTime());
          yesterday.setDate(date.getDate() - 1);
          console.log(yesterday)
          e.stopPropagation();
          e.preventDefault();

          session.user_has_group('hr.group_hr_user').then(function(has_group){
              if(has_group){
                  var options = {
                      on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                  };
                  self.do_action({
                      name: _t("Refund Orders"),
                      type: 'ir.actions.act_window',
                      res_model: 'pos.order',
                      view_mode: 'tree,form,calendar',
                      view_type: 'form',
                      views: [[false, 'list'],[false, 'form']],
                      domain: [['amount_total', '<', 0.0],['date_order','<=', date],['date_order', '>=', yesterday]],
  //                    domain: [['date_order', '=', date]],
                      target: 'current'
                  }, options)
              }
          });

      },

          pos_order: function(e){
          var self = this;
          var date = new Date();
          var yesterday = new Date(date.getTime());
          yesterday.setDate(date.getDate() - 1);
          console.log(yesterday)
          e.stopPropagation();
          e.preventDefault();
          session.user_has_group('hr.group_hr_user').then(function(has_group){
              if(has_group){
                  var options = {
                      on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                  };
                  self.do_action({
                      name: _t("Total Order"),
                      type: 'ir.actions.act_window',
                      res_model: 'pos.order',
                      view_mode: 'tree,form,calendar',
                      view_type: 'form',
                      views: [[false, 'list'],[false, 'form']],
  //                    domain: [['amount_total', '<', 0.0]],
                      target: 'current'
                  }, options)
              }
          });

      },
      pos_session: function(e){
          var self = this;
          e.stopPropagation();
          e.preventDefault();
          session.user_has_group('hr.group_hr_user').then(function(has_group){
              if(has_group){
                  var options = {
                      on_reverse_breadcrumb: self.on_reverse_breadcrumb,
                  };
                  self.do_action({
                      name: _t("sessions"),
                      type: 'ir.actions.act_window',
                      res_model: 'pos.session',
                      view_mode: 'tree,form,calendar',
                      view_type: 'form',
                      views: [[false, 'list'],[false, 'form']],
  //                     domain: [['state','=', In Progress]],
                      target: 'current'
                  }, options)
              }
          });

      },

       onclick_pos_sales:function(events){
          var option = $(events.target).val();
          console.log('came monthly')
         var self = this
          var ctx = self.$("#canvas_1");
              rpc.query({
                  model: "pos.order",
                  method: "get_department",
                  args: [option],
              }).then(function (arrays) {
              console.log(arrays)
            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: arrays[2],
                  data: arrays[0],
                  backgroundColor: [
                    "rgba(255, 99, 132,1)",
                    "rgba(54, 162, 235,1)",
                    "rgba(75, 192, 192,1)",
                    "rgba(153, 102, 255,1)",
                    "rgba(10,20,30,1)"
                  ],
                  borderColor: [
                   "rgba(255, 99, 132, 0.2)",
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(10,20,30,0.3)"
                  ],
                  borderWidth: 1
                },

              ]
            };

    //options
            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                text: "SALE DETAILS",
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#333",
                  fontSize: 16
                }
              },
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            if (window.myCharts != undefined)
            window.myCharts.destroy();
            window.myCharts = new Chart(ctx, {
  //          var chart = new Chart(ctx, {
              type: "bar",
              data: data,
              options: options
            });

          });
          },


       render_top_customer_graph:function(){
         var self = this
          var ctx = self.$(".top_customer");
              rpc.query({
                  model: "pos.order",
                  method: "get_the_top_customer",
              }).then(function (arrays) {


            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: "",
                  data: arrays[0],
                  backgroundColor: [
                    "rgb(148, 22, 227)",
                    "rgba(54, 162, 235)",
                    "rgba(75, 192, 192)",
                    "rgba(153, 102, 255)",
                    "rgba(10,20,30)"
                  ],
                  borderColor: [
                   "rgba(255, 99, 132,)",
                    "rgba(54, 162, 235,)",
                    "rgba(75, 192, 192,)",
                    "rgba(153, 102, 255,)",
                    "rgba(10,20,30,)"
                  ],
                  borderWidth: 1
                },

              ]
            };

    //options
            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                text: " Top Customer",
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#333",
                  fontSize: 16
                }
              },
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            var chart = new Chart(ctx, {
              type: "pie",
              data: data,
              options: options
            });

          });
          },

       render_top_product_graph:function(){
         var self = this
          var ctx = self.$(".top_selling_product");
              rpc.query({
                  model: "pos.order",
                  method: "get_the_top_products",
              }).then(function (arrays) {


            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: "Quantity",
                  data: arrays[0],
                  backgroundColor: [
                    "rgba(255, 99, 132,1)",
                    "rgba(54, 162, 235,1)",
                    "rgba(75, 192, 192,1)",
                    "rgba(153, 102, 255,1)",
                    "rgba(10,20,30,1)"
                  ],
                  borderColor: [
                   "rgba(255, 99, 132, 0.2)",
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(10,20,30,0.3)"
                  ],
                  borderWidth: 1
                },

              ]
            };

    //options
            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                text: " Top products",
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#333",
                  fontSize: 16
                }
              },
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            var chart = new Chart(ctx, {
              type: "horizontalBar",
              data: data,
              options: options
            });

          });
          },

       render_product_category_graph:function(){
             var self = this
          var ctx = self.$(".top_product_categories");
              rpc.query({
                  model: "pos.order",
                  method: "get_the_top_categories",
              }).then(function (arrays) {


            var data = {
              labels: arrays[1],
              datasets: [
                {
                  label: "Quantity",
                  data: arrays[0],
                  backgroundColor: [
                    "rgba(255, 99, 132,1)",
                    "rgba(54, 162, 235,1)",
                    "rgba(75, 192, 192,1)",
                    "rgba(153, 102, 255,1)",
                    "rgba(10,20,30,1)"
                  ],
                  borderColor: [
                   "rgba(255, 99, 132, 0.2)",
                    "rgba(54, 162, 235, 0.2)",
                    "rgba(75, 192, 192, 0.2)",
                    "rgba(153, 102, 255, 0.2)",
                    "rgba(10,20,30,0.3)"
                  ],
                  borderWidth: 1
                },


              ]
            };

    //options
            var options = {
              responsive: true,
              title: {
                display: true,
                position: "top",
                text: " Top product categories",
                fontSize: 18,
                fontColor: "#111"
              },
              legend: {
                display: true,
                position: "bottom",
                labels: {
                  fontColor: "#333",
                  fontSize: 16
                }
              },
              scales: {
                yAxes: [{
                  ticks: {
                    min: 0
                  }
                }]
              }
            };

            //create Chart class object
            var chart = new Chart(ctx, {
              type: "horizontalBar",
              data: data,
              options: options
            });

          });
          },
  });


  core.action_registry.add('pos_dashboard', PosDashboard);

  return PosDashboard;

});

