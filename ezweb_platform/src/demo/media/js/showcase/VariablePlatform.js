/* 
 * MORFEO Project 
 * http://morfeo-project.org 
 * 
 * Component: EzWeb
 * 
 * (C) Copyright 2004 Telefónica Investigación y Desarrollo 
 *     S.A.Unipersonal (Telefónica I+D) 
 * 
 * Info about members and contributors of the MORFEO project 
 * is available at: 
 * 
 *   http://morfeo-project.org/
 * 
 * This program is free software; you can redistribute it and/or modify 
 * it under the terms of the GNU General Public License as published by 
 * the Free Software Foundation; either version 2 of the License, or 
 * (at your option) any later version. 
 * 
 * This program is distributed in the hope that it will be useful, 
 * but WITHOUT ANY WARRANTY; without even the implied warranty of 
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
 * GNU General Public License for more details. 
 * 
 * You should have received a copy of the GNU General Public License 
 * along with this program; if not, write to the Free Software 
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA. 
 * 
 * If you want to use this software an plan to distribute a 
 * proprietary application in any way, and you are not licensing and 
 * distributing your source code under GPL, you probably need to 
 * purchase a commercial license of the product.  More info about 
 * licensing options is available at: 
 * 
 *   http://morfeo-project.org/
 */


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// VARIABLE (Parent Class)  <<PLATFORM>>
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function Variable (iGadget, name) {
	this.iGadget = null;
	this.name = null;
	this.aspect = null;
	this.value = null;
}

//////////////////////////////////////////////
// PARENT CONTRUCTOR (Super keyboard emulation)
//////////////////////////////////////////////
 
Variable.prototype.Variable = function (iGadget_, name_, aspect_, value_) {
    	this.iGadget = iGadget_;
    	this.name = name_;
	this.aspect = aspect_;
	this.value = value_;
}

//////////////////////////////////////////////
// PUBLIC METHODS TO BE INHERITANCED
//////////////////////////////////////////////

Variable.prototype.get = function () { }  

Variable.prototype.setHandler = function () { } 

GadgetVariable.prototype.set = function (value, wiring) { } 

//////////////////////////////////////////////
// PUBLIC CONSTANTS
//////////////////////////////////////////////

Variable.prototype.EVENT = "EVEN"  
Variable.prototype.SLOT = "SLOT"  
Variable.prototype.USER_PREF = "PREF"  
Variable.prototype.PROPERTY = "PROP"  

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// RVARIABLE (Derivated class) <<PLATFORM>>
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function RVariable(iGadget_, name_, aspect_, value_) {
	Variable.prototype.Variable.call(this, iGadget_, name_, aspect_, value_);
  
	this.handler = null;
}

//////////////////////////////////////////////
// DEFINING INHERITANCE
//////////////////////////////////////////////

RVariable.prototype = new Variable;

//////////////////////////////////////////////
// PUBLIC METHODS TO BE INHERITANCED
////////////////////////////////////////////// 

RVariable.prototype.writeSlot = function (newValue) { 
	switch (this.aspect){
		case Variable.prototype.SLOT:
			this.value = newValue;
			this.handler(newValue);
			break;
	}
}

//////////////////////////////////////////////
// OVERWRITTEN METHODS
//////////////////////////////////////////////

RVariable.prototype.setHandler = function (handler_) { 
	this.handler = handler_;
} 

RVariable.prototype.get = function () { 
	switch (this.aspect){
		case Variable.prototype.EXTERNAL_CONTEXT:
		case Variable.prototype.GADGET_CONTEXT:
		case Variable.prototype.USER_PREF:
		case Variable.prototype.SLOT:
			return this.value;
	}
}  



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// RWVARIABLE (Derivated class)
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function RWVariable(iGadget_, name_, aspect_, value_) {
	Variable.prototype.Variable.call(this, iGadget_, name_, aspect_, value_);
}

//////////////////////////////////////////////
// DEFINING INHERITANCE
//////////////////////////////////////////////

RWVariable.prototype = new Variable;

//////////////////////////////////////////////
// PUBLIC METHODS TO BE INHERITANCED
//////////////////////////////////////////////

RWVariable.prototype.set = function (value_, wiring) {  
  // Error control needed here!!!!!!!!
	switch (this.aspect){
		case Variable.prototype.PROPERTY:
		// PersistentEngine.guardar
		break;
		case Variable.prototype.EVENT:
		// PersistentEngine.guardar
			if (this.value != value_){
				wiring.sendEvent(this.iGadget, this.name, value_);
			}
		break;
	}
	this.value = value_;
}  

//////////////////////////////////////////////
// OVERWRITTEN METHODS
//////////////////////////////////////////////

RWVariable.prototype.get = function () {  
  // Error control needed here!!!!!!!!
	switch (this.aspect){
		case Variable.prototype.PROPERTY:
		return this.value;
		case Variable.prototype.EVENT:
		return this.value;
	}
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 

