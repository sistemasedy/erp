// Model and View for Entity
const listWarehouse = JSON.parse(localStorage.getItem("Inven"))
const listWarehouses = JSON.parse(localStorage.getItem("Warehouse"))
const fragment = document.createDocumentFragment();
const formCreate = document.querySelector('#form-create')
const listing = document.querySelector('#listing')
const editing = document.querySelector('#tableProduct')
const editings = document.querySelector('#editing')

const templateShowWarehouse = document.querySelector('#template-show-warehouse').content
const showWarehouse = document.querySelector('#show-warehouse')
const editWarehouseGeneral = document.querySelector('#edit-warehouse')
const templateEditWarehouse = document.querySelector('#template-edit-warehouse').content

const openModal = document.querySelector('#btn-open-modal')
const containerModal = document.querySelector('#modal-fuel')
const containerModalDanger = document.querySelector('#modal-fuel-danger')
const closeUno = document.querySelector('#close-x')

document.addEventListener('DOMContentLoaded', () => {
  const model = new InventoryModel()
  const view = new InventoryView()

  model.setView(view)
  view.setModel(model)

  view.render()
  view.search()
})

class InventoryModel {
    constructor() {
        this.view = null
        this.listWarehouse = listWarehouse
        this.addWarehouseForm = new AddWarehouse()
        if (!this.listWarehouse || this.listWarehouse.length < 1) {
            console.log("no data")
            this.addWarehouseForm.onClick((address, pathner, name, num) => this.addWarehouse(address, pathner, name, num))
        }   

    }

    setView(view) {
        this.view = view

    }
    save() {
        //localStorage.setItem('Warehouse', JSON.stringify(this.listWarehouse))
        localStorage.setItem('Inven', JSON.stringify(this.listWarehouse))

    }

    getWarehouse() {
        return listWarehouse.map((warehouse) => ({...warehouse}))

    }

    findWarehouse(id) {
        return listWarehouse.findIndex((warehouse) => warehouse.id == id)

    }

    stateWarehouse(id) {
        const index = this.findWarehouse(id)
        const warehouse = this.listWarehouse[index]
        warehouse.state = "ok"
        this.save()

    }

    editWarehouse(id, values) {
        const index = this.findWarehouse(id)
        Object.assign(this.listWarehouse[index], values)
        this.save()

    }

    //algo especial por el detalle de inv..
   /* addWarehouse(warehouse, pathner, amont, difference) {
        let conut_id = 0
        if (this.listProduct) {
            conut_id = parseInt(this.listProduct.length) + 1
        }else{
            conut_id = 1
        }
        let dates = new Date()
        let month = dates.getMonth()
        const warehouse = {
            ids: conut_id,
            id: Date.now(),
            warehouse,
            pathner,
            amont,
            difference,
            date: month,
            date_time: dates,
            state: "draf",
        }
        if (this.listWarehouse) {
            this.listWarehouse.push(warehouse)
            this.save()
        }else{
            localStorage.setItem('Inven', JSON.stringify([warehouse]))
        }
        return {...warehouse}

    }*/

    addWarehouse(warehouses, pathner, amont, difference) {
        let conut_id = 0
        if (this.listProduct) {
            conut_id = parseInt(this.listProduct.length) + 1
        }else{
            conut_id = 1
        }
        let dates = new Date()
        let month = dates.getMonth()
        const warehouse = {
            ids: conut_id,
            id: Date.now(),
            warehouses,
            pathner,
            amont,
            difference,
            date: month,
            date_time: dates,
            state: "draf",
        }
        if (this.listWarehouse) {
            this.listWarehouse.push(warehouse)
            this.save()
        }else{
            localStorage.setItem('Inven', JSON.stringify([warehouse]))
        }
        return {...warehouse}

    }

    /*addWarehouse2(address, partner, name, num) {
        let date = new Date()
        let month = date.getMonth()
        const Warehouse = {
            id: Date.now(),
            ids,
            month: month,
            date_time: date,
            state: "draf",
            id_address,
            ids_detail,
            partner,
            total_pa,
            total_na,
            total_num,
            
        }
        if (this.listWarehouse) {
            this.listWarehouse.push(Warehouse)
            this.save()
        }else{
            localStorage.setItem('Warehouse', JSON.stringify([Warehouse]))
        }
        return {...Warehouse}

    }*/

