const btn_turn_180 = document.getElementById('btn_turn_180');
const turn_card = document.getElementById('id-turn-card');
const turn_card_inner = document.getElementById('id-turn-card-inner');
const turn_card_front = document.getElementById('turn-card-front');
const turn_card_back = document.getElementById('turn-card-back');
const btn_turn_0 = document.getElementById('btn-turn-0');


btn_turn_180.addEventListener('click', function(){
    turn_card_inner.style.transform = "rotateY(180deg)";
});

btn_turn_0.addEventListener('click', function(){
    turn_card_inner.style.transform = "rotateY(0deg)";
});