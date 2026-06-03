odoo.define('pos_margin.ProductListSearch', function(require) {
    'use strict';

    const {
        useState,
        useRef
    } = owl.hooks;

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ProductListSearch extends PosComponent {
        constructor() {
            super(...arguments);
            this.searchWordInput = useRef('search-word-input');
            this.state = useState({ searchWord: '' });


             
        }

        get searchWord() {
            return this.state.searchWord.trim();
        }

        get selectedCategoryId() {
            return this.env.pos.get('selectedCategoryId');
        }

        productsToDisplay() {
            return this.env.pos.db.search_product_in_category(
                    this.selectedCategoryId,
                    this.searchWord
                );
            
        }

        spaceClickProduct(event) {
            var order = this.env.pos.get_order();
            
            if (event.which === 113) {
                console.log(order.orderlines.length)
                if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                    $($(document).find("#rowProduct")).addClass('rowsProduct')
                }else{
                    $($(document).find("#rowProduct.rowsProduct")).next().addClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).focus()
                    $($(document).find("#rowProduct.rowsProduct")).prev().removeClass('rowsProduct')
                    $($(document).find("#rowProduct")).removeClass('rowsProduct') 
                }
            }

            if (event.which === 81) {
                if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                    $($(document).find("#rowProduct")).addClass('rowsProduct')
                }else{
                    $($(document).find("#rowProduct.rowsProduct")).next().addClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).focus()
                    $($(document).find("#rowProduct.rowsProduct")).prev().removeClass('rowsProduct')
                    $($(document).find("#rowProduct")).removeClass('rowsProduct') 
                }
                
            }

            if (event.which === 97) {
                if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                    $($(document).find("#rowProduct")).addClass('rowsProduct')

                }else{

                    $($(document).find("#rowProduct.rowsProduct")).prev().addClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).next().removeClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).focus()                    
                }
            }


            if (event.which === 65) {
                if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                    $($(document).find("#rowProduct")).addClass('rowsProduct')

                }else{

                    $($(document).find("#rowProduct.rowsProduct")).prev().addClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).next().removeClass('rowsProduct')
                    $($(document).find("#rowProduct.rowsProduct")).focus()                    
                }
            }


            if (event.which === 98) {
                $($(document).find("#buscar")).focus()
                //console.log($($(document).find("#buscar")))
                
            }

            if (event.which === 66) {
                $($(document).find("#buscar")).focus()
                //$($(document).find("#buscar")).empty()
            }
  




            if (event.which === 32) {
                if ($($(document).find("#rowProduct.rowsProduct")).length > 0) {
                    this.selectProduct($($(document).find("#myTable"))[0].childNodes.length,this.props.products)
                } 
            }




            if (event.which === 13) {
                
                
                this.lineOrder()

                

            }
            
        }

        _clearSearch() {
            this.state.searchWord = '';
        }


  

        selectProduct(totalRows,data){

            for (var i = 0; i < totalRows; i++) {

                if (data[i].product_tmpl_id == $($(document).find("#rowProduct.rowsProduct"))[0].dataset.productId ) {
                    this.trigger('click-product', data[i]);

                }
            }
        }


        nextProduct(){

            if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                var list2 = []
                for (var i = 0; i < this.props.products.length; i++) {
                    if (this.props.products[i].default_code == 'FACTURACION') {
                        list2.push(this.props.products[i])
                    }
                }
                console.log(list2.length)
                if (list2.length > 0) {
                    $($(document).find("#rowProduct")).addClass('rowsProduct')
                }else{
                    console.log('next test')
                }
                
            }else{
                $($(document).find("#rowProduct.rowsProduct")).next().addClass('rowsProduct')
                $($(document).find("#rowProduct.rowsProduct")).focus()
                $($(document).find("#rowProduct.rowsProduct")).prev().removeClass('rowsProduct')
                $($(document).find("#rowProduct")).removeClass('rowsProduct') 
            }

            if ($($(document).find("#rowProduct.rowsProduct")).length > 0) {
                this.selectProduct($($(document).find("#myTable"))[0].childNodes.length,this.props.products)
            }
        }





        lineOrder(){
            var order = this.env.pos.get_order();

            if (order.orderlines.length === 0) {
                this.nextProduct()

                console.log('not order')
                console.log(order.orderlines.length)
                
            }else{
                var list = []
                
                for (var i = 0; i < order.orderlines.length; i++) {
                    if (order.orderlines.models[i].product.default_code == 'FACTURACION') {
                        list.push(order.orderlines.models[i])

                    }
                    
                }
                this.nextProduct()

                
                console.log(list.length)
                
            }


            if ($($(document).find("#rowProduct.rowsProduct")).length == 0) {
                console.log('not rows')
                
            }else{
                console.log($($(document).find("#rowProduct.rowsProduct"))[0].dataset.productId)
            }
            
        }



        get imageUrl() {
            const product = this.props.products;
            return `/web/image?model=product.product&field=image_128&id=${product.id}&write_date=${product.write_date}&unique=1`;
        }
        get pricelist() {
            const current_order = this.env.pos.get_order();
            if (current_order) {
                return current_order.pricelist;
            }
            return this.env.pos.default_pricelist;
        }

    }
    ProductListSearch.template = 'ProductListSearch';

    Registries.Component.add(ProductListSearch);

    return ProductListSearch;
});