    // if state draf ok delete
    removeWarehouse(id) {
        const index = this.findWarehouse(id)
        listWarehouse.splice(index, 1)
        this.save()

    }

    /*addDetailWarehouse(address, pathner, name, num) {
        let fecha = new Date()
        let month = fecha.getMonth()
        const detail = {
            id: Date.now(),
            ids,
            id_Warehouse,
            ids_product,
            active,
            c1_inch_month_1,
            c1_inch_month_2,
            c1_gallons,
            c2_inch_month_1,
            c2_inch_month_2,
            c2_gallons,
            c3_inch_month_1,
            c3_inch_month_2,
            c3_gallons,
            c4_inch_month_1,
            c4_inch_month_2,
            c4_gallons,
            c5_inch_month_1,
            c5_inch_month_2,
            c5_gallons,
            c6_inch_month_1,
            c6_inch_month_2,
            c6_gallons,
            total,
            stocks,
            num,
            price,            
            name,
        }
        if (this.listWarehouse) {
            this.listWarehouse.push(Warehouse)
            this.save()
        }else{
            localStorage.setItem('Warehouse', JSON.stringify([Warehouse]))
        }
        return {...Warehouse}

    }*/



}

class InventoryView {
    constructor() {
        this.model = null
        this.templateWarehouse = document.querySelector('#list-warehouse').content
        this.listsWarehouse = document.querySelector('#tableProduct')
        this.btn = document.getElementById("tbn-form-create")
        this.btnRemove = document.getElementById("btn-delete")
        this.inputSearch = document.querySelector('#navbar-search-input')
        //this.btnDelete = document.getElementById("btn-delete")
        this.addWarehouseForm = new AddWarehouse()
        this.addWarehouseForm.onClick((address, pathner, name, num) => this.addWarehouse(address, pathner, name, num))
        this.teste()
    }


    search() {
        this.inputSearch.onkeyup = () => {
            this.filtros2(this.inputSearch.value)


        }
    }


    filtros2(val) {
        let misDatos = []
        for (let i = 0; i< listWarehouse.length; i++) {
            var todo = listWarehouse[i]
            var curreNname = listWarehouse[i].address
            if (curreNname.toLowerCase().indexOf(val.toLowerCase()) > -1) {
                misDatos.push(todo)
            }
        }
        this.createRow(misDatos)
        console.log(misDatos)
    }

    setModel(model) {
        this.model = model
    }

    teste(){
        console.log(this.model)
    }

    render() {
        const warehouse = this.model.getWarehouse()
        this.createRow(warehouse)
        

    }
    removeWarehouse(id) {
        //this.model.removeWarehouse(id)
        console.log(id)
        this.render()
    }

    

    createRow(warehouse) {
        
        this.listsWarehouse.innerHTML = "";
        let te = document.querySelector('#testt')
        
        let btnRemo = document.createElement('button')
        btnRemo.classList.add('btn', 'btn-danger', 'mb-1', 'ml-1')
        const btn = document.querySelectorAll('.btn-danger')
        
        
        //te.appendChild(btnRemo)
        
        Object.values(warehouse).forEach(item =>{
            
            this.templateWarehouse.querySelector('a').textContent = item.id
            this.templateWarehouse.querySelectorAll('td')[1].textContent = item.warehouses
            this.templateWarehouse.querySelectorAll('td')[2].textContent = item.pathner
            this.templateWarehouse.querySelectorAll('td')[3].textContent = item.amont
            //this.templateWarehouse.querySelectorAll('td')[4].appendChild(btnRemo)
            
            this.templateWarehouse.querySelector('.btn-box-tool-1').dataset.id = item.id
            this.templateWarehouse.querySelector('.link').dataset.id = item.id
            const clone = this.templateWarehouse.cloneNode(true)

            fragment.appendChild(clone)

        })
        this.listsWarehouse.appendChild(fragment)
    }

    createOptionWarehouse(warehouse) {
        let select = document.querySelector('#warehouse')
        select.innerHTML = "";      
        let option = document.createElement('option')
        Object.values(warehouse).forEach(item =>{           
            option.textContent = item.name + " " + item.num
            option.value = item.id
            const clone = option.cloneNode(true)
            fragment.appendChild(clone)
        })
        select.appendChild(fragment)
    }

