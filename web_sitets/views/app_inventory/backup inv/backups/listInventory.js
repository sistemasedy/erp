const listInventory = JSON.parse(localStorage.getItem("Inventarios"))
const templateInventory = document.querySelector('#list-inventory').content
const fragment = document.createDocumentFragment();
const listsInventory = document.querySelector('#tableProduct')

document.addEventListener('DOMContentLoaded', () => {
  getListInventory();
  alert("hola")

})

listsInventory.addEventListener('click', e => {
  deleInventory(e)
})

function getListInventory(){
  listsInventory.innerHTML = "";
  Object.values(listInventory).forEach(item =>{
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

  if (e.target.classList.contains('link')) {
    localStorage.setItem('Tokens', JSON.stringify([{
          'id': '2',
          'token': e.target.dataset.id,
      }]));

  }
}


