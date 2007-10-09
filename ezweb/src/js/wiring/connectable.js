///////////////////////////////////////////////////////////////////////////////////////////////////
// This is the class with the common properties of every connectable object of the wiring module //
// The other connectable classes from the wiring module will inherit from this class             //
///////////////////////////////////////////////////////////////////////////////////////////////////
function Connectable(name){
	// Private attributes
   this.id;
   this.type;
   this.value;
   this.name=name;
}
// Public methods 

Connectable.prototype.getId = function(){
   return this.id;
}
	
Connectable.prototype.setId = function(value){
   this.id=value;
}
	
Connectable.prototype.getType = function(){
   return this.type;
}
	
Connectable.prototype.setType = function(value){
   this.type=value;
}
	
Connectable.prototype.getValue = function(){
   return this.value;
}

Connectable.prototype.setValue = function(value){
   this.value=value;
}

Connectable.prototype.getName = function(){
   return this.name;
}

Connectable.prototype.clear = function(value){
   null; //
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This class represents every object which may be placed in the middle of a connection between a In object and Out object //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function Out(name){
   Connectable.call(this,name);
   this.inputHash = [];
}
Out.prototype = new Connectable();

////////////////////////////////////////////////////////////////////////////////////////////////////////
// This class represents every object which may initialize one transmission through the wiring module //
////////////////////////////////////////////////////////////////////////////////////////////////////////
function In(name){
   Connectable.call(this,name);
   this.outputHash = [];
}
In.prototype = new Connectable();

/////////////////////////////////////////////////////////////////////
// This class represents every object which may transmit some data //
/////////////////////////////////////////////////////////////////////
function InOut(name){
   Connectable.call(this,name);
   this.inputHash = [];
   this.outputHash = [];
}
InOut.prototype = new Connectable();

//////////////////////////////////////////////////////////////////////////
// This class represents a iGadget variable which may produce some data //
//////////////////////////////////////////////////////////////////////////
function Event(name){
   In.call(this,name);
}
Event.prototype = new In();

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This class represents a connectable whose only purpose is to redistribute the data produced by an In object //
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function Channel(name){
   InOut.call(this,name);
}
InOut.prototype = new InOut();

/////////////////////////////////////////////////////////////////////////////
// This class representents a iGadget variable which may receive some data //
/////////////////////////////////////////////////////////////////////////////
function Slot(name){
   Out.call(this,name);
}
Slot.prototype = new Out();