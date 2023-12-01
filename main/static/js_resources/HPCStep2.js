//step2 - Update
const step1FormUpdate = document.getElementById('step1FormUpdate');
const e_tipo_documento = document.getElementById('e_tipo_documento');
const e_documento = document.getElementById('e_documento'); //o
const e_nombre = document.getElementById('e_nombre'); //o 
const fecha_nacimiento = document.getElementById('fecha_nacimiento'); //o - Date
const e_edad = document.getElementById('e_edad');  //NaN 0 - 100
const e_direccion = document.getElementById('e_direccion'); //oopc
const e_barrio = document.getElementById('e_barrio'); //opc
const e_hijos = document.getElementById('e_hijos'); //opc
const e_etnia = document.getElementById('e_etnia'); //NaN
const e_ocupacion = document.getElementById('e_ocupacion'); //nan
const e_rss = document.getElementById('e_rss'); //Nan
const eps = document.getElementById('eps'); //Nan

const numEtnias = 6;

fecha_nacimiento.addEventListener('change', function () {
    var fechaNacimiento = new Date(fecha_nacimiento.value);
    var fechaActual = new Date();
    var edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
    if (fechaActual.getMonth() < fechaNacimiento.getMonth() || (fechaActual.getMonth() === fechaNacimiento.getMonth() && fechaActual.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    e_edad.value = edad;
});


step1FormUpdate.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";fullfily
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


    addErrorMsg(e_documento.value === "" || e_documento.value.trim().length < 4, "Por favor verifique el documento", e_documento);
    addErrorMsg(e_nombre.value.trim() === "" || e_nombre.value.trim().length < 4, "Compruebe el nombre", e_nombre);
    addErrorMsg(!moment(fechaValor.value, 'YYYY-MM-DD', true).isValid(), "La fecha está en el formato incorrecto", fecha_nacimiento);
    addPreventiveMsg(e_direccion.value === "", "La dirección está vacía ¿Continuar?", e_direccion);
    addPreventiveMsg(e_barrio.value === "", "El barrio está vacío ¿Continuar?", e_barrio);
    addPreventiveMsg(e_hijos.value === "", "La cantidad de hijos está vacia, será reemplazada por 0", e_hijos);
    addErrorMsg(isNaN(e_etnia.value), "Etnia no posee un valor numérico" || e_etnia.value < 0  || e_etnia.value > numEtnias, e_etnia)

});


