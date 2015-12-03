/**
 * Created by Camila Alvarez on 20-11-2015.
 */
$('#document').ready(function() {
    query_select = $('#0-0');
    addDefaultOption(query_select);
    for(i = 0; i<options.length;i++){
        query_select.append($('<option>',{
            value: options[i],
            text: options[i]
        }));
    }
    $.fn.exists = function () {
        return this.length !== 0;
    };
    div = $('#lab_div');
    div.append($('<br>'));
    div.append($('<label>Laboratorio:</label>'));
    generate_select_lab();
    add_options_to_select($('#select_lab'),labs);
    $('#section_select option:first-child').attr("selected", "selected");
});

function generateColor(){
    return '#'+Math.floor(Math.random()*16777215).toString(16);
}

function addDefaultOption(select){
    $("<option />", {value: 'ELIJA UNA OPCION', text: 'ELIJA UNA OPCION'}).appendTo(select);
}
var id_query_select = 1;

function addCloseArgument(div,argument,j,id,color,parent){
    index = j+parent;
   if(argument) {
        $('<br id="br_close_'+id+'-'+index+'" class=' +id+'-'+index+ ' />').appendTo(div);
        $('<label id="label_'+id+'-'+index+'" class='+id+'-'+index+' style="color:'+color+
            '" for=' + id_query_select + ' > ] </label>')
            .insertAfter($('#br_close_'+id+'-'+index));
    }
}

function addSelectArgument(div,argument,j,id,color,parent) {
    index = j+parent;
    if(argument) {
        new_line = $('<br id="br_'+id+'-'+index+'" class=' +id+'-'+index+ ' />');
        new_line.appendTo(div);
        new_label= $('<label id="label_open_'+id+'-'+index+'" class=' +id+'-'+index+ ' style="color:' +color+
            '" for=' + id_query_select + ' >' + argument[j] + '</label>')
                    .insertAfter($('#br_'+id+'-'+index));
        $('<br  class=' +id+'-'+index+ ' />').insertAfter(new_label);
    }
}

function loadQueryArguments(){
    query_select = $('#0-0');
    select_value = query_select.val();

    div_sub_query = $('#div_0-0');
    refreshDiv(div_sub_query);
    if(select_value == 'GET'){
        style="";
        div_sub_query.attr('style', "");
    }
    else{
        style="padding-left: 40px;";
        div_sub_query.attr('style', "padding-left: 40px;");
    }


    div_sub_query.find('select, input, label, br, button').remove();

    if(!(select_value in query_dict)){
        return;
    }
    arguments = argument_dict[select_value];
    next_select = query_dict[select_value];
    for(j=0; j<next_select.length;j++) {
        color = generateColor();
        arg_div=$('<div style="'+style+'" id="div_arg_'+id_query_select+'-'+j+'" ></div>').appendTo(div_sub_query);
        addSelectArgument(arg_div,arguments,j,0, color,0);
        addCloseArgument(arg_div,arguments,j,0, color,0);
        addSelect(arg_div, next_select[j],j,0,0);
    }

}


function deleteEntry(id){
    $('#'+id).remove();
    $('#but_'+id).remove();
    $('br').remove("."+id);
}

function loadAndOr(id){
    div = $('#div_'+id);
    if(!div.exists()){
        div = $('<div id="div_'+id+'" ></div>').insertAfter($('#but_'+id));
    }

    addSelect(div, and_or,0, parent,pure_id);
    new_id = id_query_select-1;
    $('<button id="but_'+new_id+'-'+parent+'" onclick="deleteEntry(\''+new_id+'-'+parent+'\'); return false">-</button>')
        .insertAfter($('#'+new_id+'-'+parent));
}


