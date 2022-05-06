document.addEventListener("DOMContentLoaded", search);

const URL_API = " http://127.0.0.1:3000/api"

var customer_list = []

function init() {
  search

}

function agregar() {
  clean()
  abrir_formulario()
}


function abrir_formulario(){
  html_modal = document.getElementById("modal")
  html_modal.classList.add("opened")
}

function cerrar_modale(){
  html_modal = document.getElementById("modal")
  html_modal.classList.remove("opened")
}

async function search() {
  var url = URL_API + "/customer"
  var response = await fetch(url, {
    "method": 'GET',
    "headers": {"content-type": 'aplication/json'}
  })

  customer_list = await response.json();
  console.log(customer_list)


  var html_final = ""
  for (customer of customer_list) {
    var row =`
  <tr>
  <td>${customer.firstname}</td>
  <td>${customer.lastname}</td>
  <td>${customer.phone}</td>
  <td>${customer.email}</td>
  <td><a href="#" onclick="edit_user(${customer.id})" class="myButton">Editar</a>
      <a href="#" onclick="remove_user(${customer.id})" class="myButton_delete">Eliminar</a>
  </td>
  </tr>`

  html_final = html_final + row;
  }

  
  document.querySelector('#customers > tbody').outerHTML = html_final
}

async function remove_user(id) {
  repuesta = confirm("estas seguro de eliminarlo?")
  if (repuesta)
    var url = URL_API + "/customer/" + id
    await fetch(url, {
      "method": 'DELETE',
      "headers": {"content-type": 'aplication/json'}
    })
    window.location.reload();
}

async function guardar_cliente() {
  var data = {
    "email": document.getElementById('txt_email').value,
    "firstname": document.getElementById('txt_nombre').value,
    "lastname": document.getElementById('txt_apellido').value,
    "phone": document.getElementById('txt_telefono').value
  }

  var id_cliente = document.getElementById('txt_id').value

  if (id_cliente != "") {
    data.id = id_cliente
  }

  var url = URL_API + '/customer'
  await fetch(url, {
    "method": 'POST',
    "body": JSON.stringify(data),
    "headers": {
      "Content-Type": 'application/json'
    }
  })
  window.location.reload();
}

function edit_user(id) {
  abrir_formulario()
  var customer = customer_list.find(x => x.id == id)
  document.getElementById('txt_id').value = customer.id,
  document.getElementById('txt_email').value = customer.email,
  document.getElementById('txt_nombre').value = customer.firstname,
  document.getElementById('txt_apellido').value = customer.lastname,
  document.getElementById('txt_telefono').value = customer.phone

}


function clean() {
  document.getElementById('txt_id').value = "",
  document.getElementById('txt_email').value = "",
  document.getElementById('txt_nombre').value = "",
  document.getElementById('txt_apellido').value = "",
  document.getElementById('txt_telefono').value = ""
}