class InventoryModel {
	constructor() {
		this.view = null
		this.listInventory = listInventory
		this.addInventoryForm = new AddInventory()
		if (!this.listInventory || this.listInventory.length < 1) {
			console.log("no data")
			this.addInventoryForm.onClick((address, pathner, name, num) => this.addInventory(address, pathner, name, num))
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

    //algo especial por el detalle de inv..
	addInventory(address, pathner, name, num) {
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
            address,
            pathner,
            name,
            num,
            date: month,
            date_time: dates,
            state: "draf",
		}
		if (this.listInventory) {
			this.listInventory.push(inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([inventory]))
		}
		return {...inventory}

	}

	/*addInventory2(address, partner, name, num) {
		let date = new Date()
        let month = date.getMonth()
		const Inventory = {
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
		if (this.listInventory) {
			this.listInventory.push(Inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([Inventory]))
		}
		return {...Inventory}

	}*/

    // if state draf ok delete
	removeInventory(id) {
		const index = this.findInventory(id)
		listInventory.splice(index, 1)
		this.save()

	}

	/*addDetailInventory(address, pathner, name, num) {
		let fecha = new Date()
        let month = fecha.getMonth()
		const detail = {
			id: Date.now(),
            ids,
            id_Inventory,
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
		if (this.listInventory) {
			this.listInventory.push(Inventory)
		    this.save()
		}else{
			localStorage.setItem('Inventory', JSON.stringify([Inventory]))
		}
		return {...Inventory}

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
		this.addInventoryForm.onClick((address, pathner, name, num) => this.addInventory(address, pathner, name, num))
		this.teste()
	}


	search() {
		this.inputSearch.onkeyup = () => {
			this.filtros2(this.inputSearch.value)


		}
	}


	filtros2(val) {
		let misDatos = []
		for (let i = 0; i< listInventory.length; i++) {
			var todo = listInventory[i]
			var curreNname = listInventory[i].address
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
		const inventory = this.model.getInventory()
		this.createRow(Inventory)
		

	}
	removeInventory(id) {
		//this.model.removeInventory(id)
		console.log(id)
		this.render()
	}

	

	createRow(Inventory) {
		
		this.listsInventory.innerHTML = "";
		let te = document.querySelector('#testt')
		
		let btnRemo = document.createElement('button')
		btnRemo.classList.add('btn', 'btn-danger', 'mb-1', 'ml-1')
		const btn = document.querySelectorAll('.btn-danger')
		
		
		//te.appendChild(btnRemo)
	    
	    Object.values(inventory).forEach(item =>{
	    	
	        this.templateInventory.querySelector('a').textContent = item.id
	        this.templateInventory.querySelectorAll('td')[1].textContent = item.address
	        this.templateInventory.querySelectorAll('td')[2].textContent = item.pathner
	        this.templateInventory.querySelectorAll('td')[3].textContent = item.name
	        //this.templateInventory.querySelectorAll('td')[4].appendChild(btnRemo)
	        
	        this.templateInventory.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateInventory.querySelector('.link').dataset.id = item.id
	        const clone = this.templateInventory.cloneNode(true)

	        fragment.appendChild(clone)

	    })
	    this.listsInventory.appendChild(fragment)
	}

	addInventory(address, pathner, name, num) {
		const inventory = this.model.addInventory(address, pathner, name, num)
		console.log(inventory)
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