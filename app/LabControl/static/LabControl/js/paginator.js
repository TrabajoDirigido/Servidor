
$(function() {
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
                    url:"/lab_control/change_page/",
                    data:{page: page_num} ,
                    success: function(data) {
                        $('#tbody').empty();
                        buildTable(data);
                    }
                });
            }
        }
    });
});

function buildTable(data){
    body=$('#tbody');
    html = "";
    for(key in data){
        dict = data[key];
        click = 'onclick="loadResults(\''+dict.name+'\',\''+dict.seccion+'\')"';
        row = '<tr>';
        row += '<td>'+dict.name+'</td>'+
            '<td>'+dict.seccion+'</td>'+
            '<td>'+dict.date+'</td>';
        row += '<td><a '.concat(click,'style="cursor:pointer" >Results </a></td>');
        row += '</tr>';
        html+=row;
    }
    body.append(html);
}
