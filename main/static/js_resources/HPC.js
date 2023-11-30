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

