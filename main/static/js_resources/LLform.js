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
const subtBtn = document.getElementById('subtBtn');


const numTiposDocumento = 8;
const numSexos = 3;
const numEps = 36;
const numPaises = 1;

form_llamadas.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";
    let toDangerBg = [];
    let preventiveBan = true;
    let preventiveMsg = "";
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

    addErrorMsg(in_nombre.value.trim() === "", "El nombre no puede estar vacío", in_nombre);
    addErrorMsg(in_documento.value.trim() === "", "El documento no puede estar vacío", in_documento);
    addErrorMsg(in_tipo_documento.value < 1 || in_tipo_documento.value > numTiposDocumento, "Compruebe tipo de documento", in_tipo_documento);
    addErrorMsg(in_sexo.value < 1 || in_sexo.value > numSexos, "Compruebe el sexo", in_sexo);
    addPreventiveMsg(in_edad.value.trim() === "" || isNaN(in_edad.value.trim()), "Edad no especificada ¿Quiere continuar?", in_edad);
    addErrorMsg(in_eps.value.trim() < 1 || in_eps > numEps, "Si el paciente no tiene eps, seleccione 'Ninguna'", in_eps);
    addPreventiveMsg(in_direccion.value.trim() === "", "Dirección no especificada ¿Quiere continuar?", in_direccion);
    addPreventiveMsg(in_telefono.value.trim() === "" || isNaN(in_telefono.value.trim()), "Teléfono no especificado ¿Quiere continuar?", in_telefono);
    addErrorMsg(in_poblacion_vulnerable.value < 1, "Si el paciente no es población vulnerable seleccione 'Ninguna'", in_poblacion_vulnerable);
    addPreventiveMsg(in_observaciones.value === "", "Observaciones vacías ¿Continuar?", in_observaciones);
    addPreventiveMsg(in_seguimiento24.value !== "", "¿Quiere proporcionar información de seguimiento (24h) desde ahora?", in_seguimiento24);
    addPreventiveMsg(in_seguimiento48.value !== "", "¿Quiere proporcionar información de seguimiento (48h) desde ahora?", in_seguimiento48);
    addPreventiveMsg(in_seguimiento72.value !== "", "¿Quiere proporcionar información de seguimiento (72h) desde ahora?", in_seguimiento72);

    coms.className = "";

    if (ban) {
        if (preventiveBan) {
            form_llamadas.submit();
        } else {
            coms.classList.add('text-warning', 'mt-3', 'card');
            coms.innerHTML = preventiveMsg;
            changeBg(toWarningBg, 'bg-warning');

            subtBtn.classList.remove('btn-danger');
            subtBtn.classList.add('btn', 'btn-warning');
            
            subtBtn.addEventListener('click', function(){
                if(in_edad.value === "") in_edad.value = 0;

                form_llamadas.submit();
            });

            setTimeout(() => {
                naturalizeBg(toWarningBg, 'bg-warning')
            }, 15000);
        }
    } else {
        coms.classList.add('text-danger', 'mt-3', 'card');
        coms.innerHTML = msg;
        changeBg(toDangerBg, 'bg-danger');

        setTimeout(() => {
            naturalizeBg(toDangerBg, 'bg-danger')
        }, 7000);

        setTimeout(() => {
            coms.classList.remove('card');
            coms.innerHTML = "";
        }, 7000);
    }   
});

