function mainListInventory(){
    //showInventory()
    editInventory();



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






function showInventory(){
    var inventarios = JSON.parse(localStorage.getItem('Inventarios'));
    if (inventarios) {
        document.getElementById("editInventory").style.display = "none";
        
    }else{
        document.getElementById("viewInventory").style.display = "none";

    }
    
}

function editInventory(){
    //document.getElementById("viewInventory").style.display = "block";
    document.getElementById("editInventory").style.display = "none";
    var TokenList = localStorage.getItem("Tokens");
    var ListToken = JSON.parse(TokenList);
    var token = ListToken[0].token
    var inventarios = JSON.parse(localStorage.getItem('Inventarios'));
    
    for( var i = 0; i < inventarios.length; i++){
        if (inventarios[i].total == token) {
            var inv = inventarios[i];
        }
    }
    var info = document.getElementById("infoInventory");
    info.innerHTML = "";
    info.innerHTML = '<b>Almacen:'+ inv.almacen +'</b><br>\
                      <br>\
                      <b>Order ID:</b> 4F3S8J<br>\
                      <b>Despachador:</b>'+inv.despachador+'<br>\
                      <b>Account:</b> 968-34567';

    var info1 = document.getElementById("infoInventory1");
    info1.innerHTML = "";
    info1.innerHTML = '<b>Total $'+ inv.total +'</b><br>\
                      <br>\
                      <b>Order ID:</b> 4F3S8J<br>\
                      <b>Diferencia:</b>'+inv.diferencia+'<br>\
                      <b>Account:</b> 968-34567';

    var info2 = document.getElementById("infoInventory2");
    info2.innerHTML = "";
    info2.innerHTML = '<b>Num #'+ inv.id +'</b><br>\
                      <br>\
                      <b>Order ID:</b> 4F3S8J<br>\
                      <b>Date:</b>'+inv.fecha+'<br>\
                      <b>Account:</b> 968-34567';

    var containers = document.getElementById("editInventoryHeader");
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



function getToken(){
    var TokenList = localStorage.getItem("Tokens");
    var ListToken = JSON.parse(TokenList);
    alert("es es tu token" + " "+ ListToken[0].token);
}