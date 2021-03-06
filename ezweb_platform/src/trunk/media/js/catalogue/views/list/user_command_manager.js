/* 
*     (C) Copyright 2008 Telefonica Investigacion y Desarrollo
*     S.A.Unipersonal (Telefonica I+D)
*
*     This file is part of Morfeo EzWeb Platform.
*
*     Morfeo EzWeb Platform is free software: you can redistribute it and/or modify
*     it under the terms of the GNU Affero General Public License as published by
*     the Free Software Foundation, either version 3 of the License, or
*     (at your option) any later version.
*
*     Morfeo EzWeb Platform is distributed in the hope that it will be useful,
*     but WITHOUT ANY WARRANTY; without even the implied warranty of
*     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*     GNU Affero General Public License for more details.
*
*     You should have received a copy of the GNU Affero General Public License
*     along with Morfeo EzWeb Platform.  If not, see <http://www.gnu.org/licenses/>.
*
*     Info about members and contributors of the MORFEO project
*     is available at
*
*     http://morfeo-project.org
 */

var ListView_UserCommandManager = function (dom_wrapper) {

    this.catalogue = null;
    this.services = null;
    this.dom_wrapper = dom_wrapper;

    this.commands_info = null;

    this.set_commands_info = function (commands_info) {
        this.commands_info = commands_info;
    }

    this.set_catalogue = function (catalogue) {
        this.catalogue = catalogue;
    }

    this.set_services = function (services) {
        this.services = services;
    }

    this.init = function (dom_element) {
        this.register_commands(dom_element);
    }

    this.register_commands = function (dom_element) {
        var command_keys = this.commands_info.keys();

        for (var i=0; i<command_keys.length; i++) {
            var element_selector = command_keys[i];
            var command_code = this.commands_info[element_selector];

            var element = this.dom_wrapper.search_by_selector(element_selector);

            this.create_general_command(command_code, element);
        }
    }

    this.create_general_command = function (command_id, dom_element) {
        // Default html event = click
        var html_event = 'click';

        switch (command_id) {
        case 'VIEW_ALL':
            var command = new ViewAllCommand(dom_element, html_event, this.services, this.dom_wrapper);
            break;
        case 'SIMPLE_SEARCH':
            var element_code = this.dom_wrapper.get_code_by_element(dom_element);
            var data = {'starting_page': 1, 'scope': '', 'boolean_operator': 'AND', 'criteria': ''};

            switch (element_code) {
            case 'SEARCH_INPUT':
                html_event = 'keypress';
                break;
            case 'RESULTS_PER_PAGE_COMBO':
            case 'ORDER_BY_COMBO':
                html_event = 'change';
                break;
            case 'GADGETS_BUTTON':
                html_event = 'click';
                data['scope'] = 'gadget';
                break;
            case 'MASHUPS_BUTTON':
                html_event = 'click';
                data['scope'] = 'mashup';
                break;
            }

            var command = new SimpleSearchCommand(dom_element, html_event, this.services, this.dom_wrapper, data);
            break;
        case 'SHOW_DEVELOPER_INFO':
        case 'SHOW_SEARCH_INFO':
            var command = new ShowToolbarSectionCommand(dom_element, html_event, this.services, this.dom_wrapper, command_id);
            break;
        case 'SHOW_GADGETS':
        case 'SHOW_MASHUPS':
            var command = new ShowTabCommand(dom_element, html_event, this.services, this.dom_wrapper, command_id);
            break;
        default:
            return alert('event not identified! ' + command_id);
        }
    }

    this.create_command_from_data = function (command_id, dom_element, command_data, html_event) {
        // Default html event = click
        var default_html_event = 'click';

        if (!html_event)
            html_event = default_html_event;

        switch (command_id) {
        case 'INSTANTIATE_RESOURCE':
            var command = new InstantiateCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SIMPLE_SEARCH':
            var command = new SimpleSearchCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SHOW_RESOURCE_DETAILS':
            var command = new ShowResourceDetailsCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SUBMIT_GADGET':
            var command = new SubmitGadgetCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SUBMIT_PACKAGED_GADGET':
            var command = new SubmitPackagedGadgetCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SHOW_WINDOW':
            var command = new ShowWindowCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'SHOW_RESOURCE_LIST':
            var command = new ShowResourceListCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data);
            break;
        case 'DELETE_RESOURCE':
            var command = new DeleteResourceCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'UPDATE_RESOURCE':
            var command = new UpdateResourceHTMLCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'VOTE_RESOURCE':
            var command = new VoteResourceCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'CHANGE_RESOURCE_VERSION':
            var command = new ChangeResourceVersionCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'TAG_RESOURCE':
            var command = new TagResourceCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        case 'DELETE_TAG':
            var command = new RemoveResourceTagCommand(dom_element, html_event, this.services, this.dom_wrapper, command_data, command_id);
            break;
        default:
            return alert('event not identified! ' + command_id);
        }
    }

    this.get_service_facade = function () {
        return this.services;
    }

    this.run_initial_commands = function () {
        this.services.search('VIEW_ALL', 1, 'AND', '', '');
    }

    this.set_available_apps = function (available_apps) {
        this.catalogue.set_available_apps(available_apps);
    }
}
