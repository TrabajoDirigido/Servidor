Blockly.Blocks['subquery'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Subquery");
    var dropdown = new Blockly.FieldDropdown(dynamicOptions, function(option) {
      this.sourceBlock_.updateType_(option);
    });
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(dropdown, "QUERY");

    if(dynamicOptions()[0][1]!=null){
        var statementType = getStatementType(dynamicOptions()[0][1]);
        this.setPreviousStatement(true, statementType);
    }
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  },

  updateType_: function(option){
    if(option){
        if(this.previousConnection.targetConnection!=null)
          this.previousConnection.disconnect();
        this.setPreviousStatement(true, getStatementType(option));
    }
  }
};

Blockly.Blocks['subquerycreator'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Subquery Creator");
    this.appendDummyInput()
        .appendField("name")
        .appendField(new Blockly.FieldTextInput("name"), "NAME");
    this.appendStatementInput("QUERY")
        .setCheck(null)
        .appendField("query");
    this.appendDummyInput()
        .appendField("Create Input")
        .appendField(new Blockly.FieldCheckbox("FALSE"), "CREATE");
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
    this.ready_ = true;
    this.isNew_ = true;
  },

  onchange: function() {
    if (this.getFieldValue('CREATE') === 'TRUE') {
        var query = Blockly.JavaScript.statementToCode(this, 'QUERY');
        var name = this.getFieldValue('NAME')
        addSubqueryCode(name,query);

        var block = this.getInputTargetBlock('QUERY');
        subQueriesTypes[name] = block.previousConnection.getCheck();
        if(this.isNew_){
            subQueriesList.push([name,name]);
            this.isNew_ = false;
        }
    }
  }
};