function loadSubQueryOptions(id){
    parent = parseInt(id.substr(id.indexOf('-')+1));
    pure_id = parseInt(id.substr(0,id.indexOf('-')));
    div_sub_query = $('#div_0-0');
    selected_sub_query = $('#'+id);
    var style = "padding-left: 40px;";

    div = $('#div_'+id);
    refreshDiv(div);
    $('#but_'+id).remove();
    div.remove();

    if(selected_sub_query.val()=='AND|OR'){
        $('<button id="but_'+id+'" onclick="loadAndOr(\''+id+'\'); return false">+</button>').insertAfter($('#'+id));
        return
    }



    key = $('#'+id+" option:selected").text();
    if(!(key in query_dict)){
        if(key=='ELIJA UNA OPCION')
            return;
        return loadSubQueryArguments(id,div_sub_query,parent,pure_id);
    }
    new_div = $('<div style="padding-left:40px;" id="div_'+id+'" ></div>').insertAfter(selected_sub_query);

    if(["GET","GET_COMPARABLE","GET_OBJECT", "FILTER", "AND|OR",'VAR'].indexOf(selected_sub_query.val())>=0){
        style = "";
        new_div.attr('style', "");
    }
    next_select = query_dict[key];
    arguments = argument_dict[key];

    div = new_div;
    for(j=0; j<next_select.length;j++) {
        arg_div=$('<div style="'+style+'" id="div_arg_'+id_query_select+'-'+(j+parent)+'" ></div>').appendTo(new_div);
        color = generateColor();
        addSelectArgument(arg_div,arguments, j, pure_id,color,parent);
        addCloseArgument(arg_div,arguments,j,pure_id,color,parent);
        addSelect(arg_div, next_select[j],j, parent,pure_id);

    }
}

function addSelect(div_sub_query,next_select,j,parent,par_id){
    index = j+parent;
    id= id_query_select;
    previous_selector = $('#label_'+par_id+'-'+parent);
    new_select = $("<select id="+id+'-'+index+
        " name=\"query[]\" class="+id+'-'+index+" onchange=loadSubQueryOptions(\""+id+'-'+index+"\") />");
    new_line = $('<br class='+id+'-'+index+' />');

    if(!previous_selector.exists()) {
        new_line.appendTo(div_sub_query);
        new_select.insertAfter(new_line);
    }
    else {
        new_select.insertAfter($('#br_close_' + par_id+'-'+index));
        new_line.insertAfter(new_select);
    }

    id_query_select++;
    addDefaultOption(new_select);
    for (i = 0; i < next_select.length; i++) {
        $("<option />", {value: next_select[i], text: next_select[i]}).appendTo(new_select);
    }
}


function loadSubQueryArguments(id,div,parent,par_id){
    selected_subquery = $('#'+id);
    new_id= id_query_select;
    arguments = argument_dict[selected_subquery.val()];
    for(i=0; i<arguments.length;i++){
        $('<br id="arg_'+new_id+'" class="'+new_id+'-'+parent+'" />').insertAfter(selected_subquery);
        after = $('#arg_'+new_id);
        $('<br class='+new_id+' />').insertBefore(after);

        if(arguments[i]=='OBJETIVO:'){
            $('<label id="obj_'+id_query_select+'" class="'+id_query_select+'-'+parent+'" for="'+id_query_select+'-'+parent+'" >' + arguments[i]+'</label>').insertAfter(after);
            new_select= $("<select id='"+id_query_select+
               '-'+parent+"' name=\"query[]\" class='"+id_query_select+'-'+parent+"' />")
             .insertAfter($('#obj_'+id_query_select));
            //Se piden los alumnos conectados
            $("<option />", {value: 'TODOS', text: 'TODOS'}).appendTo(new_select);
            id_query_select++;
            continue;
        }

        $('<label class="'+id_query_select+'-'+parent+'" for="'+id_query_select+'-'+parent+'" >' + arguments[i]+'</label>'+
            '<input type="text" id="'+id_query_select+'-'+parent+'" class="'+id_query_select+
            '-'+parent+'" size="20" name="query[]" value="" placeholder="" />').insertAfter(after);
        id_query_select++;

    }
}

function refreshDiv(div){
    $('select, input', div).each(function(){
        id_query_select--;
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