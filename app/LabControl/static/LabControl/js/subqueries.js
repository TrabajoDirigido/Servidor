var subqueryList = [];

function dynamicOptions(){
	var options = subqueryList;
	return options;
}

function saveCreatedSubQuery(block, name){
	subqueryList[name] = block;
}

Blockly.Blocks['createsubquery'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Subquery");
    this.appendValueInput("NAME")
        .setCheck("String")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Name");
    this.appendStatementInput("QUERY");
    this.setInputsInline(false);
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.JavaScript['createsubquery'] = function(block) {

};