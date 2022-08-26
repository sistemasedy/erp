const listInventory = JSON.parse(localStorage.getItem("Inventarios"))
const templateInventory = document.querySelector('#list-inventory').content
const fragment = document.createDocumentFragment();
const listsInventory = document.querySelector('#tableProduct')

document.addEventListener('DOMContentLoaded', () => {
  getListInventory();

})

listsInventory.addEventListener('click', e => {
  deleInventory(e)
})


function fecha(){
  let fecha = new Date()
    let mes = fecha.getMonth()
    console.log(mes)
    console.log(fecha)
}



function getListInventory2(){
    var ProductosList = localStorage.getItem("Inventarios");
    var ListProducts = JSON.parse(ProductosList);
    //var ListProducts = ListProduct[1];
    var containers = document.getElementById("tableProduct");
    containers.innerHTML = "";

    for (var i = 0; i < ListProducts.length; i++) {
        containers.innerHTML += '<tr>\
                                  <td><a onclick="saveToken('+ListProducts[i].total+')" href="editInventory.html">'+ListProducts[i].almacen+'</a></td>\
                                  <td>'+ListProducts[i].total+'</td>\
                                  <td>'+ListProducts[i].despachador+'</td>\
                                  <td><button type="button" onclick="deletInventory('+ListProducts[i].total+')" class="btn btn-box-tool" >Eliminar</button></td>\
                                </tr>';
    }
}





function getListInventory(){
  listsInventory.innerHTML = "";
  Object.values(listInventory).forEach(item =>{
    templateInventory.querySelectorAll('td')[0].textContent = item.almacen
    templateInventory.querySelectorAll('td')[1].textContent = item.id
    templateInventory.querySelectorAll('td')[2].textContent = item.despachador
    templateInventory.querySelectorAll('td')[3].textContent = item.total
    templateInventory.querySelector('.btn-box-tool').dataset.id = item.id
    const clone = templateInventory.cloneNode(true)
    fragment.appendChild(clone)
  })
  listsInventory.appendChild(fragment)



}

const deleInventory = e => {
  if (e.target.classList.contains('btn-box-tool')) {
    for( var i = 0; i < listInventory.length; i++){
      if (listInventory[i].id == e.target.dataset.id) {
        //delete listInventory[e.target.dataset.id]
        listInventory.splice(i, 1);
      }

    }
    localStorage.setItem('Inventarios', JSON.stringify(listInventory));
    getListInventory();

  }
}





function deletInventory(almacen){
    console.log(almacen);
    var inventarios = JSON.parse(localStorage.getItem('Inventarios'));
    console.log(inventarios.length);
    for( var i = 0; i < inventarios.length; i++){

        if (inventarios[i].id == almacen) {
            inventarios.splice(i, 1);
        }
    }

    localStorage.setItem('Inventarios', JSON.stringify(inventarios));
    getListInventory();


}







































function saveToken(token){
  localStorage.setItem('Tokens', JSON.stringify([{
          'id': '2',
          'token': token,
      }]));

}



function getList(){
    var ProductosList = localStorage.getItem("conteo");
    var ListProduct = JSON.parse(ProductosList);
    var ListProducts = ListProduct[1];
    var containers = document.getElementById("tableProduct");
    containers.innerHTML = "";

    for (var i = 0; i < ListProduct.length; i++) {
        containers.innerHTML += '<tr>\
                                  <td>'+ListProducts[i].gas1+'</td>\
                                  <td>'+ListProducts[i].gas1+'</td>\
                                  <td>'+ListProducts[i].gas1+'</td>\
                                  <td>'+ListProducts[i].gas1+'</td>\
                                  <td>'+ListProducts[i].gas1+'</td>\
                                </tr>';
    }
}





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