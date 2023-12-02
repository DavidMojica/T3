const step2FormUpdate = document.getElementById('step2FormUpdate');
const documento = document.getElementById('documento');
const nombre = document.getElementById('nombre');
const apellido = document.getElementById('apellido');
const fecha_nacimiento = document.getElementById('fecha_nacimiento');
const edad = document.getElementById('edad');
const sexo = document.getElementById('sexo');
const escolaridad = document.getElementById('escolaridad');
const hijos = document.getElementById('hijos');
const direccion = document.getElementById('direccion');
const estado_civil = document.getElementById('estado_civil');
const celular = document.getElementById('celular');
const correo = document.getElementById('correo');
const lectoescritura = document.getElementById('lectoescritura');
const lectoescritura_nivel = document.getElementById('lectoescritura_nivel');
const raz_analitico = document.getElementById('raz_analitico');
const etnia = document.getElementById('etnia');
const ocupacion = document.getElementById('ocupacion');
const rss = document.getElementById('rss');

const numEtnias = 6;
const numOcupaciones = 8;
const numRegimenes = 6;
const numEps = 36;

fecha_nacimiento.addEventListener('change', function () {
    var fechaNacimiento = new Date(fecha_nacimiento.value);
    var fechaActual = new Date();
    var edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
    if (fechaActual.getMonth() < fechaNacimiento.getMonth() || (fechaActual.getMonth() === fechaNacimiento.getMonth() && fechaActual.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    e_edad.value = edad;
});