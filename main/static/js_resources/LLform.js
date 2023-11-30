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

    if(in_nombre.value.trim() === ""){
        ban = false
        msg += "El nombre no puede estar vacío";
    }

    if(in_documento.value.trim() === ""){
        ban = false;
        msg += "El documento no puede estar vacío";
    }

    if(in_tipo_documento.value < 1 || in_tipo_documento.value > numTiposDocumento){
        ban = false;
        msg += "Compruebe tipo de documento";
    }

    if(in_sexo.value < 1 || in_sexo.value > numSexos){
        ban = false;
        msg += "Compruebe el sexo";
    }

    if(in_edad.value.trim() == "" || isNaN(in_edad.value.trim())){
        preventiveBan = false;
        preventiveMsg += "Edad no especificada ¿Quiere continuar?";
    }

    if(in_eps.value.trim() < 1 || in_eps > numEps){
        ban = false;
        msg += "Si el paciente no tiene eps, seleccione 'Ninguna'";
    }

    if(in_direccion.value.trim() === ""){
        preventiveBan = false;
        preventiveMsg += "Dirección no especificada ¿Quiere continuar?";
    }

    if(in_pais.value != numPaises){
        ban = false;
        msg += "Comprobar pais";
    }

    if(in_departamento.value < 1){
        ban = false;
        msg += "Comprobar departamento";
    }

    if(in_municipio.value < 1){
        ban = false;
        msg += "Comprobar ciudad";
    }

    if(in_telefono.value.trim() === "" || isNaN(in_telefono.value.trim())){
        preventiveBan = false;
        msg += "Telefono no especificado ¿Quiere continuar?";
    }

    if(in_poblacion_vulnerable.value < 1){
        ban = false;
        msg += "Si el paciente no es poblacion vulnerable seleccione 'Ninguna'";
    }

    if(in_observaciones.value === ""){
        preventiveBan = false;
        preventiveMsg += "Observaciones vacías ¿Continuar?";
    }

    if(in_seguimiento24.value != ""){
        preventiveBan = false;
        preventiveMsg += "¿Quiere proporcionar informacion de seguimiento (24h) desde ahora?";
    }

    if(in_seguimiento48.value != ""){
        preventiveBan = false;
        preventiveMsg += "¿Quiere proporcionar informacion de seguimiento (48h) desde ahora?";
    }
    
    if(in_seguimiento72.value != ""){
        preventiveBan = false;
        preventiveMsg += "¿Quiere proporcionar informacion de seguimiento (72h) desde ahora?";
    }

    if(ban){

        if(preventiveBan){
            form_llamadas.submit();
        }
        else{
            coms.textContent = preventiveMsg;
        }
    }
    else{
        coms.textContent = msg;
    }
});

