<%--************************************************** 
 -             ***MyMobileWeb***
 - JSP code generated by MyMobileWeb Generation Proccess 
 - Date: Fri Jun 13 11:27:57 GMT+01:00 2008
**************************************************--%><%@ page session="true" %><%@ page import="org.morfeo.tidmobile.tags.writers.common.WriterData" %><%@ page import="org.morfeo.tidmobile.cfg.*" %><%@ page import="org.morfeo.tidmobile.server.lc.*" %><%@ page import="org.morfeo.tidmobile.server.*" %><%@ page import="org.morfeo.tidmobile.server.util.*" %><%@ page import="org.morfeo.tidmobile.tags.*" %><%@ page import="org.morfeo.tidmobile.CmtConstants" %><% WriterData wd = new WriterData( out, request, CmtConstants.I_MODE ); %>
<%
boolean jstl = false;
%>
<%--**************************************************--%>

<%--********CACHE ACTIVATION/DEACTIVATION********--%>
<% {
boolean cache = false;

if( !cache ) CacheConfigurator.resourceExpiresNow( response, wd.getDevice() );
} %>
<%--**************************************************--%>

<%--*************GENERATED CODE BLOCK*****************--%> 
<%!  private int[] lock = new int[0]; %>
<%

{
int wmode = ConfigUtil.getWorkingMode(Configurator.getInstance().getGlobalConfiguration());
DocumentTag documentTag = DocumentCache.getInstance().get( wd.getContext() );
if( jstl || documentTag == null || wmode == ServerConstants.WMODE_DEV ) {
synchronized(lock) {
documentTag = DocumentCache.getInstance().get(wd.getContext());
if(documentTag == null || wmode == ServerConstants.WMODE_DEV) {
documentTag = new DocumentTag();
documentTag.setOpName("Messages");   
documentTag.setFamilyName("generic");  
documentTag.setPresentationName("information");  
documentTag.setId("error");
documentTag.setStyleValues(new String[][]{{"padding","1"},{"margin","1"}});
	{
	HeadTag headTag = null;
	headTag = new HeadTag();
		{
		TitleTag titleTag = null;
		titleTag = new TitleTag();
		titleTag.setStyleValues(new String[][]{{"show-separator","true"},{"font-size","-1"},{"font-weight","bold"},{"img-display","both"},{"align","center"},{"include","true"},{"img-position","left"}});
		titleTag.setText("${_MYMW_USER_MSG.caption}", true, true );
		headTag.addDescendantTag( titleTag );
		}
	documentTag.addDescendantTag( headTag );
	}
	{
	org.morfeo.tidmobile.tags.BodyTag bodyTag = null;
	bodyTag = new org.morfeo.tidmobile.tags.BodyTag();
	bodyTag.setStyleValues(new String[][]{{"display-panels-as","plain-flow"},{"panel-links-layout","horizontal"}});
		{
		PTag pTag = null;
		pTag = new PTag("p1");
		pTag.setStyle("center vertical");
		pTag.setStyleValues(new String[][]{{"layout","vertical"},{"align","center"}});
		
                if ("none".equals(pTag.getStyleValue("display"))){                    
                pTag.setDisplay("false");                    
                }
                
		if (TidMobileTag.isDefined(pTag.getStyleValue("paginate"))){
                pTag.setPaginate(pTag.getStyleValue("paginate"));
                }
		            
            if ("true".equals(pTag.getStyleValue("paginate"))){
                documentTag.addParPaginateReference( pTag );
                bodyTag.setHasForm(true);
            }
        
			{
			ImageTag imageTag = null;
			imageTag = new ImageTag("ierror","Error");
			imageTag.setResourceid("_MYMW_ERROR", false );
			imageTag.setStyleValues(new String[][]{{"padding","0"},{"border-width","0"},{"margin","0"},{"aspect-ratio","true"}});
			
                if ("none".equals(imageTag.getStyleValue("display"))){                    
                imageTag.setDisplay("false");                    
                }
                
			pTag.addDescendantTag( imageTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
		{
		PTag pTag = null;
		pTag = new PTag("p2");
		pTag.setStyle("center vertical");
		pTag.setStyleValues(new String[][]{{"layout","vertical"},{"align","center"}});
		
                if ("none".equals(pTag.getStyleValue("display"))){                    
                pTag.setDisplay("false");                    
                }
                
		if (TidMobileTag.isDefined(pTag.getStyleValue("paginate"))){
                pTag.setPaginate(pTag.getStyleValue("paginate"));
                }
		            
            if ("true".equals(pTag.getStyleValue("paginate"))){
                documentTag.addParPaginateReference( pTag );
                bodyTag.setHasForm(true);
            }
        
			{
			LabelTag labelTag = null;
			labelTag = new LabelTag();
			labelTag.setStyle("small");
			labelTag.setStyleValues(new String[][]{{"img-display","both"},{"img-position","left"}});
			
                if ("none".equals(labelTag.getStyleValue("display"))){                    
                labelTag.setDisplay("false");                    
                }
                
			labelTag.setText("${_MYMW_USER_MSG.text}", true, true );
			pTag.addDescendantTag( labelTag );
			}
			{
			ActionTag actionTag = null;
			actionTag = new ActionTag();
			actionTag.setStyle("novalidate accept");
			actionTag.setId("_MYMW_E_BACK");
			actionTag.setValue("Volver", false, true );
			actionTag.setStyleValues(new String[][]{{"display-as","link"},{"img-position","left"}});
			
                if ("none".equals(actionTag.getStyleValue("display"))){                    
                actionTag.setDisplay("false");                    
                }
                
			pTag.addDescendantTag( actionTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
	documentTag.addDescendantTag( bodyTag );
	}
DocumentCache.getInstance().put(wd.getContext(),documentTag);
}
}
}

documentTag.write_html_wi_imode(wd);
}%>