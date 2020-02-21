function deleteForm(btn) {
    'use strict';
    btn.closest('.form-group').remove();
    var forms = document.getElementsByClassName('input-group');
    document.getElementById('id_form-TOTAL_FORMS').setAttribute('value', forms.length);
    for (var i = 0; i < forms.length; i++) {
        var form_inputs = forms.item(i).getElementsByTagName('input');
        for (var j = 0; j < form_inputs.length; j++) {
            var regexp = new RegExp('form-\\d+');
            if (form_inputs[j].name) {form_inputs[j].name = form_inputs[j].name.replace(regexp, 'form-' + i);}
            if (form_inputs[j].id) {form_inputs[j].id = form_inputs[j].id.replace(regexp, 'form-' + i);}
        }
        forms.item(i).getElementsByTagName('span')[0].innerHTML = (i + 1).toString();
    }
}


function addForm() {
    'use strict';
    var el = document.getElementById('id_form-TOTAL_FORMS');
    var counter = parseInt(el.getAttribute('value'));

    var new_div = document.createElement('div');
    new_div.className = 'form-group';
    new_div.innerHTML =
        '<div class="input-group">'+
            '<div class="input-group-prepend bg-scheduler-dark-2">'+
                '<span class="input-group-text px-2 bg-scheduler-dark-3 c-scheduler">' + (counter + 1).toString() + '</span>'+
            '</div>'+
            '<input type="text" name="form-' + (counter).toString() + '-name" maxlength="100" class="form-control bg-scheduler-dark-3" id="id_form-' + (counter).toString() + '-name">'+
            '<input type="hidden" name="form-' + (counter).toString() + '-status" value="False" id="id_form-' + (counter).toString() + '-status">'+
            '<div class="input-group-append bg-scheduler-dark-2">'+
                '<button onclick="deleteForm(this)" type="button" class="btn btn-danger px-3 delete-form-row">-</button>'+
            '</div>'+
        '</div>';
    document.getElementById('fields-wrapper').appendChild(new_div);

    document.getElementById('id_form-TOTAL_FORMS').setAttribute('value', (counter + 1).toString());
}
