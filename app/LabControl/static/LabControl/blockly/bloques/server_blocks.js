function studentsQuantity(option, self){
    if(option == "ONE"){
        if(self.getInput('ALUMNO')){
            self.removeInput('ALUMNO');
        }
        self.appendValueInput('ALUMNO')
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("student")
            .setCheck('STUDENT');
    }
    else if(option == "LIST"){
        if(self.getInput('ALUMNO')){
            self.removeInput('ALUMNO');
        }
        self.appendValueInput('ALUMNO')
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("students")
            .setCheck('STUDENTARRAY');
    }
    else if (option == "ALL" && self.getInput('ALUMNO')) {
      self.removeInput('ALUMNO');
    }
  }


//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#8m9cvs
Blockly.Blocks['serverget'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Get For");
    this.appendStatementInput("QUERY")
        .setCheck(["GETBOOLEAN", "GETOBJECT", "GETCOMPARABLE", "COUNT", "LOGIC", "MIN", "MAX"])
        .appendField("Query");

    var dropdown = new Blockly.FieldDropdown([["All", "ALL"], ["One", "ONE"], ["List", "LIST"]], function(option) {
      this.sourceBlock_.updateShape_(option);
    });

    this.appendDummyInput()
        .appendField("to")
        .appendField(dropdown, "STUDENTS");
    this.setColour(230);
    this.setTooltip('');
    this.setPreviousStatement(true, "SERVERTOPLEVEL");
    this.setHelpUrl('http://www.example.com/');
  },

  updateShape_: function(option){
    studentsQuantity(option,this);
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#kmy8wn
Blockly.Blocks['serverfilter'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Filter For");
    this.appendValueInput("VAR")
        .setCheck(["Boolean", "Number"])
        .appendField("condition")
        .appendField(new Blockly.FieldDropdown([["Equal", "equal"], ["Not Equal", "not_equal"]]), "CONDITION");
    this.appendStatementInput("QUERY")
        .setCheck(["LOGIC","COUNT","MIN","MAX"])
        .appendField("Query");

    var dropdown = new Blockly.FieldDropdown([["All", "ALL"], ["One", "ONE"], ["List", "LIST"]], function(option) {
      this.sourceBlock_.updateShape_(option);
    });

    this.appendDummyInput()
        .appendField("to")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(dropdown, "STUDENTS");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "SERVERFILTER");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  },

  updateShape_: function(option){
    studentsQuantity(option,this);
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#wfuac9
Blockly.Blocks['servercount'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Count Results");
    this.appendStatementInput("QUERY")
        .setCheck("SERVERFILTER")
        .appendField("Filter by");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "SERVERTOPLEVEL");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['servermin'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Min Of");
    this.appendStatementInput("QUERY")
        .setCheck(["SERVERFILTER","COUNT","MIN","MAX"])
        .appendField("Query");

    var dropdown = new Blockly.FieldDropdown([["All", "ALL"], ["One", "ONE"], ["List", "LIST"]], function(option) {
      this.sourceBlock_.updateShape_(option);
    });

    this.appendDummyInput()
        .appendField("to")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(dropdown, "STUDENTS");
    this.setPreviousStatement(true, "SERVERTOPLEVEL");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  },

  updateShape_: function(option){
    studentsQuantity(option,this);
  }
};

Blockly.Blocks['servermax'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Max Of");
    this.appendStatementInput("QUERY")
        .setCheck(["SERVERFILTER","COUNT","MIN","MAX"])
        .appendField("Query");

    var dropdown = new Blockly.FieldDropdown([["All", "ALL"], ["One", "ONE"], ["List", "LIST"]], function(option) {
      this.sourceBlock_.updateShape_(option);
    });

    this.appendDummyInput()
        .appendField("to")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(dropdown, "STUDENTS");
    this.setPreviousStatement(true, "SERVERTOPLEVEL");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  },

  updateShape_: function(option){
    studentsQuantity(option,this);
  }
};