    addWarehouse(address, pathner, name, num) {
        const warehouse = this.model.addWarehouse(address, pathner, name, num)
        console.log(warehouse)
        console.log(this.model)
        this.render()
    }

    showModal() {
        let modal = document.getElementById("mod")
         modal.classList.add('example-modal')

    }

    closeModal() {
        console.log("test")
        let modal = document.getElementById("mod")
         modal.classList.remove('example-modal')
    }

    closeModals() {
         console.log(containerModal)
         console.log(containerModal.classList)
         containerModal.classList.remove('example-modal')
         containerModal.classList.add('example-modal2')
    }


}


class AddWarehouse {
    constructor(){
        this.btnCreate = document.getElementById("btnCreate"); //$("#alm").val();
        this.address = document.getElementById("address"); //$("#alm").val();
        this.pathner = document.getElementById("pathner"); //$("#despachador").val();
        this.name = document.getElementById("name"); //$("#total").val();
        this.num = document.getElementById("num"); //$("#diferencia").val();
        //this.date = document.getElementById("date").value; //$("#fechas").val();
    }

    onClick(callback) {
        this.btnCreate.onclick = () => {
            //callback(this.address, this.pathner, this.name, this.num)
            if (this.address.value === '' || this.pathner.value === '') {
                alert("Los Campos Estan  Vacio")
            }else{
                callback(this.address.value, this.pathner.value, this.name.value, this.num.value)
            }
            //console.log(this.address)
            
        }

    }
}


openModal.addEventListener('click', e => {
     containerModal.style.opacity = "1"
     containerModal.style.visibility = "visible"
     containerModalDanger.classList.toggle("modal-close")
     //containerModal.classList.add('modal-close') 
     //let view = new InventoryView()
     //view.closeModals()

})
closeUno.addEventListener('click', e => {
     containerModalDanger.classList.toggle("modal-close")
     
     setTimeout(function(){
        containerModal.style.opacity = "0"
        containerModal.style.visibility = "hidden"

     },900)

})

window.addEventListener('click', e => {
    if (e.target == containerModal) {

        containerModalDanger.classList.toggle("modal-close")
     
     setTimeout(function(){
        containerModal.style.opacity = "0"
        containerModal.style.visibility = "hidden"

     },900)

    }
})


listing.addEventListener('click', e => {
  if (e.target.classList.contains('btn-box-tool')) {
    let date = document.querySelector('#date-create')

        listing.style.display = 'none'
        formCreate.style.display = 'block'
        let dates = new Date()
        date.value = dates
  }

  
  if (e.target.classList.contains('link')) {
        listing.style.display = 'none'
        editings.style.display = 'block'

        showWarehouse.innerHTML = "";
        for( var i = 0; i < listWarehouse.length; i++){
            if (listWarehouse[i].id == e.target.dataset.id) {
                var inv = listWarehouse[i];
            }
        }
        templateShowWarehouse.querySelector('input').value = inv.id
        templateShowWarehouse.querySelectorAll('span')[0].textContent = inv.id
        templateShowWarehouse.querySelectorAll('span')[1].textContent = inv.address
        templateShowWarehouse.querySelectorAll('span')[2].textContent = inv.name
        const clone = templateShowWarehouse.cloneNode(true)
        fragment.appendChild(clone)
        showWarehouse.appendChild(fragment)
  }

  if (e.target.classList.contains('btn-box-tool-1')) {
        let remove = new WarehouseModel()
        remove.removeWarehouse(e.target.dataset.id)
        location.reload()

  }

  if (e.target.classList.contains('btn-default')) {
        listing.style.display = 'none'
        editings.style.display = 'block'

        let ids = document.querySelector('#id-editing').value

        showWarehouse.innerHTML = "";
        for( var i = 0; i < listWarehouse.length; i++){
            if (listWarehouse[i].id == ids) {
                var inv = listWarehouse[i];
            }
        }
        templateEditWarehouse.querySelectorAll('input')[0].textContent = inv.id
        templateEditWarehouse.querySelectorAll('input')[1].textContent = inv.address
        templateEditWarehouse.querySelectorAll('input')[2].textContent = inv.name
        const clone = templateEditWarehouse.cloneNode(true)
        fragment.appendChild(clone)
        showWarehouse.appendChild(fragment)
  }

})

