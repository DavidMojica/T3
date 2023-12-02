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

step2FormUpdate.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";
    let preventiveBan = true;
    let preventiveMsg = "";
    let toDangerBg = [];
    let toWarningBg = [];

    const addErrorMsg = (condition, errorMsg, obj) => {
        if (condition) {
            ban = false;
            msg += errorMsg + "<br>";
            toDangerBg.push(obj);
        }
    };
    
    const addPreventiveMsg = (condition, preventiveErrorMsg, obj) => {
        if (condition) {
            preventiveBan = false;
            preventiveMsg += preventiveErrorMsg + "<br>";
            toWarningBg.push(obj);
        }
    };

    addErrorMsg(edad.value < 0 || isNaN(edad.value), "Error en la edad", edad);
    addErrorMsg(documento.value === "" || documento.value.trim().length < 4, "Por favor verifique el documento", documento);
    addErrorMsg(nombre.value.trim() === "" || nombre.value.trim().length < 4, "Compruebe el nombre", nombre);
    addErrorMsg(!moment(fecha_nacimiento.value, 'YYYY-MM-DD', true).isValid(), "La fecha está en el formato incorrecto", fecha_nacimiento);
    addPreventiveMsg(direccion.value === "", "La dirección está vacía ¿Continuar?", direccion);
    addPreventiveMsg(barrio.value === "", "El barrio está vacío ¿Continuar?", barrio);
    addPreventiveMsg(hijos.value === "", "La cantidad de hijos está vacia, será reemplazada por 0", hijos);
    addErrorMsg(isNaN(etnia.value) || etnia.value < 0  || etnia.value > numEtnias,"Dato erroneo en etnia.", etnia)
    addErrorMsg(isNaN(ocupacion.value) ||ocupacion.value < 0 ||ocupacion.value > numOcupaciones, "Dato erroneo en ocupacion.",ocupacion);
    addErrorMsg(isNaN(rss.value) || rss.value < 0 || rss.value > numRegimenes, "Dato erroneo en regimen", rss);
    addErrorMsg(isNaN(eps.value) || eps.value < 0 || eps.value > numEps, "Dato erroneo en Eps", eps); 
})