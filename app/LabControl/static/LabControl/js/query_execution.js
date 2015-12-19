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
    get_all_subqueries();
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var subqueries;

function get_all_subqueries(){
    $.ajax({
        method: "POST",
        data: {csrfmiddlewaretoken: csrftoken},
        url: "/lab_control/get_all_subquery/"
    })
    .success(function( data ) {
            subqueries = data;
    });
}

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