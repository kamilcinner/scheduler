function previous_week_shift() {
    'use strict';
    var counter = parseInt(document.getElementById('id_week_shift').getAttribute('value')) - 1;
    document.getElementById('id_week_shift').setAttribute('value', counter.toString());
}


function next_week_shift() {
    'use strict';
    var counter = parseInt(document.getElementById('id_week_shift').getAttribute('value')) + 1;
    document.getElementById('id_week_shift').setAttribute('value', counter.toString());
}


document.getElementById("previous-week-btn").addEventListener("click", previous_week_shift);
document.getElementById("next-week-btn").addEventListener("click", next_week_shift);