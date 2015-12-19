/**
 * Created by Camila Alvarez on 01-12-2015.
 */

function parseQuery(code){
    var result = [];
    var form = $('#form');
    var name =  $('#id_query_name').val();

    if (name=="" || name==null){
        alert("Please name your query");
        return;
    }
    AddParameter(form, "name", name);
    AddParameter(form, "lab", $('#select_lab').val());
    AddParameter(form, "query", code);

    form[0].submit();
}
