// Model and View for Entity
const listInventory = JSON.parse(localStorage.getItem("TableCalc"))
const listWarehouse = JSON.parse(localStorage.getItem("Warehouse"))
const listProduct = JSON.parse(localStorage.getItem("Products"))
const fragment = document.createDocumentFragment();
const formCreate = document.querySelector('#form-create')
const listing = document.querySelector('#listing')
const editing = document.querySelector('#tableProduct')
const editings = document.querySelector('#editing')

const templateShowInventory = document.querySelector('#template-show-inventory').content
const showInventory = document.querySelector('#show-inventory')
const editInventoryGeneral = document.querySelector('#edit-inventory')
const templateEditInventory = document.querySelector('#template-edit-inventory').content

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
    console.log(rango)
    //Containers()
    
})


const numero = [1,2,3,4,5,6]

const numerosPorDos = listInventory.filter((item) => item.amont == 200 )

const rango =  "range(1, 6)"








/*const datos = e => {
	console.log("data")
  
}*/

/*document.addEventListener('keyup', () => {
	//console.log(event.which)
	if (event.which == 17 || event.which == 18) {
		let date = document.querySelector('#date-create')

	    listing.style.display = 'none'
	    formCreate.style.display = 'block'
	    let dates = new Date()
	    date.value = dates
	    let view = new cerateOption()
	    view.createOptionWarehouse(listWarehouse)
	}
})*/


class InventoryModel {
	constructor() {
		this.view = null
		this.id = document.querySelector('#edit')
		this.btnUpdate = document.getElementById("btn-edit")
		this.listInventory = listInventory
		this.addInventoryForm = new AddInventory()
		if (!this.listInventory || this.listInventory.length < 1) {
			console.log("no data")
			this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))
		}	

		this.onclick()
	
	}
	onclick() {
		
		this.btnUpdate.onclick = () => {
			this.saveEdit(this.id.dataset.id, document.querySelector("#warehouse2").value, showInventory.querySelectorAll('input')[2].value)
			listing.style.display = 'none'
		    editings.style.display = 'block'
		    let id = this.id.dataset.id

		    showInventory.innerHTML = "";
		    for( var i = 0; i < listInventory.length; i++){
		        if (listInventory[i].id == id) {
		            var inv = listInventory[i];
		        }
		    }
		    templateShowInventory.querySelectorAll('span')[0].textContent = inv.pathner
		    templateShowInventory.querySelectorAll('span')[1].textContent = inv.state
		    templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
		    const clone = templateShowInventory.cloneNode(true)
		    fragment.appendChild(clone)
		    showInventory.appendChild(fragment)
			
		}
	}
	

	setView(view) {
		this.view = view

	}
	save() {
		localStorage.setItem('TableCalc', JSON.stringify(this.listInventory))
	}
	showEdit(id){
		this.view.showEdit(id)
	}

	getInventory() {
		return listInventory.map((inventory) => ({...inventory}))
	}

	findInventory(id) {
		return listInventory.findIndex((inventory) => inventory.id == id)
	}

	stateInventory(id) {
		const index = this.findInventory(id)
		const inventory = this.listInventory[index]
		inventory.state = "ok"
		this.save()

	}
	saveEdit(id, warehouse, amont){
	    let values = {
	    	warehouse,
	    	amont,
	    }
	    let index = this.findInventory(id)
	    Object.assign(listInventory[index], values)
	    this.save()
	}

	editInventory(id, values) {
		const index = this.findInventory(id)
		Object.assign(this.listInventory[index], values)
		this.save()
	}

    //algo especial por el detalle de inv..
	addInventory(warehouse, pathner, amont, difference) {
		let conut_id = 0
		if (this.listProduct) {
			conut_id = parseInt(this.listProduct.length) + 1
		}else{
			conut_id = 1
		}
		let dates = new Date()
        let month = dates.getMonth()
		const inventory = {
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
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('TableCalc', JSON.stringify([inventory]))
		}
		return {...inventory}

	}

	removeInventory(id) {
		const index = this.findInventory(id)
		listInventory.splice(index, 1)
		this.save()
	}

	/*addInventory2(warehouse, partner, amont, difference) {
		let date = new Date()
        let month = date.getMonth()
		const inventory = {
			id: Date.now(),
			ids,
			month: month,
			date_time: date,
            state: "draf",
            id_warehouse,
            ids_detail,
            partner,
            total_pa,
            total_na,
            total_difference,
            
		}
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([inventory]))
		}
		return {...inventory}

	}*/

    // if state draf ok delete
	

	/*addDetailInventory(warehouse, pathner, amont, difference) {
		let fecha = new Date()
        let month = fecha.getMonth()
		const detail = {
			id: Date.now(),
            ids,
            id_inventory,
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
            difference,
            price,            
            amont,
		}
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([inventory]))
		}
		return {...inventory}

	}*/



}

