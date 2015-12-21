
function getArray(mString){
  if(!mString){
    return "[]";
  }

  mString = mString.substring(1, mString.length-1);
  var arr = mString.split(",");

  var res = [];
  var i;
  for(i=0; i < arr.length; i++) {
    if(arr[i]==".."){
      res.push(arr[i]);
    }
    else{
      res.push(parseInt(arr[i]));
    }
  }
  return JSON.stringify(res);
}

function createJsonVar(value){
  if(!value){
    throw "Null value";
  }
  if(value == "NoNeNULLNoNe"){
    return '{"type":"null"}';
  }
  value = value.split("'").join("\"");
  var res = '{"var":'+value+',';
  if (typeof eval(value) === 'string' || eval(value) instanceof String)
    res += '"type":"string"}';
  else if (typeof eval(value) === 'boolean')
    res += '"type":"boolean"}';
  else
    res += '"type":"int"}';
  return res;
}

function genericGet(block, type){
  var value_sheet = Blockly.JavaScript.valueToCode(block, 'sheet', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var value_x = Blockly.JavaScript.valueToCode(block, 'x', Blockly.JavaScript.ORDER_ATOMIC);
  var value_y = Blockly.JavaScript.valueToCode(block, 'y', Blockly.JavaScript.ORDER_ATOMIC);

  var sheet = createJsonVar(value_sheet);

  var x = '"x":'+getArray(value_x);
  var y = '"y":'+getArray(value_y);
  
  var code = '{"method":"get",'+
        '"type":"'+type+'",'+
        '"sheet":'+sheet+','+
        x+','+
        y+'}';
     
  return code;
}

Blockly.JavaScript['get'] = function(block) {
  var type = block.getFieldValue('TYPE');
  return genericGet(block, type);
};


function genericFilter(block){
  var dropdown_condition = block.getFieldValue('CONDITION');
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_arg1 = Blockly.JavaScript.statementToCode(block, 'ARG1');
  
  var type;
  if(dropdown_condition=="EQUAL")
    type = 'equal';
  else
    type = 'not_equal';

  var mVar = createJsonVar(value_name);

  var code = '{"method":"filter",'+
        '"type":"'+type+'",'+
        '"var":'+mVar+','+
        '"vals":'+statements_arg1+'}';

  return code;
}

Blockly.JavaScript['filtercomparable'] = function(block) {
  return genericFilter(block);
};

Blockly.JavaScript['filterobject'] = function(block) {
  return genericFilter(block);
};

Blockly.JavaScript['count'] = function(block) {
  var statements_filter = Blockly.JavaScript.statementToCode(block, 'FILTER');
  var code = '{"method":"count",'+
        '"vals":'+statements_filter+'}';
  return code;
};

Blockly.JavaScript['null'] = function(block) {
  return ["NoNeNULLNoNe",Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['existchart'] = function(block) {
  var value_sheet = Blockly.JavaScript.valueToCode(block, 'sheet', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var sheet = createJsonVar(value_sheet);

  var code = '{"method":"existChart",'+
        '"sheet":'+sheet+'}';
  return code;
};

Blockly.JavaScript['chartdata'] = function(block) {
  var value_sheet = Blockly.JavaScript.valueToCode(block, 'sheet', Blockly.JavaScript.ORDER_ATOMIC) || '0';
  var sheet = createJsonVar(value_sheet);

  var type = block.getFieldValue('NAME');
  
  var code = '{"method":"dataChart",'+
        '"type":"'+type+'",'+
        '"sheet":'+sheet+'}';
  return code;
};

Blockly.JavaScript['equal'] = function(block) {
  var statements_arg1 = Blockly.JavaScript.statementToCode(block, 'ARG1');
  var statements_arg2 = Blockly.JavaScript.statementToCode(block, 'ARG2');
  
  var code = '{"method":"compare",'+
        '"arg1":'+statements_arg1.trim()+','+
        '"arg2":'+statements_arg2.trim()+'}';
  return code;
};

Blockly.JavaScript['sort'] = function(block) {
  var value_name = Blockly.JavaScript.valueToCode(block, 'NAME', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_values = Blockly.JavaScript.statementToCode(block, 'VALUES');

  var des = createJsonVar(value_name);
  
  var code = '{"method":"sort",'+
        '"des":'+des+','+
        '"vals":'+statements_values.trim()+'}';
  return code;
};

function genericLogic(block, type){
  var statements_values = Blockly.JavaScript.statementToCode(block, 'VALUES');
  var code = '{"method":"logic",'+
        '"type":"'+type+'",'+
        '"vals":'+statements_values.trim()+'}';
  return code;
}

function genericMinMax(block, type){
  var statements_values = Blockly.JavaScript.statementToCode(block, 'VALUES');
  var code = '{"method":"'+type+'",'+
        '"vals":'+statements_values.trim()+'}';
  return code;
}

Blockly.JavaScript['and'] = function(block) {
  return genericLogic(block, "and");
};

Blockly.JavaScript['or'] = function(block) {
  return genericLogic(block, "or");
};

Blockly.JavaScript['min'] = function(block) {
  return genericMinMax(block, "min");
};

Blockly.JavaScript['max'] = function(block) {
  return genericMinMax(block, "max");
};