editings.addEventListener('click', e => {
  if (e.target.classList.contains('btn-success')) {
        listing.style.display = 'none'
        editings.style.display = 'block'

        let test = new InventoryView()
        test.hola()

        let ids = document.querySelector('#id-editing').value

        showInventory.innerHTML = "";
        for( var i = 0; i < listInventory.length; i++){
            if (listInventory[i].id == ids) {
                var inv = listInventory[i];
            }
        }
        templateEditInventory.querySelectorAll('input')[0].value = inv.id
        templateEditInventory.querySelectorAll('input')[1].value = inv.warehouse
        templateEditInventory.querySelectorAll('input')[2].value = inv.amont
        const clone = templateEditInventory.cloneNode(true)
        fragment.appendChild(clone)
        showInventory.appendChild(fragment)
  }

  if (e.target.classList.contains('btn-primary')) {
        id = showInventory.querySelectorAll('input')[0].value
        warehouse = showInventory.querySelectorAll('input')[1].value
        amont = showInventory.querySelectorAll('input')[2].value
        //console.log(id)
        let values = {
            warehouse: warehouse,
            amont: amont
        }
        let index = listInventory.findIndex((inventory) => inventory.id == id)
        //console.log(index)
        Object.assign(listInventory[index], values)
        localStorage.setItem('Inventory', JSON.stringify(listInventory))

        listing.style.display = 'none'
        editings.style.display = 'block'

        showInventory.innerHTML = "";
        for( var i = 0; i < listInventory.length; i++){
            if (listInventory[i].id == id) {
                var inv = listInventory[i];
            }
        }
        templateShowInventory.querySelector('input').value = inv.id
        templateShowInventory.querySelectorAll('span')[0].textContent = inv.id
        templateShowInventory.querySelectorAll('span')[1].textContent = inv.warehouse
        templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
        const clone = templateShowInventory.cloneNode(true)
        fragment.appendChild(clone)
        showInventory.appendChild(fragment)
  }

})

formCreate.addEventListener('click', e => {

  if (e.target.classList.contains('btn-default')) {
    listing.style.display = 'block'
    formCreate.style.display = 'none'


  }

  /*if (e.target.classList.contains('btn-success')) {
    listing.style.display = 'none'
    formCreate.style.display = 'block'
    let modal = new InventoryView()
    modal.showModal()


  }*/

  if (e.target.classList.contains('btn-outline')) {
    listing.style.display = 'none'
    formCreate.style.display = 'block'
    let modal = new InventoryView()
    modal.closeModal()
  } 

})








/*class RemoveWarehouse {
    constructor(){
        this.templateWarehouse = document.querySelector('#list-Warehouse')
        this.listsWarehouse = document.querySelector('#tableProduct')
        this.tr = this.listsWarehouse.querySelectorAll('.btn-box-tool-1')
        this.btnRemoves = document.getElementById("btn-deletes")
        this.btnRemove = document.querySelector('#btn-delete')
        this.btnCreate = document.getElementById("btnCreate")
    }


    onClick(callback) {
        this.tr.onClick = () => {
            console.log("test")
        }
        this.btnRemoves.onclick = () => {
            console.log(this.tr)
            console.log(this.listsWarehouse)
        }
        

    }
}

class EditWarehouse {
    constructor(){
        this.btnEdit = document.getElementById("btn-edit"); //$("#alm").val();
        this.address = document.getElementById("address-edit"); //$("#alm").val();
        this.id = document.getElementById("id-editing"); //$("#despachador").val();
        this.name = document.getElementById("name-edit"); //$("#total").val();
        //this.num = document.getElementById("num"); //$("#diferencia").val();
        //this.date = document.getElementById("date").value; //$("#fechas").val();
    }

    onClick(callback) {
        this.btnEdit.onclick = () => {
            const Warehouse = {
                address: this.address,
                name: this.name,
            }
                callback(this.id.value, Warehouse)
            
        }

    }
}*/

