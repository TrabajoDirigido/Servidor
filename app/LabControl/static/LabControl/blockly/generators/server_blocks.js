function addForProperty(block, jsonString, option){
  var jsonQuery = JSON.parse(jsonString);
  if(option == "ALL"){
    jsonQuery["for"] = "all";
  }
  else if(option == "ONE"){
    var students = Blockly.JavaScript.valueToCode(block, 'ALUMNO', Blockly.JavaScript.ORDER_NONE) || "[]";
    jsonQuery["for"] = students;
  }
  else{
    var students = Blockly.JavaScript.valueToCode(block, 'ALUMNO') || "[]";
    jsonQuery["for"] = students.split(",");
  }

  return JSON.stringify(jsonQuery);
}

Blockly.JavaScript['serverget'] = function(block) {
  var statements_query = Blockly.JavaScript.statementToCode(block, 'QUERY');
  var dropdown_students = block.getFieldValue('STUDENTS');
  
  return addForProperty(block, statements_query, dropdown_students);
};

Blockly.JavaScript['serverfilter'] = function(block) {
  var statements_query = Blockly.JavaScript.statementToCode(block, 'QUERY');
  var dropdown_students = block.getFieldValue('STUDENTS');

  var query = addForProperty(block, statements_query, dropdown_students);

  var code = '{"method":"filter",'+
        '"var":"'+createJsonVar(Blockly.JavaScript.valueToCode(block, 'VAR', Blockly.JavaScript.ORDER_ATOMIC))+'",'+
        '"type":"'+block.getFieldValue('CONDITION')+'",'+
        '"vals":'+query+'}';

  return code;
};

Blockly.JavaScript['servercount'] = function(block) {
  var statements_query = Blockly.JavaScript.statementToCode(block, 'QUERY');
  var code = '{"method":"count",'+
        '"vals":'+statements_query+'}';
  return code;
};

Blockly.JavaScript['servermin'] = function(block) {
  var statements_query = Blockly.JavaScript.statementToCode(block, 'QUERY');
  var dropdown_students = block.getFieldValue('STUDENTS');

  var query = addForProperty(block, statements_query, dropdown_students);

  var code = '{"method":"min",'+
        '"vals":'+query+'}';
  return code;
};

Blockly.JavaScript['servermax'] = function(block) {
  var statements_query = Blockly.JavaScript.statementToCode(block, 'QUERY');
  var dropdown_students = block.getFieldValue('STUDENTS');

  var query = addForProperty(block, statements_query, dropdown_students);

  var code = '{"method":"max",'+
        '"vals":'+query+'}';
  return code;
};