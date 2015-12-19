/**
 * Created by Camila Alvarez on 20-11-2015.
 */
$('#document').ready(function() {
    $.fn.exists = function () {
        return this.length !== 0;
    };
    div = $('#lab_div');
    div.append($('<br>'));
    div.append($('<label>Laboratory:</label>'));
    generate_select_lab();
    add_options_to_select($('#select_lab'),labs);
    $('#section_select option:first-child').attr("selected", "selected");
    $('#id_query_name').val('');
});

function generate_select_lab(){
    $('#lab_div').append($('<select id="select_lab" name="select_lab" onchange="loadLabData()">'));
}

function add_options_to_select(select,data){
    for(var key in data){
            select.append($('<option>',{
                value: key,
                text: data[key]
            }));
        }
}

$('#section_select').change(function(){
    div = $('#lab_div');
    div.find('select').remove();
    generate_select_lab();

    $.ajax({
        method: "GET",
        url: "/lab_control/get_labs_per_seccion/",
        data: { seccion: $(this).val() }
    })
    .success(function( data ) {
        new_select = $('#select_lab');
        add_options_to_select(new_select,data['labs']);
    });
});