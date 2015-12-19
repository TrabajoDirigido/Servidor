/**
 * Created by Camila Alvarez on 11-12-2015.
 */

$('#document').ready(function() {
    get_all_subqueries_name();
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
var names;
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

function get_all_subqueries_name(){
    $.ajax({
        method: "POST",
        data : {csrfmiddlewaretoken: csrftoken},
        url: "/lab_control/get_all_subquery_names/"
    })
    .success(function( data ) {
            names = data.names;
    });
}

/*function create_subquery(name, type, query){
    if(names.indexOf(name)!=-1){
        alert('Name already in use');
        return;
    }
    $.ajax({
        method: "POST",
        data : {csrfmiddlewaretoken: csrftoken,
                name: name,
                type: type,
                query: query},
        url: "/lab_control/create_sub_query/"
    })
    .success(function( data ) {
            get_all_subqueries_name();
            alert('Succesfully added Sub-Query');
    });
}*/

function create_subquery(name,type,query){
    if(names.indexOf(name)!=-1){
        alert('Name already in use');
        return;
    }
    var form = $('#form');
    AddParameter(form, "csrfmiddlewaretoken", csrftoken);
    AddParameter(form, "name", name);
    AddParameter(form, "query", query);
    AddParameter(form, "type", type);

    form[0].submit();
}

function AddParameter(form, name, value) {
    var $input = $("<input />").attr("type", "hidden")
        .attr("name", name)
        .attr("value", value);
    form.append($input);
}