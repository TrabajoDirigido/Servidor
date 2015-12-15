/**
 * Blockly Demos: Plane Seat Calculator Blocks
 *
 * Copyright 2013 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Blocks for Blockly's Plane Seat Calculator application.
 * @author fraser@google.com (Neil Fraser)
 */
'use strict';

function genericGetInit(self, name){
  self.appendDummyInput()
      .appendField(name);
  self.appendValueInput("sheet")
      .setCheck(["Number", "String"])
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("sheet");
  self.appendValueInput("x")
      .setCheck("String")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("x");
  self.appendValueInput("y")
      .setCheck("String")
      .setAlign(Blockly.ALIGN_RIGHT)
      .appendField("y");
  self.setInputsInline(false);
  self.setPreviousStatement(true, "GETCOMPARABLE");
  self.setColour(120);
  self.setTooltip('');
}

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#nas6zq
Blockly.Blocks['getdouble'] = {
  init: function() {
    genericGetInit(this, "Get Double");
  }
};

Blockly.Blocks['getboolean'] = {
  init: function() {
    genericGetInit(this, "Get Boolean");
    this.setPreviousStatement(true, "GETBOOLEAN");
  }
};

Blockly.Blocks['getstring'] = {
  init: function() {
    genericGetInit(this, "Get String");
  }
};

Blockly.Blocks['getformula'] = {
  init: function() {
    genericGetInit(this, "Get Formula");
  }
};

Blockly.Blocks['getobject'] = {
  init: function() {
    genericGetInit(this, "Get Object");
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#zawz2w



Blockly.Blocks['filterobject'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Filter Any");
    this.appendDummyInput()
        .appendField("Condition")
        .appendField(new Blockly.FieldDropdown([["Equal", "EQUAL"], ["Not Equal", "NOTEQUAL"]]), "CONDITION");
    this.appendValueInput("NAME")
        .setCheck(["Boolean", "String", "Number", "NULL"])
        .appendField("Value");
    this.appendStatementInput("ARG1")
        .setCheck(["GETOBJECT","GETCOMPARABLE", "GETBOOLEAN"])
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Get Any");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "FILTEROBJECT");
    this.setColour(200);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#wqyhex
Blockly.Blocks['filtercomparable'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Filter Comparable");
    this.appendDummyInput()
        .appendField("Condition")
        .appendField(new Blockly.FieldDropdown([["Equal", "EQUAL"], ["Not Equal", "NOTEQUAL"]]), "CONDITION");
    this.appendValueInput("NAME")
        .setCheck(["Boolean", "String", "Number", "NULL"])
        .appendField("Value");
    this.appendStatementInput("ARG1")
        .setCheck("GETCOMPARABLE", "GETBOOLEAN")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Get Comparable");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "FILTERCOMPARABLE");
    this.setColour(200);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#77pp82
Blockly.Blocks['count'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Count");
    this.appendStatementInput("FILTER")
        .setCheck(["FILTERCOMPARABLE", "FILTEROBJECT"])
        .appendField("Filter");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "COUNT");
    this.setColour(180);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};


//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#64tdh7
//old var

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#8442qw
Blockly.Blocks['equal'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Equal");
    this.appendStatementInput("ARG1")
        .setCheck(["FILTERCOMPARABLE", "FILTEROBJECT", "GETOBJECT", "GETCOMPARABLE", "GETBOOLEAN", "VAR", "SORT", "EQUAL"])
        .appendField("Arg1");
    this.appendStatementInput("ARG2")
        .setCheck(["FILTERCOMPARABLE", "FILTEROBJECT", "GETOBJECT", "GETCOMPARABLE", "GETBOOLEAN", "VAR", "SORT", "EQUAL"])
        .appendField("Arg2");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "EQUAL");
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#gvo7uk
Blockly.Blocks['sort'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Sort");
    this.appendValueInput("NAME")
        .setCheck("Boolean")
        .appendField("Descendent");
    this.appendStatementInput("VALUES")
        .setCheck(["FILTERCOMPARABLE", "GETCOMPARABLE", "GETBOOLEAN", "EQUAL"])
        .appendField("Values");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "SORT");
    this.setColour(65);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#2uvw96
Blockly.Blocks['and'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("And");
    this.appendStatementInput("VALUES")
        .setCheck(["EQUAL", "LOGICLIST", "GETBOOLEAN"])
        .appendField("Values");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "LOGIC");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#g4n3eu
Blockly.Blocks['or'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Or");
    this.appendStatementInput("VALUES")
        .setCheck(["EQUAL", "LOGICLIST", "GETBOOLEAN"])
        .appendField("Values");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "LOGIC");
    this.setColour(230);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['min'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Min");
    this.appendStatementInput("VALUES")
        .setCheck(["EQUAL", "GETCOMPARABLE", "FILTERCOMPARABLE", "GETBOOLEAN"])
        .appendField("Values");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "MIN");
    this.setColour(10);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['max'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Max");
    this.appendStatementInput("VALUES")
        .setCheck(["EQUAL", "GETCOMPARABLE", "FILTERCOMPARABLE", "GETBOOLEAN"])
        .appendField("Values");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "MAX");
    this.setColour(10);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['existchart'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Exists Chart");
    this.appendValueInput("sheet")
        .setCheck(["String", "Number"])
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("sheet");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "GETBOOLEAN");
    this.setColour(110);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['chartdata'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Chart Data")
        .appendField(new Blockly.FieldDropdown([["tittle", "tittle"], ["xLabel", "xLabel"], ["yLabel", "yLabel"], ["series", "series"], ["type", "type"]]), "NAME");
    this.appendValueInput("sheet")
        .setCheck(["String", "Number"])
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("sheet");
    this.setInputsInline(false);
    this.setPreviousStatement(true, "GETCOMPARABLE");
    this.setColour(110);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['null'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Null");
    this.setInputsInline(false);
    this.setOutput(true, "NULL");
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};