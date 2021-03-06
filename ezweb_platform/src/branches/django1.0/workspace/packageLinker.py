from workspace.models import WorkSpaceVariable, AbstractVariable, VariableValue
from igadget.models import Variable

from django.db import models

class PackageLinker:
    def link_workspace(self, workspace, user):
        # Linking user to workspace
        self.add_user_to_workspace(workspace, user)
        
        # Getting all abstract variables of workspace
        ws_igadget_vars = Variable.objects.filter(igadget__tab__workspace=workspace)
        
        # Linking igadgets' gadget with user
        # For user personal showcase 
        for var in ws_igadget_vars:
            gadget = var.igadget.gadget
            gadget.users.add(user)
            
            gadget.save()
        
        ws_vars = WorkSpaceVariable.objects.filter(workspace=workspace)
        
        abstract_var_list = self.get_abstract_var_list(ws_igadget_vars, ws_vars)
        
        # Creating new VariableValue to each AbstractVariable
        # Linking each new VariableValue to the user argument
        self.add_user_to_abstract_variable_list(abstract_var_list, user)

    def add_user_to_workspace(self, workspace, user):
        workspace.users.add(user)
        workspace.save()

    def add_user_to_abstract_variable_list(self, abstract_var_list, user):
        for (abstract_var, variable) in abstract_var_list:
            variable_value = VariableValue(user=user, value='', abstract_variable=abstract_var)
            
            # variable is the child element of the Variable inheritance
            # variable == None => wk_variable
            # variable != None => igadget_variable associated to abstract_variable
            if variable and variable.vardef.default_value:
                variable_value.value = variable.vardef.default_value
            
            variable_value.save()
    
    def get_abstract_var_list(self, ws_igadget_vars, ws_vars):
        abstract_var_list = []
        
        for igadget_var in ws_igadget_vars:
            abstract_var_list.append((igadget_var.abstract_variable, igadget_var))
            
        for ws_var in ws_vars:
            abstract_var_list.append((ws_var.abstract_variable, None))
        
        return abstract_var_list
        
        