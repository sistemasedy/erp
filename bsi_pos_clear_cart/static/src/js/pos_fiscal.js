odoo.define('pos_l10n_ar_identification.screens', function(require) {
    'use strict';

    const ClientListScreen = require('point_of_sale.ClientListScreen');
    var rpc = require('web.rpc')
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
                console.log("inicio", this.listTipos())
                
            }


            async listTipos() {
                let lista = await this.rpc({
                    model: 'res.partner',
                    method: '_get_l10n_do_dgii_payer_types_selection'
                });

                return lista
            }


            


            clickFiscal() {
                var self = this;
                console.log("test", this.env.pos.l10n_do_dgii_tax_payer_type)
                console.log("test2", this.env.pos)
                this.fiscalChanges();
                //this.saveChanges();
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
                XMLReq.open( "GET", "https://raw.githubusercontent.com/sistemasedy/api_ncf/main/DGII_RNC/TMP/DGII_RNC2.TXT", false )

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



            async fiscalSave() {

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
                  var inputName = list[0].name;
                  var inputVat = list[0].ncf;

                  event.detail.processedChanges.name = inputName
                  event.detail.processedChanges.vat = inputVat

                  
                }
                
              }
                  
            }

            async saveChanges(event) {
                var num_ncf = $($(document).find("#num_ncf"))[0].value;

                if (num_ncf) {
                  this.fiscalSave();
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

                //this.state.selectedClient = this.env.pos.db.get_partner_by_id(event.detail.processedChanges.id);

            }

            

        };

    Registries.Component.extend(ClientListScreen, POSSaveClientOverride);

    return ClientListScreen;
});