class InventoryView {
	constructor() {
		this.model = null
		this.templateInventory = document.querySelector('#list-inventory').content
		this.listsInventory = document.querySelector('#tableProduct')
		this.templateGasOil = document.querySelector('#list-product-gas').content
		this.listsProductGas = document.querySelector('#tableProductGasOil')
		this.btn = document.getElementById("tbn-form-create")
		this.btnRemove = document.getElementById("btn-delete")
		this.inputSearch = document.querySelector('#navbar-search-input')
		this.inputGasPul = document.querySelector('#inputGasPul')
		this.inputGasPul2 = document.querySelector('#inputGasPul2')
		this.btnUpdate = document.getElementById("btn-test")
		this.btnUpdates = document.getElementById("btn-add")
		//this.btnDelete = document.getElementById("btn-delete")
		this.addInventoryForm = new AddInventory()
		this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))
		this.addInventoryForm.showEdit(() => this.showCreate())
		//this.addInventoryForm.saveEdit((id, warehouse, amont) => this.saveEdit(id, warehouse, amont))
		this.search()
		
		this.t = true
		if (this.t) {this.onclick()}
			
	
	}
	setModel(model) {
		this.model = model
	}
	onclick() {	
		
		
		this.btnUpdate.onclick = () => {
			this.btnUpdates.style.display = "block"
					
		}

		this.btnUpdates.onclick = () => {
			//this.showContainer()
			containerModal.style.opacity = "1"
		     containerModal.style.visibility = "visible"
		     containerModalDanger.classList.toggle("modal-close")			
		}
	}



	showContainer(){
		const cant = [1,2,3,4,5]
		for (let i = 0; i< cant.length; i++) {
			let containers = document.querySelector('#containers')
		    let containersTemplate = document.querySelector('#container-to').content
		    let button = document.querySelector('#button-edit')
		    const clone = containersTemplate.cloneNode(true)
		    fragment.appendChild(clone)
		}
	    containers.appendChild(fragment)
	}

	showButton(){
	    let containers = document.querySelector('#containers')
	    let button = document.querySelector('#button-edit').content
	    const clone = button.cloneNode(true)
	    fragment.appendChild(clone)
	    containers.appendChild(fragment)
	}
	/*onclick() {
		let id = document.querySelector('#edit')
		this.btnUpdate.onclick = () => {
			this.model.saveEdit(id.dataset.id, document.querySelector("#warehouse2").value, showInventory.querySelectorAll('input')[2].value)
		}
	}*/
	search() {
		this.inputSearch.onkeyup = () => {
			this.filtros2(this.inputSearch.value)
		}
		this.inputGasPul.onkeyup = () => {
			this.calculo(this.inputGasPul.value, this.inputGasPul2.value)
		}
		this.inputGasPul2.onkeyup = () => {
			this.calculo(this.inputGasPul.value, this.inputGasPul2.value)
		}
	}

	/*filtros2(val) {
		let busqueda = "uc"
		let expresion = new RegExp(val+'.*', "i")

		let filtros = listInventory.match(val)//filter(item => expresion.test(item))


		let misDatos = []
		for (let i = 0; i< listInventory.length; i++) {
			var todo = listInventory[i]
			var currenAmont = listInventory[i].warehouse
			if (currenAmont.toLowerCase().indexOf(val.toLowerCase()) > -1) {
				misDatos.push(todo)
			}
		}
		this.createRow(filtros)
	}*/

	filtros2(val) {
		let misDatos = []
		for (let i = 0; i< listInventory.length; i++) {
			var todo = listInventory[i]
			var currenAmont = listInventory[i].amont
			if (currenAmont.toLowerCase().indexOf(val.toLowerCase()) > -1) {
				misDatos.push(todo)
			}
		}
		this.createRow(misDatos)
	}	

	render() {
		const inventory = this.model.getInventory()
		this.createRow(inventory)
		

	}
	removeInventory(id) {
		//this.model.removeInventory(id)
		this.render()
	}

	calculo(val1, val2){
		let suma = parseInt(val1)+parseInt(val2)

		this.listsProductGas.querySelectorAll('label')[0].textContent = suma
		
	}

	//pendiente para el sig v--
	createRowGasOil(product) {
		console.log(product)
		this.listsProductGas.innerHTML = "";
		let suma = this.calculo("45", "6")
	    
	    Object.values(product).forEach(item =>{
	    	console.log(item.name)
	        this.templateGasOil.querySelectorAll('td')[0].textContent = item.code
	        this.templateGasOil.querySelectorAll('td')[1].textContent = item.name
	        this.templateGasOil.querySelectorAll('label')[0].textContent = suma

	        const clone = this.templateGasOil.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.listsProductGas.appendChild(fragment)
	}




	createRow(inventory) {
		this.listsInventory.innerHTML = "";
		let te = document.querySelector('#testt')
		let btnRemo = document.createElement('button')
		btnRemo.classList.add('btn', 'btn-danger', 'mb-1', 'ml-1')
		const btn = document.querySelectorAll('.btn-danger')
	    
	    Object.values(inventory).forEach(item =>{
	    	let misDatos = []
	    	/*let index = this.getIdWArehouse(item.id)
	    	if (listWarehouse[index].id == item.warehouse) {
					misDatos.push(todo)
				}*/
			for (let i = 0; i< listWarehouse.length; i++) {
				var todo = listWarehouse[i]
				var currenAmont = listWarehouse[i].id
				if (currenAmont == item.warehouse) {
					misDatos.push(todo)
				}
			}
	        this.templateInventory.querySelector('a').textContent = item.id
	        this.templateInventory.querySelectorAll('td')[1].textContent = misDatos[0].name + " " + misDatos[0].num
	        this.templateInventory.querySelectorAll('td')[2].textContent = item.pathner
	        this.templateInventory.querySelectorAll('td')[3].textContent = item.amont
	        this.templateInventory.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateInventory.querySelector('.link').dataset.id = item.id
	        const clone = this.templateInventory.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.listsInventory.appendChild(fragment)
	}

	showFormCreate(){
		listing.style.display = 'none'
	    formCreate.style.display = 'block'
	}
	showFormEdit(){
		listing.style.display = 'none'
	    editings.style.display = 'block'
	}

	showCreate(){
		let date = document.querySelector('#date-create')
		this.showFormCreate()	    
	    let dates = new Date()
	    date.valueAsDate = dates
	    let view = new cerateOption()
	    view.createOptionWarehouse(listWarehouse)

	    //this.createRowGasOil(listProduct)
	}

	showEdit(id){
		this.showFormEdit()
	    let inv = this.getIdInventory(id)
	    document.querySelector('#edit').dataset.id = inv.id
	    templateShowInventory.querySelectorAll('span')[0].textContent = inv.pathner
	    templateShowInventory.querySelectorAll('span')[1].textContent = inv.state
	    templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
	    const clone = templateShowInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	}
	
	showDetail(){
		this.showFormEdit()
	    let inv = this.getIdInventory(document.querySelector('#edit').dataset.id)
	    showInventory.innerHTML = ""
	    templateEditInventory.querySelectorAll('input')[0].textContent = inv.pathner
	    templateEditInventory.querySelectorAll('input')[1].textContent = inv.state
	    templateEditInventory.querySelectorAll('input')[2].textContent = inv.amont
	    const clone = templateEditInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	}
	showEditing(){
		this.showFormEdit()
	    let inv = this.getIdInventory(document.querySelector('#edit').dataset.id)
	    showInventory.innerHTML = ""
	    templateEditInventory.querySelectorAll('input')[0].value = inv.pathner
	    templateEditInventory.querySelectorAll('input')[1].value = inv.state
	    templateEditInventory.querySelectorAll('input')[2].value = inv.amont
	    const clone = templateEditInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	    let view = new cerateOption()
        view.createOptionWarehouse2(listWarehouse,inv.warehouse)
	}
	
	saveEdit(id, warehouse, amont){
		
		//let id = document.querySelector('#edit').dataset.id
		listing.style.display = 'none'
	    editings.style.display = 'block'

	    showInventory.innerHTML = "";
	    for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == id) {
	            var inv = listInventory[i];
	        }
	    }
	    templateShowInventory.querySelectorAll('span')[0].textContent = inv.pathner
	    templateShowInventory.querySelectorAll('span')[1].textContent = inv.state
	    templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
	    const clone = templateShowInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	}
	addInventory(warehouse, pathner, amont, difference) {
		const inventory = this.model.addInventory(warehouse, pathner, amont, difference)
		this.render()
	}
	//getInventoryAll and getInventory
	getIdInventory(id){
		/*console.log("init")
		console.log(id)
		console.log(model)
		const index = this.model.findInventory(id)
		console.log(index)
		let inv = listInventory[index]*/
		for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == id) {
	            var inv = listInventory[i];
	        }
	      }
	    return inv
	}

	getIdWArehouse(id){
		for( var i = 0; i < listWarehouse.length; i++){
	        if (listWarehouse[i].id == id) {
	            var inv = listWarehouse[i];
	        }
	      }
	    return inv
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
		console.log("test")
		 console.log(containerModal)
		 console.log(containerModal.classList)
		 containerModal.classList.remove('example-modal')
		 containerModal.classList.add('example-modal2')
	}
}

