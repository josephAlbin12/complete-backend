
// SOMETHING TO NOTE
// For some reason, the global variables listed below only seem 
// to have values when printed inside the Airtable list, retrieve, update segments of code
// if you go outside of it and print, you just get it's original definition
// in this case, we get empty arrays

// ALSO, it seems to be a bit buggy, sometimes it ends the script without even running everything

// CURRENTLY, only checking for UT EID and Event to be matching
// NEED to add time and sign-in/out checking
// In the future, maybe consider blacklisting for each event so no duplicates
var Airtable = require('airtable');
var base = new Airtable({apiKey: 'keyYlHLddpShtr8mH'}).base('app1uoqBzrNjrnB28');
var attendance = [];
var organizations = [];
var retrievedOrgs = []

base('E-Week Attendance').select({
    view: 'Attendance Grid View',
    cellFormat: "json",
}).firstPage(function(err, records) {
    if (err) { console.error(err); return; }
    records.forEach(function(record) {
    	// console.log(typeof test);
    	// console.log(record);
    	// add each record object to main object array
        attendance.push(record);
    });
    // console.log(attendance);
    
    // beginning of validation script
    // brute force method: can look into optimization after MVP
    for (var i = 0; i < attendance.length; i++) {
    	var id1 = attendance[i].get('UT EID');
    	var event1 = attendance[i].get('Event');
    	// console.log(id1);
    	// console.log(event1);

    	for (var j = i + 1; j < attendance.length; j++) {
    		var id2 = attendance[j].get('UT EID');
    		var event2 = attendance[j].get('Event');

    		if (id1 == id2 && event1 == event2) {
    			console.log("Success!");
    			organizations.push(attendance[i].get('Organization'));
    		}
    	}
    }
});


base('Leaderboard').select({
    view: 'Grid view',
    cellFormat: "json"
}).firstPage(function(err, records) {
    if (err) { console.error(err); return; }
    records.forEach(function(record) {
    // get records
    retrievedOrgs.push(record);
    });
    // console.log(retrievedOrgs);
    // start adding points
    for (var a = 0; a < organizations.length; a++) {
    	for (var b = 0; b < retrievedOrgs.length; b++) {
    		if (organizations[a] == retrievedOrgs[b].get('Organization')) {
    			// add 1 point for current org
    			console.log("Yeet!");
    			var thisID = retrievedOrgs[b].getId();
    			console.log(thisID);
    			var thisAttendanceScore = retrievedOrgs[b].get('Attendance');
    			thisAttendanceScore++;
    			console.log(thisAttendanceScore);

			    base('Leaderboard').update(thisID, {
			    "Attendance": thisAttendanceScore
			}, function(err, record) {
			  if (err) {
			    console.error(err);
			    return;
			  }
			  console.log("Successfully added attendance point!");
			});
    		}
    	}
    }
});






