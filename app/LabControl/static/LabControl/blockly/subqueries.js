function dynamicOptions(){
	var subQueriesList = [];
	if(Object.keys(subqueries).length==0){
		return [["",null]];
	}
	for(var name in subqueries){
		subQueriesList.push([name,name]);
    }
    console.log("List:"+subQueriesList);
	return subQueriesList;
}

function getStatementType(name){
    return subqueries[name]["type"];
}

function getSubqueryCode(name){
	var query = subqueries[name]["query"];
	query = query.split("'").join("\"")
	return query;
}

function studentsList(){
	var list = [];

	var arrayLength = clients.length;
	if(arrayLength==0){
		return [["",null]];
	}
	for (var i = 0; i < arrayLength; i++) {
	    list.push([clients[i],clients[i]]);
	}
    return list;
}