class cerateOption {
	constructor(){
		this.select = document.querySelector('#warehouse')
		this.select2 = document.querySelector('#warehouse2')
	}

	createOptionWarehouse(warehouse) {
		this.select.innerHTML = "";		
		let option = document.createElement('option')
	    Object.values(warehouse).forEach(item =>{	    	
	        option.textContent = item.name + " " + item.num
	        option.value = item.id
	        const clone = option.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.select.appendChild(fragment)
	}

	createOptionWarehouse2(warehouse, id) {
		let misDatos = []
		for (let i = 0; i< warehouse.length; i++) {
			var todo = warehouse[i]
			var currenAmont = warehouse[i].id
			if (currenAmont == id) {
				misDatos.push(todo)
			}
		}
		this.select2.innerHTML = "";		
		let option = document.createElement('option')
	    Object.values(warehouse).forEach(item =>{	    	
	        option.textContent = item.name + " " + item.num
	        option.value = item.id
	        const clone = option.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.select2.appendChild(fragment)
	    for (let i = 0; i< this.select2.options.length; i++) {
			if (this.select2.options[i].value == id) {
				this.select2.options[i].defaultSelected = true
			}
		}
	}
}


class InventoryView2 {
	constructor() {
		this.templateInventory = document.querySelector('#list-inventory').content
		this.listsInventory = document.querySelector('#tableProduct')
		this.btn = document.getElementById("tbn-form-create")
		this.btnRemove = document.getElementById("btn-delete")
		this.inputSearch = document.querySelector('#navbar-search-input')
	}
	removeInventory(id) {
		//this.model.removeInventory(id)
		console.log(id)
		this.render()
	}
	createRow(inventory) {
		this.listsInventory.innerHTML = "";
		let te = document.querySelector('#testt')
		let btnRemo = document.createElement('button')
		btnRemo.classList.add('btn', 'btn-danger', 'mb-1', 'ml-1')
		const btn = document.querySelectorAll('.btn-danger')
	    
	    Object.values(inventory).forEach(item =>{
	    	let misDatos = []
	    	/*let index = this.getIdWArehouse(item.id)
	    	if (listWarehouse[index].id == item.warehouse) {
					misDatos.push(todo)
				}*/
			for (let i = 0; i< listWarehouse.length; i++) {
				var todo = listWarehouse[i]
				var currenAmont = listWarehouse[i].id
				if (currenAmont == item.warehouse) {
					misDatos.push(todo)
				}
			}
	        this.templateInventory.querySelector('a').textContent = item.id
	        this.templateInventory.querySelectorAll('td')[1].textContent = misDatos[0].name + " " + misDatos[0].num
	        this.templateInventory.querySelectorAll('td')[2].textContent = item.pathner
	        this.templateInventory.querySelectorAll('td')[3].textContent = item.amont
	        this.templateInventory.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateInventory.querySelector('.link').dataset.id = item.id
	        const clone = this.templateInventory.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.listsInventory.appendChild(fragment)
	}
	showFormCreate(){
		listing.style.display = 'none'
	    formCreate.style.display = 'block'
	}
	showFormEdit(){
		listing.style.display = 'none'
	    editings.style.display = 'block'
	}

	showCreate(){
		let date = document.querySelector('#date-create')
		this.showFormCreate()	    
	    let dates = new Date()
	    date.valueAsDate = dates
	    let view = new cerateOption()
	    view.createOptionWarehouse(listWarehouse)
	}

	showEdit(id){
		this.showFormEdit()
	    let inv = this.getIdInventory(id)
	    document.querySelector('#edit').dataset.id = inv.id
	    templateShowInventory.querySelectorAll('span')[0].textContent = inv.pathner
	    templateShowInventory.querySelectorAll('span')[1].textContent = inv.state
	    templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
	    const clone = templateShowInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	}
	
	
	showEditing(){
		this.showFormEdit()
	    let inv = this.getIdInventory(document.querySelector('#edit').dataset.id)
	    showInventory.innerHTML = ""
	    templateEditInventory.querySelectorAll('input')[0].value = inv.pathner
	    templateEditInventory.querySelectorAll('input')[1].value = inv.state
	    templateEditInventory.querySelectorAll('input')[2].value = inv.amont
	    const clone = templateEditInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	    let view = new cerateOption()
        view.createOptionWarehouse2(listWarehouse,inv.warehouse)
	}
	update(){
		this.model.saveEdit()
		let id = document.querySelector('#edit').dataset.id
		console.log(id)
		listing.style.display = 'none'
	    editings.style.display = 'block'

	    showInventory.innerHTML = "";
	    for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == id) {
	            var inv = listInventory[i];
	        }
	    }
	    templateShowInventory.querySelectorAll('span')[0].textContent = inv.pathner
	    templateShowInventory.querySelectorAll('span')[1].textContent = inv.state
	    templateShowInventory.querySelectorAll('span')[2].textContent = inv.amont
	    const clone = templateShowInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
	}
	
	//getInventoryAll and getInventory
	getIdInventory(id){
		/*console.log("init")
		console.log(id)
		console.log(model)
		const index = this.model.findInventory(id)
		console.log(index)
		let inv = listInventory[index]*/
		for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == id) {
	            var inv = listInventory[i];
	        }
	      }
	    return inv
	}
}


class AddInventory {
	constructor(){
		this.btnCreate = document.getElementById("btnCreate")
		this.warehouse = document.getElementById("warehouse"); //$("#alm").val();
	    this.pathner = document.getElementById("pathner"); //$("#despachador").val();
	    this.amont = document.getElementById("amont"); //$("#total").val();
	    this.difference = document.getElementById("difference"); //$("#diferencia").val();
	    //this.btnEdit = document.getElementById("btnEdit")
	    this.btnEdit = document.getElementById("btn-form-create")
	    
	}

	onClick(callback) {
		this.btnCreate.onclick = () => {
			if (this.warehouse.value === '' || this.pathner.value === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.warehouse.value, this.pathner.value, this.amont.value, this.difference.value)
			}
		}
	}
	//showEdit(callback) {this.btnEdit.onclick = () => {callback(document.getElementById("btnEdit").dataset.id)}
	showEdit(callback) {this.btnEdit.onclick = () => {callback()}}
	

	
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

function Containers(){
	let containers = document.querySelector('#containers')
	containers.innerHTML = ""
	const res = JSON.parse(localStorage.getItem("Containers"))

	if (res) {
		
		for (let i = 0; i< res.length; i++) {

			
		    let containersTemplate = document.querySelector('#container-to').content
		    let button = document.querySelector('#button-edit')
		    const clone = containersTemplate.cloneNode(true)
		    fragment.appendChild(clone)
		}
	    containers.appendChild(fragment)

		
	}

}


window.addEventListener('click', e => {
	if (e.target.classList.contains('btn-outline')) {
		let name = document.querySelector('#nameContainer')
		const res = JSON.parse(localStorage.getItem("Containers"))

		const container = {
			id: Date.now(),
            name: name,
            state: "draf",
		}
		
		if (res) {
			res.push(container)
			localStorage.setItem('Containers', JSON.stringify(res))
		}else{
			localStorage.setItem('Containers', JSON.stringify([res]))
		}
		Containers()
     
	     setTimeout(function(){
	     	containerModal.style.opacity = "0"
	        containerModal.style.visibility = "hidden"

	     },900)
  }

	if (e.target == containerModal) {
		containerModalDanger.classList.toggle("modal-close")
     
     setTimeout(function(){
     	containerModal.style.opacity = "0"
        containerModal.style.visibility = "hidden"

     },900)

	}
})

listing.addEventListener('click', e => {
  const view = new InventoryView2()
  const model = new InventoryModel()
  /*if (e.target.classList.contains('btn-box-tool')) {
	view.showCreate()
  }*/
  
  if (e.target.classList.contains('btn-box-tool-1')) {
		model.removeInventory(e.target.dataset.id)
		let inventory = model.getInventory()
		view.createRow(inventory)
  }
  if (e.target.classList.contains('btn-default')) {
     view.showDetail()	    
  }
  if (e.target.classList.contains('link')) {
  	view.showEdit(e.target.dataset.id)
  }

})

editings.addEventListener('click', e => {
	const view = new InventoryView()
    const model = new InventoryModel()
  if (e.target.classList.contains('btn-success')) { 
     view.showEditing()
  }

  if (e.target.classList.contains('btn-primary')) {
  	
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




class TablaCalculo {
	constructor(){
		this.btnCreate = document.getElementById("btnCreate")
		this.warehouse = document.getElementById("warehouse"); //$("#alm").val();
	    this.pathner = document.getElementById("pathner"); //$("#despachador").val();
	    this.amont = document.getElementById("amont"); //$("#total").val();
	    this.difference = document.getElementById("difference"); //$("#diferencia").val();
	    //this.btnEdit = document.getElementById("btnEdit")
	    this.btnEdit = document.getElementById("btn-form-create")
	    
	}

	onClick(callback) {
		this.btnCreate.onclick = () => {
			if (this.warehouse.value === '' || this.pathner.value === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.warehouse.value, this.pathner.value, this.amont.value, this.difference.value)
			}
		}
	}
	//showEdit(callback) {this.btnEdit.onclick = () => {callback(document.getElementById("btnEdit").dataset.id)}
	showEdit(callback) {this.btnEdit.onclick = () => {callback()}}
	

	
}



/*class RemoveInventory {
	constructor(){
		this.templateInventory = document.querySelector('#list-inventory')
		this.listsInventory = document.querySelector('#tableProduct')
		this.tr = this.listsInventory.querySelectorAll('.btn-box-tool-1')
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
			console.log(this.listsInventory)
		}
		

	}
}

class EditInventory {
	constructor(){
		this.btnEdit = document.getElementById("btn-edit"); //$("#alm").val();
		this.warehouse = document.getElementById("warehouse-edit"); //$("#alm").val();
	    this.id = document.getElementById("id-editing"); //$("#despachador").val();
	    this.amont = document.getElementById("amont-edit"); //$("#total").val();
	    //this.difference = document.getElementById("difference"); //$("#diferencia").val();
	    //this.date = document.getElementById("date").value; //$("#fechas").val();
	}

	onClick(callback) {
		this.btnEdit.onclick = () => {
			const inventory = {
	            warehouse: this.warehouse,
	            amont: this.amont,
			}
				callback(this.id.value, inventory)
			
		}

	}
}*/

