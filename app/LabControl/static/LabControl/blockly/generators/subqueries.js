Blockly.JavaScript['subquery'] = function(block) {
    var dropdown_query = block.getFieldValue('QUERY');
    return getSubqueryCode(dropdown_query);
};