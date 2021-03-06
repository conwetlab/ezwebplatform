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


function WorkSpace (workSpaceState) {

	// ****************
	// CALLBACK METHODS
	// ****************

	// Not like the remaining methods. This is a callback function to process AJAX requests, so must be public.
	var loadWorkSpace = function (transport) {
		// JSON-coded iGadget-variable mapping
		var response = transport.responseText;
		this.workSpaceGlobalInfo = eval ('(' + response + ')');

		this.varManager = new VarManager(this);
		this.contextManager = new ContextManager(this, this.workSpaceGlobalInfo);
		
		var tabs = this.workSpaceGlobalInfo['workspace']['tabList'];

		var visibleTabId = null;

		if (tabs.length>0) {
			visibleTabId = tabs[0].id;
			for (var i=0; i<tabs.length; i++) {
				var tab = tabs[i];
				this.tabInstances[tab.id] = new Tab(tab, this);
				
				if (tab.visible == 'true') {
					visibleTabId = tab.id;
				}
			}
		}

		this.wiring = new Wiring(this, this.workSpaceGlobalInfo);
		this.wiringInterface = new WiringInterface(this.wiring, this, $("wiring"), $("wiring_link"));

		if (tabs.length > 0) {
			for (i = 0; i < tabs.length; i++)
				this.tabInstances[tabs[i].id].getDragboard().paint();
		}

		this.loaded = true;
		//this.setTab(visibleTabName);
		//set the visible tab. It will be displayed as current tab afterwards
		this.visibleTab = this.tabInstances[visibleTabId];
		
		this._createWorkspaceMenu();

		OpManagerFactory.getInstance().continueLoadingGlobalModules(Modules.prototype.ACTIVE_WORKSPACE);
	}

	var onError = function (transport, e) {
		var msg;
		if (e) {
			msg = interpolate(gettext("JavaScript exception on file %(errorFile)s (line: %(errorLine)s): %(errorDesc)s"),
 			                  {errorFile: e.fileName, errorLine: e.lineNumber, errorDesc: e},
			                  true);
		} else {
			msg = transport.status + " " + transport.statusText;
		}
		msg = interpolate(gettext("Error retreiving workspace data: %(errorMsg)s."),
		                          {errorMsg: msg}, true);
		LogManagerFactory.getInstance().log(msg);
	}
	
	var renameSuccess = function(transport) {
	}
	var renameError = function(transport, e) {
		var msg;
		if (transport.responseXML) {
				msg = transport.responseXML.documentElement.textContent;
			} else {
				msg = "HTTP Error " + transport.status + " - " + transport.statusText;
			}

			msg = interpolate(gettext("Error renaming workspace, changes will not be saved: %(errorMsg)s."), {errorMsg: msg}, true);
			LogManagerFactory.getInstance().log(msg);
	}
	var deleteSuccess = function(transport) {
		var tabList = this.tabInstances.keys();
		
		for (var i=0; i<tabList.length; i++) {
			var tab = this.tabInstances[tabList[i]];
			tab.destroy;
			//TODO:treatment of wiring, varManager, etc.
		}
		LayoutManagerFactory.getInstance().hideCover();
	}
	var deleteError = function(transport, e) {
			var msg;
			if (transport.responseXML) {
				msg = transport.responseXML.documentElement.textContent;
			} else {
				msg = "HTTP Error " + transport.status + " - " + transport.statusText;
			}

			msg = interpolate(gettext("Error removing workspace, changes will not be saved: %(errorMsg)s."), {errorMsg: msg}, true);
			LogManagerFactory.getInstance().log(msg);
			LayoutManagerFactory.getInstance().hideCover();
	}
	
	//**** TAB CALLBACK*****
	var createTabSuccess = function(transport) {
		var response = transport.responseText;
		var tabInfo = eval ('(' + response + ')');
		
		tabInfo.igadgetList=[];
		
		this.tabInstances[tabInfo.id] = new Tab(tabInfo, this);
		this._checkLock();
		this.setTab(this.tabInstances[tabInfo.id]);
		for(var i=0; i< tabInfo.workspaceVariables.length; i++){
			this.varManager.parseWorkspaceVariable(tabInfo.workspaceVariables[i]);
			this.wiring.processVar(tabInfo.workspaceVariables[i]);
		}
	}
	
	var createTabError = function(transport, e) {
		var msg;
		if (transport.responseXML) {
			msg = transport.responseXML.documentElement.textContent;
		} else {
			msg = "HTTP Error " + transport.status + " - " + transport.statusText;
		}

		msg = interpolate(gettext("Error creating a tab: %(errorMsg)s."), {errorMsg: msg}, true);
		LogManagerFactory.getInstance().log(msg);
	}
	
	// ****************
	// PUBLIC METHODS
	// ****************
	
	WorkSpace.prototype.fillWithLabel = function() {
		this.workSpaceNameHTMLElement = this.workSpaceHTMLElement.firstDescendant();
		if(this.workSpaceNameHTMLElement != null){
			this.workSpaceNameHTMLElement.remove();
		}
		var nameToShow = (this.workSpaceState.name.length>15)?this.workSpaceState.name.substring(0, 15)+"..." : this.workSpaceState.name;
		var spanHTML = "<span>"+nameToShow+"</span>";
    	new Insertion.Top(this.workSpaceHTMLElement, spanHTML);
		this.workSpaceNameHTMLElement = this.workSpaceHTMLElement.firstDescendant();
		Event.observe(this.workSpaceNameHTMLElement, 'click', function(e){this.fillWithInput();}.bind(this));
    }


	WorkSpace.prototype.fillWithInput = function () {
		this.workSpaceNameHTMLElement.remove();
		var inputHTML = "<input class='ws_name' value='"+this.workSpaceState.name+"' size='"+this.workSpaceState.name.length+" maxlength=30' />";
		new Insertion.Top(this.workSpaceHTMLElement, inputHTML);
		this.workSpaceNameHTMLElement =  this.workSpaceHTMLElement.firstDescendant();
		this.workSpaceNameHTMLElement.focus();	
		Event.observe(this.workSpaceNameHTMLElement, 'blur', function(e){Event.stop(e);
					this.fillWithLabel()}.bind(this));
		Event.observe(this.workSpaceNameHTMLElement, 'change', function(e){Event.stop(e);
					this.updateInfo(e.target.value, null);}.bind(this));
		Event.observe(this.workSpaceNameHTMLElement, 'keyup', function(e){Event.stop(e);
					e.target.size = e.target.value.length;}.bind(this));
	}
	
	
    WorkSpace.prototype.updateInfo = function (workSpaceName, active) {
		//If the server isn't working the changes will not be saved	
		this.workSpaceState.name = workSpaceName;		

		var workSpaceUrl = URIs.GET_POST_WORKSPACE.evaluate({'id': this.workSpaceState.id});
		var o = new Object;
		o.name = workSpaceName;
		if (active !=null)
			o.active = active
		workSpaceData = Object.toJSON(o);
		params = 'workspace=' + workSpaceData;
		PersistenceEngineFactory.getInstance().send_update(workSpaceUrl, params, this, renameSuccess, renameError);
    }
    
    WorkSpace.prototype.deleteWorkSpace = function() {
		if(OpManagerFactory.getInstance().removeWorkSpace(this.workSpaceState.id)==true){
			var workSpaceUrl = URIs.GET_POST_WORKSPACE.evaluate({'id': this.workSpaceState.id});
			PersistenceEngineFactory.getInstance().send_delete(workSpaceUrl, this, deleteSuccess, deleteError);		
		}
	}

    WorkSpace.prototype.getName = function () {
    	return this.workSpaceState.name;
	}
	
    WorkSpace.prototype.getId = function () {
    	return this.workSpaceState.id;
	}
    
    WorkSpace.prototype.getWiring = function () {
    	return this.wiring;
	}
	
	WorkSpace.prototype.getWiringInterface = function () {
    	return this.wiringInterface;
	}
    
    WorkSpace.prototype.getVarManager = function () {
    	return this.varManager;
	}
	
	WorkSpace.prototype.getContextManager = function () {
    	return this.contextManager;
	}

	WorkSpace.prototype.downloadWorkSpaceInfo = function () {
		var workSpaceUrl = URIs.GET_POST_WORKSPACE.evaluate({'id': this.workSpaceState.id});
		PersistenceEngineFactory.getInstance().send_get(workSpaceUrl, this, loadWorkSpace, onError);
	}
	
	WorkSpace.prototype.showWiring = function() {
		if (!this.loaded)
			return;
		
		this.visibleTab.unmark();
		this.wiringInterface.show();
	}
	
/*	WorkSpace.prototype.hideAndUnmark = function() {
		if (!this.loaded)
			return;
		
		this.wiringInterface.hide();
		
		var tabList = this.tabInstances.keys();
		
		for (var i=0; i<tabList.length; i++) {
			var tab = this.tabInstances[tabList[i]];
			
			tab.hideAndUnmark();
		}
	}
*/
	
/*	//hide only the information in the wrapper. The tabs remain inalterable
	WorkSpace.prototype.hideContent = function() {
		this.visibleTab.markAsCurrent();
		this.wiringInterface.hide();
		this.visibleTab.hideDragboard();
		
	}
*/

	//hide all information about a workspace (wiring, tabs)
	WorkSpace.prototype.hide = function() {
		if (!this.loaded)
			return;
		
		//this.wiringInterface.hide();

		
		var tabList = this.tabInstances.keys();
		
		for (var i=0; i<tabList.length; i++) {
			var tab = this.tabInstances[tabList[i]];
			
			tab.hide();
		}
	}
	
	WorkSpace.prototype.show = function() {	
		if (!this.loaded)
			return;
			
		//global tab section
		this.fillWithLabel();
		
		var tabList = this.tabInstances.keys();
		
		for (var i=0; i<tabList.length; i++) {
			var tab = this.tabInstances[tabList[i]];
	
			if (tab == this.visibleTab)
				tab.show();
			else
				tab.unmark();
		}

	}
	
	WorkSpace.prototype.getTab = function(tabId) {
		return this.tabInstances[tabId];
	}
	
/*	WorkSpace.prototype.selectTab = function(tab) {
		LayoutManagerFactory.getInstance().unMarkGlobalTabs();
		if(this.visibleTab == tab){ //allow renaming
			this.visibleTab.fillWithInput();
		}else{ //first click on this tab -> mark as current
			this.setTab(tab);
		}			
	}*/
	
	WorkSpace.prototype.setTab = function(tab) {
		if (!this.loaded)
			return;
		if(this.visibleTab != null){
			this.visibleTab.unmark();		
		}
		this.visibleTab = tab;
		this.visibleTab.show();
		
	}
	
	WorkSpace.prototype.getVisibleTab = function() {
		if (!this.loaded)
			return;
		
		return this.visibleTab;
	}
	
/*	WorkSpace.prototype.showVisibleTab = function() {
		this.hideAndUnmark();
		this.visibleTab.show();
	}
*/
	
/*	WorkSpace.prototype.tabExists = function(tabName){
		var tabKeys = this.tabInstances.keys();
		for(var i=0;i<tabKeys.length;i++){
			if(this.tabInstances[tabKeys[i]].tabInfo.name == tabName)
				return true;
		}
		return false;
	}*/
	
	WorkSpace.prototype.addTab = function() {

		var tabsUrl = URIs.GET_POST_TABS.evaluate({'workspace_id': this.workSpaceState.id});
		var o = new Object;
		o.name = "MyTab "+(this.tabInstances.keys().length + 1).toString();
		tabData = Object.toJSON(o);
		params = 'tab=' + tabData;
		PersistenceEngineFactory.getInstance().send_post(tabsUrl, params, this, createTabSuccess, createTabError);
	
	}
	
	WorkSpace.prototype.removeTab = function(tabId){
		if(this.tabInstances.keys().length <= 1){
			var msg;
			msg = "there must be one tab at least";

			msg = interpolate(gettext("Error removing tab: %(errorMsg)s."), {errorMsg: msg}, true);
			LogManagerFactory.getInstance().log(msg);
			LayoutManagerFactory.getInstance().hideCover();
			return false;
		}
		this.tabInstances.remove(tabId);
		this.varManager.removeWorkspaceVariable(tabId);
		this.visibleTab.connectable.destroy();
		this.visibleTab.destroy();
		this.visibleTab = null;
		//set the first tab as current
		this.setTab(this.tabInstances.values()[0]);
		return true;
	}
	

	WorkSpace.prototype.goTab = function(tab) {
		if (!this.loaded)
			return;
		
		this.visibleTab.unmark();
		this.visibleTab = tab;
		this.visibleTab.go();
	}
	

	WorkSpace.prototype.addIGadget = function(tab, igadget, igadgetJSON) {
		this.varManager.addInstance(igadget, igadgetJSON);
		this.contextManager.addInstance(igadget, igadget.getGadget().getTemplate());
		this.wiring.addInstance(igadget, igadgetJSON.variables);
		
		tab.getDragboard().showInstance(igadget);

		// The dragboard must be shown after an igadget insertion
		//LayoutManagerFactory.getInstance().unMarkGlobalTabs();
		this.visibleTab.show();
	}
	
	WorkSpace.prototype.removeIGadget = function(iGadgetId) {
			this.visibleTab.getDragboard().removeInstance(iGadgetId); // TODO split into hideInstance and removeInstance
			this.varManager.removeInstance(iGadgetId);
			this.wiring.removeInstance(iGadgetId);
			this.contextManager.removeInstance(iGadgetId);
	}

	WorkSpace.prototype.getIGadgets = function() {
		if (!this.loaded)
			return;

		var iGadgets = new Array();
		var keys = this.tabInstances.keys();
		for (var i = 0; i < keys.length; i++) {
			iGadgets = iGadgets.concat(this.tabInstances[keys[i]].getDragboard().getIGadgets());
		}

		return iGadgets;
	}
	
	WorkSpace.prototype.getActiveDragboard = function() {
		return this.visibleTab.getDragboard();
	}

    // *****************
    //  CONSTRUCTOR
    // *****************

	this.workSpaceState = workSpaceState;
	this.workSpaceGlobal = null;
	this.wiringInterface = null;
	this.varManager = null;
	this.tabInstances = new Hash();
	this.wiring = null;
	this.varManager = null;
	this.contextManager = null;
	this.loaded = false;
	this.wiringLayer = null;
	this.visibleTab = null;
	this.workSpaceHTMLElement = $('workspace_name');
	this.unlockEntryPos;
	
	var wsOpsLauncher = 'ws_operations_link';
	var idMenu = 'menu_'+this.workSpaceState.id;
	
	//create workspace menu
	this._createWorkspaceMenu = function(){
		var optionPosition = 0;
		var menuHTML = '<div id="'+idMenu+'" class="drop_down_menu"><div id="submenu_'+idMenu+'" class="submenu"></div></div>';
		new Insertion.After($('menu_layer'), menuHTML);
		this.menu = new DropDownMenu(idMenu);
		this.menu.addOption("/ezweb/images/rename.gif", gettext("Rename"), function(){OpManagerFactory.getInstance().activeWorkSpace.fillWithInput(); 
							LayoutManagerFactory.getInstance().hideCover();},optionPosition++);
		this.unlockEntryPos = optionPosition;
		this.unlockEntryId = this.menu.addOption("/ezweb/images/unlock.png", gettext("Unlock"), function(){LayoutManagerFactory.getInstance().hideCover(); this._lockFunc(false);}.bind(this), optionPosition++);
		this.lockEntryId = this.menu.addOption("/ezweb/images/lock.png", gettext("Lock"), function(){LayoutManagerFactory.getInstance().hideCover(); this._lockFunc(true);}.bind(this), optionPosition++);							
		var res = this._checkLock();
		optionPosition -= res;
		this.menu.addOption("/ezweb/images/remove.png",gettext("Remove"),function(){LayoutManagerFactory.getInstance().showWindowMenu('deleteWorkSpace');}, optionPosition++);
		this.menu.addOption("/ezweb/images/list-add.png",gettext("New workspace"),function(){LayoutManagerFactory.getInstance().showWindowMenu('createWorkSpace');}, optionPosition++);
	}
		
	
	this._lockFunc = function(locked) {
		var keys = this.tabInstances.keys();
		for (var i = 0; i < keys.length; i++) {
			this.tabInstances[keys[i]]._lockFunc(locked);
		}
	}.bind(this);
	
	this._checkLock = function() {
		var keys = this.tabInstances.keys();
		var all = true;
		var locked = null;
		var numRemoved = 0;
		var position = this.unlockEntryPos;
		for (var i = 0; i < keys.length; i++) {
			if (i == 0){
				locked = this.tabInstances[keys[i]].dragboard.isLocked();
			} else if (locked != this.tabInstances[keys[i]].dragboard.isLocked()){
				all = false;	
			}
		}
		
		if(all){
			if(locked && this.lockEntryId!=null){
				this.menu.removeOption(this.lockEntryId);
				this.lockEntryId = null;
				numRemoved++;				
			}else if(!locked && this.unlockEntryId!=null){
				this.menu.removeOption(this.unlockEntryId);
				this.unlockEntryId = null;	
				numRemoved++;
			}
		}
		
		if((!all || locked) && this.unlockEntryId==null){
			this.unlockEntryId = this.menu.addOption("/ezweb/images/unlock.png", gettext("Unlock"), function(){LayoutManagerFactory.getInstance().hideCover(); this._lockFunc(false);}.bind(this), this.unlockEntryPos);
		}
		if((!all || !locked) && this.lockEntryId==null){
			if(this.unlockEntryId)
				position = this.unlockEntryPos + 1;
			this.lockEntryId = this.menu.addOption("/ezweb/images/lock.png", gettext("Lock"), function(){LayoutManagerFactory.getInstance().hideCover(); this._lockFunc(true);}.bind(this), position);	
		}
		return numRemoved;
	}.bind(this);
	
}
