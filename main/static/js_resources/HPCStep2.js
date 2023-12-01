//step2 - Update
const step1FormUpdate = document.getElementById('step1FormUpdate');
const e_tipo_documento = document.getElementById('e_tipo_documento');
const e_documento = document.getElementById('e_documento'); //o
const e_nombre = document.getElementById('e_nombre'); //o 
const fecha_nacimiento = document.getElementById('fecha_nacimiento'); //o
const e_edad = document.getElementById('e_edad'); 
const e_direccion = document.getElementById('e_direccion'); //oopc
const e_barrio = document.getElementById('e_barrio'); //opc
const e_hijos = document.getElementById('e_hijos'); //opc


fecha_nacimiento.addEventListener('change', function () {
    var fechaNacimiento = new Date(fecha_nacimiento.value);
    var fechaActual = new Date();
    var edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
    if (fechaActual.getMonth() < fechaNacimiento.getMonth() || (fechaActual.getMonth() === fechaNacimiento.getMonth() && fechaActual.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    e_edad.value = edad;
});