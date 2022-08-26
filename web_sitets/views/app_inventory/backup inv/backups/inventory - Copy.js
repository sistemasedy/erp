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


class InventoryModel {
	constructor() {
		this.view = null
		this.listInventory = listInventory
		if (!this.listInventory || this.listInventory.length < 1) {
			alert("no hay datos") //this.listInventory = this.base(data)
		}

	}

	setView(view) {
		this.view = view

	}
	save() {
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
		const inventory = {
			//Date.Now(),  //Date.getMonth()
			id: "1" ,
            warehouse,
            pathner,
            amont,
            difference,
            date: "oct",
            state: "draf",
		}
		this.listInventory.push(inventory)
		console.log(this.listInventory)
		this.save()


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
		this.addInventoryForm = new AddInventory()

		this.addInventoryForm.onClick((warehouse, pathner, amont, difference) => this.addInventory(warehouse, pathner, amont, difference))

	}

	setModel(model) {
		this.model = model
	}

	render() {

		const inventory = this.model.getInventory()
		listsInventory.innerHTML = "";
	    Object.values(inventory).forEach(item =>{
	      templateInventory.querySelector('a').textContent = item.almacen
	      templateInventory.querySelectorAll('td')[1].textContent = item.id
	      templateInventory.querySelectorAll('td')[2].textContent = item.despachador
	      templateInventory.querySelectorAll('td')[3].textContent = item.total
	      templateInventory.querySelector('.btn-box-tool').dataset.id = item.id
	      templateInventory.querySelector('.link').dataset.id = item.id
	      const clone = templateInventory.cloneNode(true)
	      fragment.appendChild(clone)
	    })
	    listsInventory.appendChild(fragment)
	}

	//createRow(inventory) {}

	addInventory(warehouse, pathner, amont, difference) {
		const inventory = this.model.addInventory(warehouse, pathner, amont, difference)
		this.render()
	}






}


class AddInventory {
	constructor(){
		this.btnCreate = document.getElementById("tbnCreate"); //$("#alm").val();
		this.warehouse = document.getElementById("warehouse").value; //$("#alm").val();
	    this.pathner = document.getElementById("pathner").value; //$("#despachador").val();
	    this.amont = document.getElementById("amont").value; //$("#total").val();
	    this.difference = document.getElementById("difference").value; //$("#diferencia").val();
	    //this.date = document.getElementById("date").value; //$("#fechas").val();
	}

	onClick(callback) {
		this.btnCreate.onClick = () => {
			if (this.warehouse === '' || this.pathner === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.warehouse, this.pathner, this.amont, this.difference)
			}
		}

	}
}