// rnapuzzles/static/js/puzzles/createForm.js

function updateAttr(action, element, attr_name, num) {
    parts = element.attr(attr_name).split('-', 3);
    if (action == 'add') {
        num = parseInt(parts[1]) + 1;
    }
    element.attr(attr_name, parts[0] + '-' + num + '-' + parts[2]);
}

$(document).ready(function() {

    var forms = $('.file-form-container');
    $('#id_form-TOTAL_FORMS').val(forms.length);

    $('#id_puzzle_info').val($("#id_choice :selected").val());

    $(this).on('click', '.add-file-form', function() {

        // create a clone of the existing form element with blank fields and updated attributes
        $('div.file-form-container:last').clone().each(function() {
            $(this).find('input').each(function() {
                $(this).val('');
                updateAttr('add', $(this), 'id', null);
                updateAttr('add', $(this), 'name', null);
            });

            $(this).find('label').each(function() {
                updateAttr('add', $(this), 'for', null);
            });

            $(this).find('div.form-group').each(function() {
                updateAttr('add', $(this), 'id', null);
            });

        }).appendTo('div#file-form-wrapper');

        $('div.file-form-container:last').prev('div.file-form-container').find('.btn.add-file-form')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-file-form').addClass('remove-file-form')
        .html('Delete')

        // Increment the TOTAL_FORMS
        $('#id_form-TOTAL_FORMS').val(parseInt($('#id_form-TOTAL_FORMS').val()) + 1);
    });

    $(this).on('click','.remove-file-form',function() {
        if (parseInt($('#id_form-TOTAL_FORMS').val()) > 1) {
            $(this).closest('.file-form-container').remove();

            var forms = $('.file-form-container');
            $('#id_form-TOTAL_FORMS').val(forms.length);

            for (var i=0, formCount=forms.length; i < formCount; i++) {
                $(forms.get(i)).find('input').each(function() {
                    updateAttr('remove', $(this), 'id', i);
                    updateAttr('remove', $(this), 'name', i);
                });

                $(forms.get(i)).find('label').each(function() {
                    updateAttr('remove', $(this), 'for', i);
                });

                $(forms.get(i)).find('div.form-group').each(function() {
                    updateAttr('remove', $(this), 'id', i);
                });
            }
        }
    });

    $('#id_choice').change(function(e) {
        $('#id_puzzle_info').val($("#id_choice :selected").val());
    });

    /*  change "Choose file" to chosen file's filename
        doesn't work on dynamically added elements, only original form from FilesFormset */

    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        $(e.target).siblings('.custom-file-label').text(fileName);
    });
});