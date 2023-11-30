const form_llamadas = document.getElementById('form-llamadas'); //o
const in_nombre = document.getElementById('in_nombre'); //o
const in_documento = document.getElementById('in_documento');//o
const in_tipo_documento = document.getElementById('in_tipo_documento');//o
const in_sexo = document.getElementById('in_sexo'); //o
const in_edad = document.getElementById('in_edad');
const in_eps = document.getElementById('in_eps'); //o-n
const in_direccion = document.getElementById('in_direccion');
const in_pais = document.getElementById('in_pais');
const in_departamento = document.getElementById('in_departamento');
const in_municipio = document.getElementById('in_municipio');
const in_telefono = document.getElementById('in_telefono');
const in_poblacion_vulnerable = document.getElementById('in_poblacion_vulnerable'); //o-n
const in_observaciones = document.getElementById('in_observaciones');
const in_seguimiento24 = document.getElementById('in_seguimiento24');
const in_seguimiento48 = document.getElementById('in_seguimiento48');
const in_seguimiento72 = document.getElementById('in_seguimiento72');
const coms = document.getElementById('coms');


const numTiposDocumento = 8;
const numSexos = 3;
const numEps = 36;
const numPaises = 1;

form_llamadas.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";
    let preventiveBan = true;
    let preventiveMsg = "";

    const addErrorMsg = (condition, errorMsg) => {
        if (condition) {
            ban = false;
            msg += errorMsg + "<br>";
        }
    };

    const addPreventiveMsg = (condition, preventiveErrorMsg) => {
        if (condition) {
            preventiveBan = false;
            preventiveMsg += preventiveErrorMsg + "<br>";
        }
    };

    addErrorMsg(in_nombre.value.trim() === "", "El nombre no puede estar vacío \n");
    addErrorMsg(in_documento.value.trim() === "", "El documento no puede estar vacío");
    addErrorMsg(in_tipo_documento.value < 1 || in_tipo_documento.value > numTiposDocumento, "Compruebe tipo de documento");
    addErrorMsg(in_sexo.value < 1 || in_sexo.value > numSexos, "Compruebe el sexo");
    addPreventiveMsg(in_edad.value.trim() === "" || isNaN(in_edad.value.trim()), "Edad no especificada ¿Quiere continuar?");
    addErrorMsg(in_eps.value.trim() < 1 || in_eps > numEps, "Si el paciente no tiene eps, seleccione 'Ninguna'");
    addPreventiveMsg(in_direccion.value.trim() === "", "Dirección no especificada ¿Quiere continuar?");
    addErrorMsg(in_pais.value != numPaises, "Comprobar país");
    addErrorMsg(in_departamento.value < 1, "Comprobar departamento");
    addErrorMsg(in_municipio.value < 1, "Comprobar ciudad");
    addPreventiveMsg(in_telefono.value.trim() === "" || isNaN(in_telefono.value.trim()), "Teléfono no especificado ¿Quiere continuar?");
    addErrorMsg(in_poblacion_vulnerable.value < 1, "Si el paciente no es población vulnerable seleccione 'Ninguna'");
    addPreventiveMsg(in_observaciones.value === "", "Observaciones vacías ¿Continuar?");
    addPreventiveMsg(in_seguimiento24.value !== "", "¿Quiere proporcionar información de seguimiento (24h) desde ahora?");
    addPreventiveMsg(in_seguimiento48.value !== "", "¿Quiere proporcionar información de seguimiento (48h) desde ahora?");
    addPreventiveMsg(in_seguimiento72.value !== "", "¿Quiere proporcionar información de seguimiento (72h) desde ahora?");

    coms.classList.remove();
    if (ban) {
        if (preventiveBan) {
            form_llamadas.submit();
        } else {
            coms.classList.add('text-warning', 'mt-3');
            coms.innerHTML = preventiveMsg;
        }
    } else {
        coms.classList.add('text-danger', 'mt-3');
        coms.innerHTML = msg;
    }
});

