Blockly.JavaScript['var'] = function(block) {
  var code = new Array(block.itemCount_);
  for (var n = 0; n < block.itemCount_; n++) {
    var temp = Blockly.JavaScript.valueToCode(block, 'ADD' + n,
        Blockly.JavaScript.ORDER_COMMA) || 'null';
    code[n] = temp.split("'").join("\"");
  }
  var res = '[' + code.join(',') + ']';
  return res;
};

Blockly.JavaScript['student'] = function(block) {
  var dropdown_student = block.getFieldValue('STUDENT');
  return [dropdown_student, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['studentlist'] = function(block) {
  var code = new Array(block.itemCount_);
  for (var n = 0; n < block.itemCount_; n++) {
    code[n] = Blockly.JavaScript.valueToCode(block, 'ADD' + n,
        Blockly.JavaScript.ORDER_NONE) || 'null';
  }
  var res = code.join(',');
  return [res, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['lists_logic'] = function(block) {
  var code = new Array(block.itemCount_);
  for (var n = 0; n < block.itemCount_; n++) {
    code[n] = Blockly.JavaScript.statementToCode(block, 'ADD' + n);
  }
  var res = '[' + code.join(',') + ']';
  return res;
};