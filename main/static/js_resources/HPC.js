//Step 1
const in_documento = document.getElementById('in_documento');
const step0Form = document.getElementById('step0Form');
const step1Msg = document.getElementById('step1Msg');

step0Form.addEventListener('submit', function(e){
    e.preventDefault();
    ban = true;
    msg = "";
    let toDangerBg = [];
    
    if(in_documento.value.trim() == ""){
        msg += "Ingrese el documento del paciente";
        ban = false;
        toDangerBg.push(in_documento);
    }

    if(ban){
        step0Form.submit();
    } else{
        changeBg(toDangerBg, 'bg-danger');
        step1Msg.innerHTML = msg;
        setTimeout(() => {
            naturalizeBg(toDangerBg, 'bg-danger');
            step1Msg.innerHTML = "";
        }, 4000);
    }
});
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