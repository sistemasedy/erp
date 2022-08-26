odoo.define('pos_margin.ProductSearch', function(require) {
    'use strict';

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const Ajax = require('web.ajax');

    const data_json = []


    class ProductSearch extends PosComponent {
           constructor() {
               super(...arguments);
               //useListener('click', this.onClickDir);

           }

           

           get searchWord() {
                return this.state.searchWord.trim();
            }

           get currentOrder() {
                return this.env.pos.get_order();
            }

           onClickDir() {
                console.log("file")
                //$($(document).find("div.search-box input")).focus()
            }


           async provarPad(){
              var list = []
              var list2 = []
              var num_ncf = '101071397'


              if (data_json.length > 0) {
                console.log("ya tenemos datos")
                for (var i = 0; i < data_json.length; i++) {
                  if (data_json[i].state == 'ACTIVO') {
                    if (data_json[i].ncf == num_ncf) {
                      list.push(data_json[i])

                    }
                  }
                }

                for (var i = 0; i < data_json.length; i++) {
                  if (data_json[i].state == 'ACTIVO') {
                    if (data_json[i].ncf == '101070803') {
                      list2.push(data_json[i])

                    }
                  }
                }


                if (list2.length == 0) {
                  console.log("que considencia")
                  console.log("es inde", list2)
                }else{
                  console.log("es inde", list2)
                }
                
                if (list.length > 0) {
                  console.log(list[0].name, list[0].ncf, list[0].state)
                }else{
                  console.log("not resul")
                }
                
              }else{
                var XMLReq = new XMLHttpRequest();
                XMLReq.open( "GET", "https://raw.githubusercontent.com/sistemasedy/api_ncf/main/DGII_RNC/TMP/DGII_RNC.TXT", false )

                XMLReq.onreadystatechange = function() {
                  if(XMLReq.readyState == 4 && XMLReq.status == 200) {
                    console.log("esperando respuesta")

                    var lines = XMLReq.responseText.split("\n");
                    //var data_json = [];
                    var tmp;
                    for(var index in lines){
                      tmp = lines[index].trim().split("|");
                      data_json.push({
                        ncf : tmp[0],
                        name : tmp[1],
                        state : tmp[9]
                      });
                    }

                    

                    for (var i = 0; i < data_json.length; i++) {
                      if (data_json[i].state == 'ACTIVO') {
                        if (data_json[i].ncf == num_ncf) {
                          list.push(data_json[i])

                        }
                      }
                    }

                    for (var i = 0; i < data_json.length; i++) {
                      if (data_json[i].state == 'ACTIVO') {
                        if (data_json[i].ncf == '101070803') {
                          list2.push(data_json[i])

                        }
                      }
                    }


                    if (list2.length == 0) {
                      console.log("que considencia")
                      console.log("es inde", list2)
                    }else{
                      console.log("es inde", list2)
                    }
                    
                    if (list.length > 0) {
                      console.log(list[0].name, list[0].ncf, list[0].state)
                    }else{
                      console.log("not resul")
                    }
                  }
                }

                XMLReq.send();

              }


           }
       }

   ProductSearch.template = 'ProductSearch';
   ProductScreen.addControlButton({
       component: ProductSearch,
       condition: function() {
           return this.env.pos;
       },
   });
    

    Registries.Component.add(ProductSearch);

    return ProductSearch;
});

