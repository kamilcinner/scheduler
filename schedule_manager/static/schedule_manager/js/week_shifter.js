function previous_week_shift() {
    'use strict';
    document.getElementById('id_week_shift').setAttribute('value', -1);
}


function next_week_shift() {
    'use strict';
    document.getElementById('id_week_shift').setAttribute('value', 1);
}


function set_today_date() {
    'use strict';
    var today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    const yyyy = today.getFullYear();

    today = yyyy + '-' + mm + '-' + dd;
    document.getElementById('id_date').setAttribute('value', today);
}


function submit_form() {
    'use strict';
    document.getElementById('schedule-week-form').submit();
}


document.getElementById("previous-week-btn").addEventListener("click", previous_week_shift);
document.getElementById("next-week-btn").addEventListener("click", next_week_shift);
document.getElementById("current-week-btn").addEventListener("click", set_today_date);
document.getElementById('id_date').addEventListener('change', submit_form);