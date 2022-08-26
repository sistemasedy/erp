// Model and View for Entity
const listProduct = JSON.parse(localStorage.getItem("Products"))
const fragment = document.createDocumentFragment();
const formCreate = document.querySelector('#form-create')
const listing = document.querySelector('#listing')
const editing = document.querySelector('#tableProduct')


document.addEventListener('DOMContentLoaded', () => {
  const model = new ProductModel()
  const view = new ProductView()

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
  	const view = new ProductView()
  	view.removeProduct(e.target.dataset.id)   
       

    }
})


formCreate.addEventListener('click', e => {

  if (e.target.classList.contains('btn-default')) {
    listing.style.display = 'block'
    formCreate.style.display = 'none'


  }
})


class ProductModel {
	constructor() {
		this.view = null
		this.listProduct = listProduct
		this.addProductForm = new AddProduct()
		if (!this.listProduct || this.listProduct.length < 1) {
			console.log("no data")
			this.addProductForm.onClick((name, measure, price, code, category) => this.addProduct(name, measure, price, code, category))
		}	

	}

	setView(view) {
		this.view = view

	}
	save() {
		//localStorage.setItem('Inventarios', JSON.stringify(this.listProduct))
		localStorage.setItem('Products', JSON.stringify(this.listProduct))

	}

	getProduct() {
		return listProduct.map((Product) => ({...Product}))

	}

	findProduct(id) {
		return this.listProduct.findIndex((Product) => Product.id === id)

	}

	stateProduct(id) {
		const index = this.findProduct(id)
		const Product = this.listProduct[index]
		Product.active = "False"
		this.save()

	}

	editProduct(id, values) {
		const index = this.findProduct(id)
		Object.assign(this.listProduct[index], values)
		this.save()

	}

    //algo especial por el detalle de inv..
	addProduct(name, measure, price, code, category) {
		let conut_id = 0
		if (this.listProduct) {
			conut_id = parseInt(this.listProduct.length) + 1
		}else{
			conut_id = 1
		}
		let fecha = new Date()
        let month = fecha.getMonth()
		const Product = {
			id: Date.now(),
			ids: conut_id,
			active: "True",
            name,
            measure,
            price,
            code,
            category,
		}
		if (this.listProduct) {
			this.listProduct.push(Product)
		    this.save()
		}else{
			localStorage.setItem('Products', JSON.stringify([Product]))
		}
		
		


		return {...Product}

	}

    // if state draf ok delete
	removeProduct(id) {
		const index = this.findProduct(id)
		this.listProduct.splice(index, 1)
		this.save()

	}

}

class ProductView {
	constructor() {
		this.model = null
		this.templateProduct = document.querySelector('#list-product').content
		this.listsProduct = document.querySelector('#tableProduct')
		this.btn = document.getElementById("tbn-form-create"); //$("#alm").val();
		this.addProductForm = new AddProduct()
		this.addProductForm.onClick((name, measure, price, code, category) => this.addProduct(name, measure, price, code, category))

	}


	setModel(model) {
		this.model = model
	}

	render() {
		const Product = this.model.getProduct()
		this.createRow(Product)
		

	}
	removeProduct() {
		//this.model.removeProduct(id)
		this.render()
		console.log('id')
	}

    //const btnRemove = document.getElementById("btn-removes")

	createRow(Product) {
		
		this.listsProduct.innerHTML = "";
	    Object.values(Product).forEach(item =>{
	        this.templateProduct.querySelector('a').textContent = item.code
	        this.templateProduct.querySelectorAll('td')[1].textContent = item.name
	        this.templateProduct.querySelectorAll('td')[2].textContent = item.price
	        this.templateProduct.querySelectorAll('td')[3].textContent = item.measure
	        this.templateProduct.querySelector('.btn-box-tool-1').dataset.id = item.id
	        this.templateProduct.querySelector('.link').dataset.id = item.id

	        const clone = this.templateProduct.cloneNode(true)
	        fragment.appendChild(clone)
	    })
	    this.listsProduct.appendChild(fragment)
	    
	    
	    
	}

	addProduct(name, measure, price, code, category) {
		const Product = this.model.addProduct(name, measure, price, code, category)
		this.render()
	}
}


class AddProduct {
	constructor(){
		this.btnCreate = document.getElementById("btnCreate"); //$("#alm").val();
		this.name = document.getElementById("nametxt"); //$("#alm").val();
	    this.btnMeasure = document.getElementById("measuretxt"); //$("#despachador").val();
	    this.price = document.getElementById("pricetxt"); //$("#total").val();
	    this.code = document.getElementById("codetxt"); //$("#diferencia").val();
	    this.btnCategory = document.getElementById("categorytxt"); //$("#fechas").val();
	   
	}
	onClick(callback) {
		
		this.btnCreate.onclick = () => {
			if (this.name.value === '' || this.code.value === '') {
				alert("Los Campos Estan  Vacio")
			}else{
				callback(this.name.value, this.btnMeasure.value, this.price.value, this.code.value, this.btnCategory.value)
				this.name.value = ""
				this.price.value = ""
				this.code.value = ""
			}
			
		}

	}
}