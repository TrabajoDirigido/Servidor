var subQueries = {};
var subQueriesList = [];
var subQueriesTypes = {};

function dynamicOptions(){
    if(subQueriesList == false){
        return [["", null]];
    }
	return subQueriesList;
}

function getStatementType(name){
    return subQueriesTypes[name];
}

function getSubqueryCode(name){
	return subQueries[name];
}