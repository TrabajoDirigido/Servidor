/**
 * Created by Camila Alvarez on 01-12-2015.
 */

function parseQuery(){
    var result = [];
    parseRecursive($("#start"),result);
    var form = $('#form');
    var name =  $('#id_query_name').val();
    result[0].AS =  name;
    AddParameter(form, "name", name);
    AddParameter(form, "lab", $('#select_lab').val());
    AddParameter(form, "query", JSON.stringify(result[0]));

    form[0].submit();
}

function parseRecursive(div,result){
    div.children('select').each(function(){
        if($(this).val()=='BOOLEAN' || $(this).val()=='STRING' || $(this).val()=='NUMERIC'){
            labels = div.children('label');
            labels.each(function(){
                if($(this).text()=="VALOR: ")
                    input = $(this).attr('for');
            });
            vals = $('#'+input).val();
            vals= vals.split(",");
            for(i=0;i<vals.length;i++){
                vals[i]=vals[i].trim();
            }
            result.push(vals);

        }
        else if($(this).val()=='ASCENDENTE' || $(this).val()=='DESCENDENTE'){
            val = false;
            if($(this).val()=='DESCENDENTE'){
                val = true;
            }
            result.push(val);
        }
        else if($(this).val()=='EQUAL_TRUE'){
            vals = {type: 'equal', var: true};
            result.push(vals);
        }
        else if($(this).val()=='EQUAL_FALSE' ){
            vals = {type: 'equal', var: false};
            result.push(vals);
        }
        else if($(this).val()=='CONDITION_EQUAL' || $(this).val()=='CONDITION_NOT_EQUAL' ){
            labels = div.children('label');
            labels.each(function(){
                if($(this).text()=="VALOR: ")
                    input = $(this).attr('for');
            });
            vals = {type: $(this).val().substr(10).toLowerCase(), var: $('#'+input).val()};
            result.push(vals);
        }
        else if($(this).val()=='GET_BOOLEAN' || $(this).val()=='GET_NUMERIC' ||
            $(this).val()=='GET_STRING' || $(this).val()=='GET_FORMULA' ||
            $(this).val()=='GET_OBJECT'){
            labels = div.children('label');
            var select_for=null;
            var for_value = null;
            var input_x, input_y,input_sheet;
            labels.each(function(){
                if($(this).text()=="X: ")
                    input_x = $(this).attr('for');
                else if($(this).text()=="Y: ")
                    input_y = $(this).attr('for');
                else if($(this).text()=='HOJA:')
                    input_sheet = $(this).attr('for');
                else if($(this).text()=='OBJETIVO:')
                    select_for = $(this).attr('for');
            });

            var x = $('#'+input_x).val();
            x= x.split(",");
            for(i=0;i<x.length;i++){
                x[i]= x[i].trim();
            }

            var y = $('#'+input_y).val();
            y= y.split(",");
            for(i=0;i<y.length;i++){
                y[i]= y[i].trim();
            }

            var sheet = $('#'+input_sheet).val();
            if(select_for)
                for_value = $('#'+select_for).val()=='TODOS' ? 'all': $('#'+select_for).val();
            var type = $(this).val().substr(4).toLowerCase();

            var res = {method: 'get',
                      x: x,
                      y: y,
                      sheet: sheet
                      };

            if(type!='object')
                res.type=type;
            if(for_value)
                res.for=for_value;
            result.push(res);
        }
        else if($(this).val()=='FILTER' || $(this).val()=='GET' ||
           $(this).val()=='VAR' ||  $(this).val()=='GET_COMPARABLE' ||
            $(this).val()=='SERVER_FILTER' || $(this).val()=='SERVER_GET'){
            var new_div = $('#div_'+$(this).attr('id'));
            new_div.children('div').each(function(){
                parseRecursive($(this),result);
            });
        }
        else if($(this).val()=='AND|OR'){
            var new_div = $('#div_'+$(this).attr('id'));
            parseRecursive(new_div,result);

        }
        else if($(this).val()=='AND' || $(this).val()=='OR'){
            res ={};
            res.method='logic';
            res.type=$(this).val();
            var new_div = $('#div_'+$(this).attr('id'));
            res.vals=[];
            parseRecursive(new_div.children('div:first'), res.vals);
            if(res.vals.length == 1)
                res.vals= res.vals[0];
            labels = new_div.children('div:last-child').children('label');
            var select_for=null;
            var for_value = null;
            labels.each(function(){
                if($(this).text()=='OBJETIVO:') {
                    select_for = $(this).attr('for');
                }
            });
            if(select_for)
                for_value = $('#'+select_for).val()=='TODOS' ? 'all': $('#'+select_for).val();
            if(for_value)
                res.for=for_value;
            result.push(res);

        }
        else if($(this).val()=='EQUAL'){
            var res = {};
            res.method='compare';
            var new_div = $('#div_'+$(this).attr('id'));
            res.arg1=[];
            res.arg2=[];
            parseRecursive(new_div.children('div:first'),res.arg1);
            if(res.arg1.length == 1)
                    res.arg1= res.arg1[0];
            parseRecursive(new_div.children('div:nth-child(2)'),res.arg2);
            if(res.arg2.length == 1)
                    res.arg2= res.arg2[0];
            result.push(res);
        }
        else if($(this).val()=='SORT'){
            var res = {};
            res.method=$(this).val().toLowerCase();
            var new_div = $('#div_'+$(this).attr('id'));
            res.des=[];
            res.vals=[];
            parseRecursive(new_div.children('div:first'),res.des);
            if(res.des.length == 1)
                    res.des= res.des[0];
            parseRecursive(new_div.children('div:nth-child(2)'),res.vals);
            if(res.vals.length == 1)
                    res.vals= res.vals[0];
            result.push(res)
        }
        else if( $(this).val()=='MIN' || $(this).val()=='MAX' ||
                $(this).val()=='SERVER_MIN' || $(this).val()=='SERVER_MAX'){
            var res = {};
            if($(this).val().length()==10)
                res.method=$(this).val().toLowerCase().substr(7);
            else
                res.method=$(this).val().toLowerCase();
            var new_div = $('#div_'+$(this).attr('id'));
            res.vals=[];
            parseRecursive(new_div.children('div:first'), res.vals);
            if(res.vals.length == 1)
                res.vals= res.vals[0];

            labels = new_div.children('div:last-child').children('label');
            var select_for=null;
            var for_value = null;
            labels.each(function(){
                if($(this).text()=='OBJETIVO:') {
                    select_for = $(this).attr('for');
                }
            });
            if(select_for)
                for_value = $('#'+select_for).val()=='TODOS' ? 'all': $('#'+select_for).val();
            if(for_value)
                res.for=for_value;
            result.push(res);
        }
        else if($(this).val()=='FILTER_COMPARABLE' || $(this).val()=='FILTER_OBJECT'
            || $(this).val()=='SERVER_FILTER_BOOL' || $(this).val()=='SERVER_FILTER_NUMERIC' ){
            var res = {};
            res.method='filter';
            var new_div = $('#div_'+$(this).attr('id'));
            res.filter=[];
            res.vals=[];
            var for_val=[];
            parseRecursive(new_div.children('div:first'),res.filter);
            if(res.filter.length == 1)
                    res.filter= res.filter[0];
            parseRecursive(new_div.children('div:nth-child(2)'),res.vals);
            if(res.vals.length == 1)
                    res.vals= res.vals[0];
            labels = new_div.children('div:last-child').children('label');
            var select_for=null;
            var for_value = null;
            labels.each(function(){
                if($(this).text()=='OBJETIVO:') {
                    select_for = $(this).attr('for');
                }
            });
            if(select_for)
                for_value = $('#'+select_for).val()=='TODOS' ? 'all': $('#'+select_for).val();
            if(for_value)
                res.for=for_value;
            result.push(res);
        }
        else if($(this).val()=='COUNT' || $(this).val()=='SERVER_COUNT'){
            var res = {};
            res.method='count';
            var new_div = $('#div_'+$(this).attr('id'));
            res.vals=[];
            var for_val=[];
            parseRecursive(new_div.children('div:first'), res.vals);
            if(res.vals.length == 1)
                res.vals= res.vals[0];
            labels = new_div.children('div:last-child').children('label');
            var select_for=null;
            var for_value = null;
            labels.each(function(){
                if($(this).text()=='OBJETIVO:') {
                    select_for = $(this).attr('for');
                }
            });
            if(select_for)
                for_value = $('#'+select_for).val()=='TODOS' ? 'all': $('#'+select_for).val();
            if(for_value)
                res.for=for_value;

            result.push(res);
        }

    });

    return result;

}