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


/**
 * @author luismarcos.ayllon
 */
var MyClassFactory  = function () {

	// *********************************
	// SINGLETON INSTANCE
	// *********************************
	var instance = null;

	function MyClass () {
		
		// *********************************
		// PRIVATE VARIABLES AND FUNCTIONS
		// *********************************
		var myPrivateVar = "private variable accessed";
	    function myPrivateMethod(){ 
			alert ("private method accessed");
		}
	
		// *********************
		// PRIVILEGED METHODS
		// *********************
		this.getMyPrivateVar = function(){ return myPrivateVar }
		
	
		// *******************
		// PUBLIC PROPERTIES 
		// *******************
		this.myPublicVar = "public var accessed";
	
		// ****************
		// PUBLIC METHODS
		// ****************
		MyClass.prototype.myPublicMethod = function () {alert ("public method accessed")}
			
	}
	
	// ************************
	// SINGLETON GET INSTANCE
	// ************************
	return new function() {
    	this.getInstance = function() {
    		if (instance == null) {
        		instance = new MyClass();
            	instance.constructor = null;
         	}
         	return instance;
       	}
	}
	
}();

var myInstance = MyClassFactory.getInstance();
myInstance.myPublicMethod(); // OK
alert (myInstance.myPublicVar); // OK
alert (myInstance.getMyPrivateVar()); // OK
myInstance.myPrivateMethod (); // NO
alert (myInstance.myPrivateVar); // NO