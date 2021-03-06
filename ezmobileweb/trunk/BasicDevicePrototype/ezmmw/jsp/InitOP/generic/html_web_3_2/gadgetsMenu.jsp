<%--************************************************** 
 -             ***MyMobileWeb***
 - JSP code generated by MyMobileWeb Generation Proccess 
 - Date: Tue Jun 17 08:31:58 GMT+01:00 2008
**************************************************--%><%@ page session="true" %><%@ page import="org.morfeo.tidmobile.tags.writers.common.WriterData" %><%@ page import="org.morfeo.tidmobile.cfg.*" %><%@ page import="org.morfeo.tidmobile.server.lc.*" %><%@ page import="org.morfeo.tidmobile.server.*" %><%@ page import="org.morfeo.tidmobile.server.util.*" %><%@ page import="org.morfeo.tidmobile.tags.*" %><%@ page import="org.morfeo.tidmobile.CmtConstants" %><% WriterData wd = new WriterData( out, request, CmtConstants.HTML ); %>
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
documentTag.setOpName("InitOP");   
documentTag.setFamilyName("generic");  
documentTag.setPresentationName("gadgetsMenu");  
documentTag.setId("gadgetsMenu");
documentTag.setStyleValues(new String[][]{{"padding","1"},{"margin","1"}});
	{
	HeadTag headTag = null;
	headTag = new HeadTag();
		{
		TitleTag titleTag = null;
		titleTag = new TitleTag();
		titleTag.setStyleValues(new String[][]{{"show-separator","true"},{"font-size","-1"},{"font-weight","bold"},{"img-display","both"},{"align","center"},{"include","true"},{"img-position","left"}});
		titleTag.setText("Gadgets menu", false, true );
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
		pTag = new PTag("");
		pTag.setStyleValues(new String[][]{{"layout","horizontal"},{"align","left"}});
		
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
			labelTag.setId("workspace_name");
			labelTag.setStyle("name");
			labelTag.setStyleValues(new String[][]{{"font-weight","bold"},{"img-display","both"},{"img-position","left"}});
			
                if ("none".equals(labelTag.getStyleValue("display"))){                    
                labelTag.setDisplay("false");                    
                }
                
			labelTag.setText("${workspaceName}", true, true );
			pTag.addDescendantTag( labelTag );
			}
			{
			LabelTag labelTag = null;
			labelTag = new LabelTag();
			labelTag.setId("tab_name");
			labelTag.setStyle("name");
			labelTag.setStyleValues(new String[][]{{"font-weight","bold"},{"img-display","both"},{"img-position","left"}});
			
                if ("none".equals(labelTag.getStyleValue("display"))){                    
                labelTag.setDisplay("false");                    
                }
                
			labelTag.setText("${tabName}", true, true );
			pTag.addDescendantTag( labelTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
		{
		PTag pTag = null;
		pTag = new PTag("");
		pTag.setStyleValues(new String[][]{{"layout","horizontal"},{"align","left"}});
		
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
			MenuTag menuTag = null;
			menuTag = new MenuTag("gadgets_menu");
			menuTag.setBind("${id}");
			menuTag.setOptionsbind("${userIgadgetList}");
			menuTag.setStyle("gadgetMenu");
			menuTag.setKeymember("id");
			menuTag.setTextmember("name");
			menuTag.setImgmember("image");
			menuTag.setHrefmember("href");
			menuTag.setLongtitlemember("description");
            menuTag.setLongTitle( true );
			menuTag.setStyleValues(new String[][]{{"show-menu-separator","false"},{"page-label-type","linktoeachpage"},{"cols","3"},{"visibility","visible"},{"page-link-range","sequential"},{"page-selected-color","red"},{"page-display-total","false"},{"layout","vertical"},{"menu-separator-char-vertical","|"},{"img-position","left"},{"page-total-color","red"},{"background-color1","rgb(224, 224, 224)"},{"page-controls","only-nextprepage"},{"colored","true"},{"img-display","both"},{"align","left"},{"pagination-type","nextprepage"},{"page-position","top"},{"page-control-type","link"}});
			
                if ("none".equals(menuTag.getStyleValue("display"))){                    
                menuTag.setDisplay("false");                    
                }
                
			menuTag.setPaginate("true");
			menuTag.setAlign("left");
			menuTag.setDynamicInfo("generic","html_web_3_2","mypresentation.css","menu","gadgetMenu",wd.getContext());
			
           String displayAs = menuTag.getStyleValue("display-as");
	       if ("combo-button".equals(displayAs) || "combo".equals(displayAs)){
				bodyTag.setHasForm(true);
		   }
         
			pTag.addDescendantTag( menuTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
		{
		PTag pTag = null;
		pTag = new PTag("pEnd");
		pTag.setStyleValues(new String[][]{{"layout","horizontal"},{"align","left"}});
		
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
			LinkTag linkTag = null;
			linkTag = new LinkTag("lindex");
			linkTag.setResourceid("logout");
			linkTag.setStyle("foot");
			linkTag.setStyleValues(new String[][]{{"img-display","both"},{"img-position","left"}});
			
                if ("none".equals(linkTag.getStyleValue("display"))){                    
                linkTag.setDisplay("false");                    
                }
                
			linkTag.setText("Salir", false, true );
			{
			ImageTag imageTag = new ImageTag();
			linkTag.setStylesImage( imageTag.getStyleValues() );
			}
			pTag.addDescendantTag( linkTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
	documentTag.addDescendantTag( bodyTag );
	}
DocumentCache.getInstance().put(wd.getContext(),documentTag);
}
}
}

documentTag.write_html_web_3_2(wd);
}%>