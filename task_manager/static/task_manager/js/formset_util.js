// function addForm() {
//     var el = document.getElementById('id_form-TOTAL_FORMS');
//     var counter = parseInt(el.getAttribute('value'));
//     $('.fields-wrapper').append(
//         '<div class="form-group">'+
//         '<div class="input-group">'+
//         '<div class="input-group-prepend bg-scheduler">'+
//         '<span class="input-group-text px-2 bg-scheduler-dark c-scheduler">' + (counter + 1) + '</span>'+
//         '</div>'+
//         '<input type="text" name="form-' + counter + '-name" maxlength="100" class="form-control bg-scheduler-dark" id="id_form-' + counter + '-name">'+
//         '<input type="hidden" name="form-' + counter + '-status" counterue="False" id="id_form-' + counter + '-status">'+
//         '<div class="input-group-append bg-scheduler">'+
//         '<button type="button" class="btn btn-danger px-3 delete-form-row">-</button>'+
//         '</div>'+
//         '</div>'+
//         '</div>'
//     );
//     counter += 1;
//     el.setAttribute('value', counter);
//     $('.delete-form-row').click(function(){
//         deleteForm(this)
//     });
// }
// function deleteForm(el) {
//     $(el).closest('.form-group').remove();
//     var forms = $('.input-group');
//     $('#id_form-TOTAL_FORMS').val(forms.length);
//     for (var i = 0, formCount = forms.length; i < formCount; i++) {
//         $(forms.get(i)).find(':input').each(function () {
//             var regexp = new RegExp('form-\\d+');
//             if (el.name) el.name = el.name.replace(regexp, 'form-' + i);
//             if (el.id) el.id = el.id.replace(regexp, 'form-' + i)
//         });
//         $(forms.get(i)).find('span').html(i + 1);
//     }
// }
// $(document).ready(function(){
//     $('.add-form-row').click(function(){
//         addForm()
//     });
//     $('.delete-form-row').click(function(){
//         deleteForm(this)
//     });
// });