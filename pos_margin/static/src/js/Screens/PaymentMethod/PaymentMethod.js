odoo.define('pos_magnify_image.PaymentMethod', function (require) {
    "use strict";

    const { useState } = owl.hooks;
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const ClientListScreen = require('point_of_sale.ClientListScreen');
    
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const Ajax = require('web.ajax');

    const data_json = [];

    const PaymentMethod = ClientListScreen =>
        class extends ClientListScreen { 

            async ncfTxt() {

              var list = []
              var num_ncf = $($(document).find("#num_ncf"))[0].value;
              if (data_json.length > 0) {
                for (var i = 0; i < data_json.length; i++) {
                  if (data_json[i].state == 'ACTIVO') {
                    if (data_json[i].ncf == num_ncf) {
                      list.push(data_json[i])

                    }
                  }
                }
                
                if (list.length > 0) {
                  var inputName = $($(document).find("input.detail.client-name"))[0].value = list[0].name;
                  var inputVat = $($(document).find("input.detail.vat"))[0].value = list[0].ncf;
                  $($(document).find("input.detail.client-name"))[0].focus()

                  
                }else{
                  alert("Numero de Comprovante no Existe")
                }
                
              }else{
                var XMLReq = new XMLHttpRequest();
                XMLReq.open( "GET", "https://raw.githubusercontent.com/sistemasedy/api_ncf/main/DGII_RNC/TMP/DGII_RNC.TXT", false )

                XMLReq.onreadystatechange = function() {
                  if(XMLReq.readyState == 4 && XMLReq.status == 200) {

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
                    
                    if (list.length > 0) {
                      var inputName = $($(document).find("input.detail.client-name"))[0].value = list[0].name;
                      var inputVat = $($(document).find("input.detail.vat"))[0].value = list[0].ncf;
                      $($(document).find("input.detail.client-name"))[0].focus()
                      
                    }else{
                      alert("Numero de Comprovante no Existe")
                    }                   

                    
                  }
                }

                XMLReq.send();

              }
              if (true) {
                //var inputSearch = $($(document).find("div.searchbox-client.top-content-center"))[0].value = list[0].name;
                console.log($($(document).find("div.searchbox-client.top-content-center")))
                console.log($($(document).find("input.detail.vat"))[0].value)
                  
              }     
            }

            provar(){
              console.log("null")
            }


  

         
        }
    Registries.Component.extend(ClientListScreen, PaymentMethod);
    return PaymentMethod;
});