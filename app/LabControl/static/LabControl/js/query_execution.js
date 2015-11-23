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
    }
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

    div_sub_query = $('#subquery_body');

    refreshDiv(div_sub_query);
    div_sub_query.find('select, input, label, br').remove();

    if(!(select_value in query_dict)){
        return;
    }
    arguments = argument_dict[select_value];
    next_select = query_dict[select_value];
    for(j=0; j<next_select.length;j++) {
        color = generateColor();
        addSelectArgument(div_sub_query,arguments,j,0, color,0);
        addCloseArgument(div_sub_query,arguments,j,0, color,0);
        addSelect(div_sub_query, next_select[j],j,0,0);
    }

}

function loadSubQueryOptions(id){
    parent = parseInt(id.substr(id.indexOf('-')+1));
    pure_id = parseInt(id.substr(0,id.indexOf('-')));
    div_sub_query = $('#subquery_body');

    console.log('before: '+id_query_select);
    div = $('#div_'+id);
    refreshDiv(div);
    console.log('after: '+id_query_select);
    div.remove();

    new_div = $('<div id="div_'+id+'" ></div>').insertAfter($('#'+id));

    key = $('#'+id+" option:selected").text();
    if(!(key in query_dict)){
        if(key=='ELIJA UNA OPCION')
            return;
        return loadSubQueryArguments(id,div_sub_query,parent,pure_id);
    }

    next_select = query_dict[key];
    arguments = argument_dict[key];

    div = new_div;
    for(j=0; j<next_select.length;j++) {
        arg_div=$('<div id="div_arg_'+id_query_select+'-'+j+'" ></div>').appendTo(new_div);
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
            $('<label id="obj_'+new_id+'" class="'+new_id+'-'+parent+'" for='+new_id+' >' + arguments[i]+'</label>').insertAfter(after);
            new_select= $("<select id='"+new_id+
               '-'+parent+"' name=\"query[]\" class='"+new_id+'-'+parent+"' />")
             .insertAfter($('#obj_'+new_id));
            //Se piden los alumnos conectados
            $("<option />", {value: 'TODOS', text: 'TODOS'}).appendTo(new_select);
            id_query_select++;
            continue;
        }

        $('<label class="'+new_id+'-'+parent+'" for='+new_id+' >' + arguments[i]+'</label>'+
            '<input type="text" id="'+new_id+'-'+parent+'" class="'+new_id+
            '-'+parent+'" size="20" name="query[]" value="" placeholder="" />').insertAfter(after);

        id_query_select++;

    }
}

function refreshDiv(div){
    $('select, input', div).each(function(){
        id_query_select--;
    });

}