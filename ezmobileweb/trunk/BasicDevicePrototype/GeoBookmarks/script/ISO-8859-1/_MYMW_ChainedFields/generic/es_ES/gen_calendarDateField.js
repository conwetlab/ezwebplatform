/**
    -                    ***MyMobileWeb***
    - Java Script code generated by MyMobileWeb Generation Proccess
    - Date: Fri Jun 13 11:27:58 GMT+01:00 2008
    - Note: DO NOT TOUCH
**/

function _smt_npr_onsubmit_gen_validate() { 

 // Validate control: _MYMW_DATE_MON__MYMW_Calendar_VAL
 if(document.forms[0]._MYMW_DATE_MON__MYMW_Calendar_VAL) {

	var v_MYMW_DATE_MON__MYMW_Calendar = trim(document.forms[0]._MYMW_DATE_MON__MYMW_Calendar_VAL.value);
	if(v_MYMW_DATE_MON__MYMW_Calendar != "") {

	// Validate Format .. 
	if ( ( v_MYMW_DATE_MON__MYMW_Calendar.length < 1 ) || ( v_MYMW_DATE_MON__MYMW_Calendar.length > 2 ) ) {
		alert(messageFormat(getMessage('MyMobileWeb_Month_Date'),new Array()));
		return false;
	}

	// Validate Types .. 
	if(!isInteger(v_MYMW_DATE_MON__MYMW_Calendar)) {
		alert(messageFormat(getMessage('MyMobileWeb_Month_Date'),new Array()));
		return false;
	}

	// Validate Ranges ..

	var _MYMW_DATE_MON__MYMW_Calendar = parseInt(v_MYMW_DATE_MON__MYMW_Calendar, 10);

	if( (_MYMW_DATE_MON__MYMW_Calendar < 1) || (_MYMW_DATE_MON__MYMW_Calendar > 12) ) {

	alert(messageFormat(getMessage('MyMobileWeb_Month_Date'),new Array()));
		return false;
	}

	}
 }

 // Validate control: _MYMW_DATE_YEA__MYMW_Calendar_VAL
 if(document.forms[0]._MYMW_DATE_YEA__MYMW_Calendar_VAL) {

	var v_MYMW_DATE_YEA__MYMW_Calendar = trim(document.forms[0]._MYMW_DATE_YEA__MYMW_Calendar_VAL.value);
	if(v_MYMW_DATE_YEA__MYMW_Calendar != "") {

	// Validate Format .. 
	if ( ( v_MYMW_DATE_YEA__MYMW_Calendar.length < 1 ) || ( v_MYMW_DATE_YEA__MYMW_Calendar.length > 4 ) ) {
		alert(messageFormat(getMessage('MyMobileWeb_Year_Date'),new Array()));
		return false;
	}

	// Validate Types .. 
	if(!isInteger(v_MYMW_DATE_YEA__MYMW_Calendar)) {
		alert(messageFormat(getMessage('MyMobileWeb_Year_Date'),new Array()));
		return false;
	}

	// Validate Ranges ..

	var _MYMW_DATE_YEA__MYMW_Calendar = parseInt(v_MYMW_DATE_YEA__MYMW_Calendar, 10);

	if( (_MYMW_DATE_YEA__MYMW_Calendar < 1) || (_MYMW_DATE_YEA__MYMW_Calendar > 9999) ) {

	alert(messageFormat(getMessage('MyMobileWeb_Year_Date'),new Array()));
		return false;
	}

	}
 }

 // Validate control: _MYMW_DATE_DAY__MYMW_Calendar_VAL
 if(document.forms[0]._MYMW_DATE_DAY__MYMW_Calendar_VAL) {

	var v_MYMW_DATE_DAY__MYMW_Calendar = trim(document.forms[0]._MYMW_DATE_DAY__MYMW_Calendar_VAL.value);
	if(v_MYMW_DATE_DAY__MYMW_Calendar != "") {

	// Validate Format .. 
	if ( ( v_MYMW_DATE_DAY__MYMW_Calendar.length < 1 ) || ( v_MYMW_DATE_DAY__MYMW_Calendar.length > 2 ) ) {
		alert(messageFormat(getMessage('MyMobileWeb_Day_Date'),new Array()));
		return false;
	}

	// Validate Types .. 
	if(!isInteger(v_MYMW_DATE_DAY__MYMW_Calendar)) {
		alert(messageFormat(getMessage('MyMobileWeb_Day_Date'),new Array()));
		return false;
	}

	// Validate Ranges ..

	var _MYMW_DATE_DAY__MYMW_Calendar = parseInt(v_MYMW_DATE_DAY__MYMW_Calendar, 10);

	if( (_MYMW_DATE_DAY__MYMW_Calendar < 1) || (_MYMW_DATE_DAY__MYMW_Calendar > 31) ) {

	alert(messageFormat(getMessage('MyMobileWeb_Day_Date'),new Array()));
		return false;
	}

	}
 }

 // Validate control: _MYMW_Calendar_VAL
 if(document.forms[0]._MYMW_Calendar_VAL) {

 }

 if(typeof _smt_npr_onsubmit_validate == 'function') { var result = _smt_npr_onsubmit_validate(); } 


 if ( result ) return true;
 else return false;

}
