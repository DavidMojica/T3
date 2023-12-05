const sp_edad = document.getElementById('sp_edad');
const hpcForm = document.getElementById('hpcForm');

const sp_ulco = document.getElementById('sp_ulco');
const cs_fu = document.getElementById('cs_fu');

hpcForm.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";
    let preventiveBan = true;
    let preventiveMsg = "";
    let toDangerBg = [];
    let toWarningBg = [];
    var formatoFecha = /^(\d{4})-(\d{2})-(\d{2})$/;

    if (!formatoFecha.test(cs_fu.value)) cs_fu.value = null;
    if (!formatoFecha.test(sp_ulco.value)) sp_ulco.value = null;
    if(sp_edad.value == "") sp_edad.value = 0;


    if(ban){
        if(preventiveBan){
            hpcForm.submit();
        }
    }
});
