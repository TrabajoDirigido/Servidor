/**
 * Created by Camila Alvarez on 24-11-2015.
 */
$('#document').ready(function() {
    div = $('#lab_div');
    div.append($('<br>'));
    div.append($('<label>Laboratory:</label>'));
    generate_select_lab();
    add_options_to_select($('#select_lab'),labs);
    $('#section_select option[value='+seccion+']').attr("selected", "selected");
    $('#select_lab option[value='+lab+']').attr("selected", "selected");
    createPagination(page_number);
    fill_table(table)
});


function createPagination(page_number){
    $("#paginator").jui_pagination({
        totalPages: page_number,
        currentPage: 1,
        disableSelectionNavPane: true,
        onChangePage: function (event, page_num) {
            if (isNaN(page_num) || page_num <= 0) {
                alert('Página inválida' + ' (' + page_num + ')');
            } else {
                $.ajax({
                    type: "GET",
                    url:"/lab_control/change_page_results/",
                    data:{page: page_num,
                        seccion: $('#section_select').val(),
                        lab: $('#select_lab').val()} ,
                    success: function(data) {
                        $('#tbody').empty();
                        fill_table(data);
                    }
                });
            }
        }
    });
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
        $('#tbody').empty();
        fill_table(data['first_lab']);
        $("#nav_pane_paginator").jui_pagination('destroy');
        createPagination(data['page_number']);
    });
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

function loadLabData(){
    $.ajax({
        method: "GET",
        url: "/lab_control/get_table_for_lab/",
        data: { lab: $('#select_lab').val() }
    })
    .success(function( data ) {
        $('#tbody').empty();
        fill_table(data['lab']);
        $("#nav_pane_paginator").jui_pagination('destroy');
        createPagination(data['page_number']);
    });
}

function fill_table(data){
    body=$('#tbody');
    html = "";
    for(key in data){
        dict = data[key];
        row = '<tr>';
        row += '<td>'+dict['name']+'</td>'+
            '<td>'+dict['value']+'</td>';
        row += '</tr>';
        html+=row;
    }
    body.append(html);
}
