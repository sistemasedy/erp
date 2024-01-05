odoo.define('pos_l10n_ar_identification.screens', function(require) {
    'use strict';

    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');
    const { useListener } = require('web.custom_hooks');
    
    const Ajax = require('web.ajax');

    const data_json = [];

    

    const POSSaveClientOverride = ClientListScreen =>
        class extends ClientListScreen {
            /**
             * @override
             */

             constructor() {
                super(...arguments);
                useListener('click-fiscal', () => this.clickFiscal());
            }


            clickFiscal() {
                var self = this;
                this.fiscalChanges();
                //this.saveChanges();
           }

           async hola() {

              var list = []
                console.log('hola fiscal')  
            }

           async fiscalChanges() {

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
                  await this.showPopup('OfflineErrorPopup', {
                        title: this.env._t('Offline'),
                        body: this.env._t('Numero de Comprovante no Existe'),
                    });
                  //alert("Numero de Comprovante no Existe")
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

            async saveChanges(event) {
              var num_ncf = $($(document).find("#num_ncf"))[0].value;

              if (num_ncf) {
                console.log("el dato es", num_ncf)
              }else{
                console.log("no hay")
              }

                try{
                    let partnerId = await this.rpc({
                        model: 'res.partner',
                        method: 'create_from_ui',
                        args: [event.detail.processedChanges],
                    });
                    await this.env.pos.load_new_partners();
                    this.state.selectedClient = this.env.pos.db.get_partner_by_id(partnerId);
                    this.state.detailIsShown = false;
                    this.render();

                }catch (error){
                    if (error.message.code < 0) {
                        await this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Offline'),
                            body: this.env._t('Unable to save changes.'),
                        });
                    } else {
                        throw error;
                    }
                }

            }

            

        };

    Registries.Component.extend(ClientListScreen, POSSaveClientOverride);

    return ClientListScreen;
});