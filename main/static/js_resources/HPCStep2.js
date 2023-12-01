//step2 - Update
const step1FormUpdate = document.getElementById('step1FormUpdate');
const e_documento = document.getElementById('e_documento');
const e_nombre = document.getElementById('e_nombre');
const fecha_nacimiento = document.getElementById('fecha_nacimiento');
const e_edad = document.getElementById('e_edad');

fecha_nacimiento.addEventListener('change', function () {
    var fechaNacimiento = new Date(fecha_nacimiento.value);
    var fechaActual = new Date();
    var edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
    if (fechaActual.getMonth() < fechaNacimiento.getMonth() || (fechaActual.getMonth() === fechaNacimiento.getMonth() && fechaActual.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    e_edad.value = edad;
});