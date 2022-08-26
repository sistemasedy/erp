// Model and View for Entity
const listInventory = JSON.parse(localStorage.getItem("Inventory"))
const listWarehouse = JSON.parse(localStorage.getItem("Warehouse"))
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
//const closeModal = document.querySelectorAll('.btn-outline')

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
		this.listInventory = listInventory
		this.addInventoryForm = new AddInventory()
		if (!this.listInventory || this.listInventory.length < 1) {
			console.log("no data")
			this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))
		}	

	}

	setView(view) {
		this.view = view

	}
	save() {
		//localStorage.setItem('Inventory', JSON.stringify(this.listInventory))
		localStorage.setItem('Inventory', JSON.stringify(this.listInventory))

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

	editInventory(id, values) {
		const index = this.findInventory(id)
		Object.assign(this.listInventory[index], values)
		this.save()

	}

	teste(warehouse, pathner, amont, difference){
		return warehouse
	}

    //algo especial por el detalle de inv..
	addInventory(warehouse, pathner, amont, difference) {
		console.log(warehouse)
		console.log("test model add")
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
		console.log("test add 2" + inventory)
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([inventory]))
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
		this.btn = document.getElementById("tbn-form-create")
		this.btnRemove = document.getElementById("btn-delete")
		this.inputSearch = document.querySelector('#navbar-search-input')
		//this.btnDelete = document.getElementById("btn-delete")
		this.addInventoryForm = new AddInventory()
		this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))
		this.teste()
	}

	setModel(model) {
		this.model = model
	}


	search() {
		this.inputSearch.onkeyup = () => {
			this.filtros2(this.inputSearch.value)


		}
	}

	teste(){
		console.log(this.model)
	}


	filtros2(val) {
		let misDatos = []
		for (let i = 0; i< listInventory.length; i++) {
			var todo = listInventory[i]
			var currenAmont = listInventory[i].warehouse
			if (currenAmont.toLowerCase().indexOf(val.toLowerCase()) > -1) {
				misDatos.push(todo)
			}
		}
		this.createRow(misDatos)
		console.log(misDatos)
	}

	

	render() {
		const inventory = this.model.getInventory()
		this.createRow(inventory)
		

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
		
		
		//te.appendChild(btnRemo)
	    
	    Object.values(inventory).forEach(item =>{
	    	
	        this.templateInventory.querySelector('a').textContent = item.id
	        this.templateInventory.querySelectorAll('td')[1].textContent = item.warehouse
	        this.templateInventory.querySelectorAll('td')[2].textContent = item.pathner
	        this.templateInventory.querySelectorAll('td')[3].textContent = item.amont
	        //this.templateInventory.querySelectorAll('td')[4].appendChild(btnRemo)
	        
	        this.templateInventory.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateInventory.querySelector('.link').dataset.id = item.id
	        const clone = this.templateInventory.cloneNode(true)

	        fragment.appendChild(clone)

	    })
	    this.listsInventory.appendChild(fragment)
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

	

	addInventory(warehouse, pathner, amont, difference) {
		console.log("tes" + " " + warehouse)
		const inventory = this.model.addInventory(warehouse, pathner, amont, difference)
		console.log("test" + " " + inventory)
		this.render()
	}

	showModal() {
		//$('#mod').modal('toggle')
		//console.log('modal')
		let modal = document.getElementById("mod")
		 modal.classList.add('example-modal')

		//modal.removeClass("modal fade").addClass("example-modal")

	}

	closeModal() {
		console.log("test")
		let modal = document.getElementById("mod")
		 modal.classList.remove('example-modal')
	}

	closeModals() {
		console.log("test")
		//let modal = document.getElementById("mod")
		 //modal.classList.remove('example-modal')
		 console.log(containerModal)
		 console.log(containerModal.classList)
		 containerModal.classList.remove('example-modal')
		 containerModal.classList.add('example-modal2')
	}


}


class AddInventory {
	constructor(){
		this.btnCreate = document.getElementById("btnCreate"); //$("#alm").val();
		this.warehouse = document.getElementById("warehouse"); //$("#alm").val();
	    this.pathner = document.getElementById("pathner"); //$("#despachador").val();
	    this.amont = document.getElementById("amont"); //$("#total").val();
	    this.difference = document.getElementById("difference"); //$("#diferencia").val();
	    //this.date = document.getElementById("date").value; //$("#fechas").val();
	}

	onClick(callback) {
		this.btnCreate.onclick = () => {
			if (this.warehouse.value === '' || this.pathner.value === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.warehouse.value, this.pathner.value, this.amont.value, this.difference.value)
			}
			//console.log(this.warehouse)
			
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
	    let view = new InventoryView()
	    view.createOptionWarehouse(listWarehouse)
  }

  
  if (e.target.classList.contains('link')) {
	    listing.style.display = 'none'
	    editings.style.display = 'block'

	    showInventory.innerHTML = "";
	    for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == e.target.dataset.id) {
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

  if (e.target.classList.contains('btn-box-tool-1')) {
		let remove = new InventoryModel()
		remove.removeInventory(e.target.dataset.id)
		location.reload()

  }

  if (e.target.classList.contains('btn-default')) {
	    listing.style.display = 'none'
	    editings.style.display = 'block'

	    let ids = document.querySelector('#id-editing').value

	    showInventory.innerHTML = "";
	    for( var i = 0; i < listInventory.length; i++){
	        if (listInventory[i].id == ids) {
	            var inv = listInventory[i];
	        }
	    }
	    templateEditInventory.querySelectorAll('input')[0].textContent = inv.id
	    templateEditInventory.querySelectorAll('input')[1].textContent = inv.warehouse
	    templateEditInventory.querySelectorAll('input')[2].textContent = inv.amont
	    const clone = templateEditInventory.cloneNode(true)
	    fragment.appendChild(clone)
	    showInventory.appendChild(fragment)
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

