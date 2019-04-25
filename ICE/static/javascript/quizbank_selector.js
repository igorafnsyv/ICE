let selected_banks = document.getElementsByClassName("bank");
let last_selected = -1;
function bankSelect(){
    if (last_selected != -1) {
        let elem = document.getElementById(last_selected);
        elem.checked = false;
    }
    for (let i = 0; i < selected_banks.length; i++) {
        if (selected_banks[i].checked) {
            last_selected = selected_banks[i].value;
        }
    }
}