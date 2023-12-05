const sp_edad = document.getElementById('sp_edad');
const hpcForm = document.getElementById('hpcForm');

hpcForm.addEventListener('submit', function(e){
    e.preventDefault();
    let ban = true;
    let msg = "";
    let preventiveBan = true;
    let preventiveMsg = "";
    let toDangerBg = [];
    let toWarningBg = [];

    if(sp_edad.value == "") sp_edad.value = 0;

    if(ban){
        if(preventiveBan){
            hpcForm.submit();
        }
    }
});
