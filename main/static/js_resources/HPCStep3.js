const step2FormUpdate = document.getElementById('step2FormUpdate');
const documento = document.getElementById('documento');
const tipo_documento = document.getElementById('tipo_documento');
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
const step3Error = document.getElementById('step3Error');
const submitBtn3 = document.getElementById('submitBtn3');

const numEtnias = 6;
const numOcupaciones = 8;
const numRegimenes = 6;
const numEps = 36;
const numTipoDocumentos = 8;
const numSexos = 3;
const numEstadosCivil = 6;
const numEscolaridades = 7;
const numLectoes = 4;
const numLectoesNiv = 6;
const numRa = 6;

fecha_nacimiento.addEventListener('change', function () {
    var fechaNacimiento = new Date(fecha_nacimiento.value);
    var fechaActual = new Date();
    var edadNum = fechaActual.getFullYear() - fechaNacimiento.getFullYear();
    if (fechaActual.getMonth() < fechaNacimiento.getMonth() || (fechaActual.getMonth() === fechaNacimiento.getMonth() && fechaActual.getDate() < fechaNacimiento.getDate())) {
        edadNum--;
    }
    edad.value = edadNum;
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
    
    addErrorMsg(raz_analitico.value.trim() <= 0 || raz_analitico.value.trim() > numRa, "Compruebe razonamiento analitico", raz_analitico);
    addErrorMsg(lectoescritura_nivel.value.trim() <= 0 || lectoescritura_nivel > numLectoesNiv, "Compruebe lectoescritura nivel", lectoescritura_nivel);
    addErrorMsg(lectoescritura.value.trim() <= 0 || lectoescritura.value.trim() > numLectoes, "Compruebe lectoescritura", lectoescritura);
    addErrorMsg(escolaridad.value.trim() <= 0 || escolaridad.value.trim() > numEscolaridades, "Compruebe escolaridad", escolaridad);
    addErrorMsg(estado_civil.value.trim() <= 0 || estado_civil.value.trim() > numEstadosCivil, "Compruebe estado civil", estado_civil);
    addErrorMsg(sexo.value.trim() <= 0 || sexo.value.trim() > numSexos, "Comrpuebe el sexo", sexo);
    addErrorMsg(tipo_documento.value.trim() <= 0 || tipo_documento.value.trim() > numTipoDocumentos, "Compruebe tipo de documento", tipo_documento);
    addErrorMsg(edad.value.trim() < 0 || isNaN(edad.value.trim()), "Error en la edad", edad);
    addErrorMsg(documento.value.trim() === "" || documento.value.trim().length < 4, "Por favor verifique el documento", documento);
    addErrorMsg(nombre.value.trim() === "" || nombre.value.trim().length < 4, "Compruebe el nombre", nombre);
    addErrorMsg(!moment(fecha_nacimiento.value.trim(), 'YYYY-MM-DD', true).isValid(), "La fecha está en el formato incorrecto", fecha_nacimiento);
    addPreventiveMsg(direccion.value.trim() === "", "La dirección está vacía ¿Continuar?", direccion);
    addPreventiveMsg(barrio.value.trim() === "", "El barrio está vacío ¿Continuar?", barrio);
    addPreventiveMsg(hijos.value.trim() === "", "La cantidad de hijos está vacia, será reemplazada por 0", hijos);
    addErrorMsg(isNaN(etnia.value.trim()) || etnia.value.trim() < 0  || etnia.value.trim() > numEtnias,"Dato erroneo en etnia.", etnia)
    addErrorMsg(isNaN(ocupacion.value.trim()) ||ocupacion.value.trim() < 0 ||ocupacion.value.trim() > numOcupaciones, "Dato erroneo en ocupacion.",ocupacion);
    addErrorMsg(isNaN(rss.value.trim()) || rss.value.trim() < 0 || rss.value.trim() > numRegimenes, "Dato erroneo en regimen", rss);
    addErrorMsg(isNaN(eps.value.trim()) || eps.value.trim() < 0 || eps.value.trim() > numEps, "Dato erroneo en Eps", eps); 

    step3Error.className = "";

    if (ban){
        if(preventiveBan){
            step2FormUpdate.submit();
        } else {
            step3Error.classList.add('text-warning', 'mt-3', 'card');
            step3Error.innerHTML = preventiveMsg;
            changeBg(toWarningBg, 'bg-warning');

            submitBtn3.classList.remove('btn-danger');
            submitBtn3.classList.add('btn', 'btn-warning');
            
            submitBtn3.addEventListener('click', function(){
                if(edad.value === "") edad.value = 0;
                if(hijos.value === "") hijos.value = 0;

                step2FormUpdate.submit();
            });

            setTimeout(() => {
                naturalizeBg(toWarningBg, 'bg-warning')
            }, 15000);
        }
    } else{
        step3Error.classList.add('text-danger', 'mt-3', 'card');
        step3Error.innerHTML = msg;
        changeBg(toDangerBg, 'bg-danger');

        setTimeout(() => {
            naturalizeBg(toDangerBg, 'bg-danger')
        }, 7000);

        setTimeout(() => {
            step3Error.classList.remove('card');
            step3Error.innerHTML = "";
        }, 7000);  
    }

})