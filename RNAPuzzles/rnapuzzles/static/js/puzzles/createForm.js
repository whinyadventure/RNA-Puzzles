// initial values

$('.file-form-container:not(:first)').each(function(){
    changeButtonVal($(this));
});

var forms = $('.file-form-container');

$('#id_form-TOTAL_FORMS').val(forms.length);

$('#id_puzzle_info').val($("#id_choice :selected").val());


// helper functions
function changeButtonVal(form_div) {

    form_div.find('.btn.add-file-form')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-file-form').addClass('remove-file-form')
        .html('<i class="fa fa-minus"></i> Delete');

}


function updateAttr(action, element, attr_name, num) {

    var attr = $(this).attr(attr_name);

        parts = element.attr(attr_name).split('-', 3);
        if (action == 'add') {
            num = parseInt(parts[1]) + 1;
        }
        element.attr(attr_name, parts[0] + '-' + num + '-' + parts[2]);
}


// add file form
$(document).on('click', '.add-file-form', function() {

    //var first_in_empty = $('input[type=file]:not([value])').closest('.file-form-container').clone(true);
    var $new_clone = $('div.file-form-container:first').clone(true);

    $new_clone.each(function() {
        $(this).find('input').each(function() {
            $(this).val('');
            updateAttr('add', $(this), 'id', null);
            updateAttr('add', $(this), 'name', null);

        });

        $(this).find('label').each(function() {
            updateAttr('add', $(this), 'for', null);
        });

        $(this).find('.custom-file-label').text('Choose file');

        $(this).find('div.form-group').each(function() {
            updateAttr('add', $(this), 'id', null);
        });
    });

    $new_clone.prependTo('#file-form-wrapper');

    changeButtonVal($('div.file-form-container:first').next('div.file-form-container'));

    // Increment the TOTAL_FORMS
    $('#id_form-TOTAL_FORMS').val(parseInt($('#id_form-TOTAL_FORMS').val()) + 1);
});


// delete file form
$(document).on('click', '.remove-file-form', function() {
    if (parseInt($('#id_form-TOTAL_FORMS').val()) > 1) {
        $(this).closest('.file-form-container').remove();

        var forms = $('.file-form-container');
        $('#id_form-TOTAL_FORMS').val(forms.length);

        for (var i=0, id=forms.length-1; i <= id; i++, id--) {
            $(forms.get(i)).find('input').each(function() {
                updateAttr('delete', $(this), 'id', id);
                updateAttr('delete', $(this), 'name', id);
            });

            $(forms.get(i)).find('label').each(function() {
                updateAttr('delete', $(this), 'for', id);
            });

            $(forms.get(i)).find('div.form-group').each(function() {
                updateAttr('delete', $(this), 'id', id);
            });
        }
    }
});


// change events
$('#id_choice').on('change', function() {
    $('#id_puzzle_info').val($("#id_choice :selected").val());
});


$('input[type="file"]').on('change', function() {
    $(this).next('label').text($(this).val().split('\\').pop());
})