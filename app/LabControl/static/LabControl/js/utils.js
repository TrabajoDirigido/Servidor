/**
 * Created by Camila Alvarez on 24-11-2015.
 */
$(document).ready(function() {
    $("#datepicker").datepicker();
});


function loadResults(name, seccion){
    form = $('#form');
    AddParameter(form, "name", name);
    AddParameter(form, "seccion", seccion);

    //Send the Form
    form[0].submit();
}

function AddParameter(form, name, value) {
    var $input = $("<input />").attr("type", "hidden")
        .attr("name", name)
        .attr("value", value);
    form.append($input);
}