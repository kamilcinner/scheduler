function is_leap_year() {
    'use strict';
    var selector = document.getElementById('id_year');
    var year = parseInt(selector.options[selector.selectedIndex].value);

    if (year % 4 === 0) {
        if (year % 100 === 0) {
            if (year % 400 === 0) {return  true;}
        }
        else {return true;}
    }
    return false;
}


function validate_day_form() {
    'use strict';
    var selector = document.getElementById('id_month');
    var month = parseInt(selector.options[selector.selectedIndex].value);

    var day = document.getElementById('id_day');
    var last_day = parseInt(day.options[day.length-1].value);

    const lesser_months = [2,4,6,9,11];
    var good_last_day;

    if (lesser_months.includes(month)) {
        if (month === 2) {
            if (is_leap_year())
                {good_last_day = 29;}
            else
                {good_last_day = 28;}
        } else {good_last_day = 30;}
    } else {good_last_day = 31;}

    while (last_day > good_last_day) {
        day.remove(last_day-1);
        last_day--;
    }
    while (last_day < good_last_day) {
        last_day++;
        day.innerHTML += '<option value="' + last_day + '">' + last_day + '</option>';
    }
}


document.getElementById('id_month').addEventListener("change", validate_day_form);
document.getElementById('id_year').addEventListener("change", validate_day_form);

validate_day_form();
