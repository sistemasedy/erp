class Inventarios {
    constructor(nombre) {
        this.ProductosList = localStorage.getItem(this.nombre);
        this.nombre = nombre;
        this.almacen = document.getElementById("almacentxt").value;
        this.notas = document.getElementById("notastxt").value;
        this.totalPA = document.getElementById("totalpatxt").value;
        this.totalNA = document.getElementById("totalnatxt").value;
        this.diferencia = document.getElementById("diferenciatxt").value;
        //this.articulos = [];
        
    }

    base(){
        localStorage.setItem(this.nombre, JSON.stringify([{
            'almacen': this.almacen,
            'notas': this.notas,
            'totalpa': this.totalPA,
            'totalna': this.totalNA,
            'diferencia': this.diferencia,
        }]));
    }

    add(){
        var ProductosList = localStorage.getItem(this.nombre);
        if (ProductosList) {
            var ListProduct = JSON.parse(ProductosList);
            ListProduct.push([{
                'almacen': this.almacen,
                'notas': this.notas,
                'totalpa': this.totalPA,
                'totalna': this.totalNA,
                'diferencia': this.diferencia,
            }]);
            localStorage.setItem(this.nombre, JSON.stringify(ListProduct));
        }else{
            this.base();
        }
        this.clear();
    }

    clear(){
        document.getElementById("almacentxt").value = "";
        document.getElementById("notastxt").value = "";
        document.getElementById("totalpatxt").value = "";
        document.getElementById("totalnatxt").value = "";
        document.getElementById("diferenciatxt").value = "";
    }

    get(){
        var ProductosList = localStorage.getItem(this.nombre);
        var ListProduct = JSON.parse(ProductosList);
        var ListProducts = ListProduct[2];
        var container = document.getElementById("product");

        var containers = document.getElementById("products");
        containers.innerHTML = "";
        alert("datos" + " "+ ListProduct.length)

        for (var i = 0; i < ListProduct.length; i++) {
            containers.innerHTML += '<ul class="todo-list">\
                                      <li>\
                                            <span class="handle">\
                                              <i class="fa fa-ellipsis-v"></i>\
                                              <i class="fa fa-ellipsis-v"></i>\
                                            </span>\
                                        <input type="checkbox" value="">\
                                        <span class="text">'+ ListProducts[i].almacen +'</span>\
                                        <small class="label label-danger"><i class="fa fa-clock-o"></i> 2 mins</small>\
                                        <div class="tools">\
                                          <i class="fa fa-edit"></i>\
                                          <i class="fa fa-trash-o"></i>\
                                        </div>\
                                      </li>\
                                    </ul>'; 
        }

    }
}

function general(){
    var fech = new Date(2011,   1  ,    29);
    //var nombre = new fech.getMonth();
    var inicial = new Inventarios("conteo");
    inicial.add();
    inicial.get();

}



