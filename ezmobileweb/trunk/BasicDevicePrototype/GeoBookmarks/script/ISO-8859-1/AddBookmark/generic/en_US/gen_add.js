/**
    -                    ***MyMobileWeb***
    - Java Script code generated by MyMobileWeb Generation Proccess
    - Date: Fri Jun 13 11:27:58 GMT+01:00 2008
    - Note: DO NOT TOUCH
**/

function _smt_npr_onsubmit_gen_validate() { 

	var resul = add_onsubmit_gen_validate();
	if (resul) { return true; } else { return false; }

}

function add_onsubmit_gen_validate() { 

 // Validate control: bookmarkType_VAL
 if(document.forms[0].bookmarkType_VAL) {

 }

 // Validate control: bookmarkName_VAL
 if(document.forms[0].bookmarkName_VAL) {

	var vbookmarkName = trim(document.forms[0].bookmarkName_VAL.value);
	if(vbookmarkName != "") {

	// Validate Format .. 
	if ( ( vbookmarkName.length < 0 ) || ( vbookmarkName.length > 100 ) ) {
		var parameters = new Array('Name:','0','100');
		alert(messageFormat(getMessage('MyMobileWeb_E_Min_Max_Length'),parameters));
		return false;
	}

	}
 }

 // Validate control: bookmarkLocation_VAL
 if(document.forms[0].bookmarkLocation_VAL) {

	var vbookmarkLocation = trim(document.forms[0].bookmarkLocation_VAL.value);
	if(vbookmarkLocation != "") {

	// Validate Format .. 
	if ( ( vbookmarkLocation.length < 0 ) || ( vbookmarkLocation.length > 100 ) ) {
		var parameters = new Array('Location:','0','100');
		alert(messageFormat(getMessage('MyMobileWeb_E_Min_Max_Length'),parameters));
		return false;
	}

	}
 }

 if(typeof add_onsubmit_validate == 'function') { var result = add_onsubmit_validate(); } 


 if ( result ) return true;
 else return false;

}