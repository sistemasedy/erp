
function tes(){
    
    
    var containers = document.getElementById("createInventoryHeader");
    containers.innerHTML = "";
    containers.innerHTML = '<div class="col-xs-10 text-center">\
                              <h2 class="page-header">\
                                <div class="col-md-6">\
                                  <div class="form-group">\
                                    <label>ALMACEN</label>\
                                    <select class="form-control select2" style="width: 100%;">\
                                      <option id="alm" selected="selected">Alabama</option>\
                                      <option id="alm1">Alaska</option>\
                                      <option>California</option>\
                                      <option>Delaware</option>\
                                      <option>Tennessee</option>\
                                      <option>Texas</option>\
                                      <option>Washington</option>\
                                    </select>\
                                  </div>\
                                </div>\
                              </h2>\
                            </div>\
                            <small class="pull-right">Date: 2/10/2014</small>';

    var fecha = document.getElementById("fecha");
    var date = Date()

    fecha.innerHTML = '<input id="fechas" value="'+ date +'" type="text" class="form-control">';

}




function deletInventory(almacen){
    console.log(almacen);
    var inventarios = JSON.parse(localStorage.getItem('Inventarios'));
    console.log(inventarios.length);
    for( var i = 0; i < inventarios.length; i++){

        if (inventarios[i].total == almacen) {
            inventarios.splice(i, 1);
        }
    }

    localStorage.setItem('Inventarios', JSON.stringify(inventarios));
    getListInventory();


}



function mainListInventory(){
    tes();

}


function saveInventory(){

    var almacen = document.getElementById("alm").value; //$("#alm").val();
    var despachador = document.getElementById("despachador").value; //$("#despachador").val();
    var total = document.getElementById("total").value; //$("#total").val();
    var diferencia = document.getElementById("diferencia").value; //$("#diferencia").val();
    var fecha = document.getElementById("fechas").value; //$("#fechas").val();

   

    if (localStorage.getItem('Inventarios') === null) {
        localStorage.setItem('Inventarios', JSON.stringify([{
            'id': '1',
            'almacen': almacen,
            'despachador': despachador,
            'total': total,
            'diferencia': diferencia,
            'fecha': fecha,
        }]));
    }else{
        var inventarios = JSON.parse(localStorage.getItem('Inventarios'));
        
        var id = parseInt(inventarios.length) + 1
        inventarios.push({
            'id': id,
            'almacen': almacen,
            'despachador': despachador,
            'total': total,
            'diferencia': diferencia,
            'fecha': fecha,
        });
        localStorage.setItem('Inventarios', JSON.stringify(inventarios));
    }

}