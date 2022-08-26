// Model and View for Entity
const listInventory = JSON.parse(localStorage.getItem("Inventarios"))
const fragment = document.createDocumentFragment();
const formCreate = document.querySelector('#form-create')
const listing = document.querySelector('#listing')
const editing = document.querySelector('#tableProduct')


document.addEventListener('DOMContentLoaded', () => {
  const model = new InventoryModel()
  const view = new InventoryView()

  model.setView(view)
  view.setModel(model)

  view.render()
})


listing.addEventListener('click', e => {

  if (e.target.classList.contains('btn-box-tool')) {
    listing.style.display = 'none'
    formCreate.style.display = 'block'

  }

  if (e.target.classList.contains('btn-box-tool-1')) {
  	const view = new InventoryView()
  	view.removeInventory(e.target.dataset.id)   
       

    }
})


formCreate.addEventListener('click', e => {

  if (e.target.classList.contains('btn-default')) {
    listing.style.display = 'block'
    formCreate.style.display = 'none'


  }
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
		//localStorage.setItem('Inventarios', JSON.stringify(this.listInventory))
		localStorage.setItem('Inventarios', JSON.stringify(this.listInventory))

	}

	getInventory() {
		return listInventory.map((inventory) => ({...inventory}))

	}

	findInventory(id) {
		return this.listInventory.findIndex((inventory) => inventory.id === id)

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

    //algo especial por el detalle de inv..
	addInventory(warehouse, pathner, amont, difference) {
		let fecha = new Date()
        let month = fecha.getMonth()
		const inventory = {
			id: Date.now(),
            warehouse,
            pathner,
            amont,
            difference,
            date: month,
            state: "draf",
		}
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventarios', JSON.stringify([inventory]))
		}
		
		


		return {...inventory}

	}

    // if state draf ok delete
	removeInventory(id) {
		const index = this.findInventory(id)
		this.listInventory.splice(index, 1)
		this.save()

	}

}

class InventoryView {
	constructor() {
		this.model = null
		this.templateInventory = document.querySelector('#list-inventory').content
		this.listsInventory = document.querySelector('#tableProduct')
		this.btn = document.getElementById("tbn-form-create"); //$("#alm").val();
		this.addInventoryForm = new AddInventory()
		this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))

	}


	setModel(model) {
		this.model = model
	}

	render() {
		const inventory = this.model.getInventory()
		this.createRow(inventory)
		

	}
	removeInventory() {
		//this.model.removeInventory(id)
		this.render()
		console.log('id')
	}

    //const btnRemove = document.getElementById("btn-removes")

	createRow(inventory) {
		
		this.listsInventory.innerHTML = "";
	    Object.values(inventory).forEach(item =>{
	        this.templateInventory.querySelector('a').textContent = item.id
	        this.templateInventory.querySelectorAll('td')[1].textContent = item.warehouse
	        this.templateInventory.querySelectorAll('td')[2].textContent = item.pathner
	        this.templateInventory.querySelectorAll('td')[3].textContent = item.amont
	        this.templateInventory.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateInventory.querySelector('.link').dataset.id = item.id

	        const clone = this.templateInventory.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.listsInventory.appendChild(fragment)
	    
	    
	    
	}

	addInventory(warehouse, pathner, amont, difference) {
		const inventory = this.model.addInventory(warehouse, pathner, amont, difference)
		this.render()
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
			//callback(this.warehouse, this.pathner, this.amont, this.difference)
			if (this.warehouse.value === '' || this.pathner.value === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.warehouse.value, this.pathner.value, this.amont.value, this.difference.value)
			}
			//console.log(this.warehouse)
			
		}

	}
}