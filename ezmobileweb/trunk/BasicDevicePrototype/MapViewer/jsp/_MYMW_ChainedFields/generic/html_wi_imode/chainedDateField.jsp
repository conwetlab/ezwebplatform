<%--************************************************** 
 -             ***MyMobileWeb***
 - JSP code generated by MyMobileWeb Generation Proccess 
 - Date: Fri May 30 10:42:55 GMT+01:00 2008
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
documentTag.setOpName("_MYMW_ChainedFields");   
documentTag.setFamilyName("generic");  
documentTag.setPresentationName("chainedDateField");  
documentTag.setId("chainedDateField");
documentTag.setStyleValues(new String[][]{{"padding","1"},{"margin","1"}});
	{
	HeadTag headTag = null;
	headTag = new HeadTag();
		{
		TitleTag titleTag = null;
		titleTag = new TitleTag();
		titleTag.setStyleValues(new String[][]{{"show-separator","true"},{"font-size","-1"},{"font-weight","bold"},{"img-display","both"},{"align","center"},{"include","true"},{"img-position","left"}});
		titleTag.setText("${_MYMW_CDF_TITLE}", true, true );
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
		pTag.setStyle("vertical");
		pTag.setStyleValues(new String[][]{{"layout","vertical"},{"align","left"}});
		
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
			ChainedMenuTag chainedMenuTag = null;
			chainedMenuTag = new ChainedMenuTag("ChaDatField");
			chainedMenuTag.setStyleValues(new String[][]{{"autoselect","all-but-last"},{"display-as","combo-disabled"},{"required","true"},{"ajax","false"}});
			
                if ("none".equals(chainedMenuTag.getStyleValue("display"))){                    
                chainedMenuTag.setDisplay("false");                    
                }
                
			chainedMenuTag.setAlign("left");
			chainedMenuTag.setNumMenus(0);
				{
				MenuTag menuTag = null;
				menuTag = new MenuTag("Year");
				menuTag.setBind("${_MYMW_DATE_YEA_}");
				menuTag.setOptionsbind("${_MYMW_MENU_YEARS}");
				menuTag.setStyle("paginate");
				menuTag.setTitle("Year");
				menuTag.setStyleValues(new String[][]{{"show-menu-separator","false"},{"page-label-type","linktoeachpage"},{"visibility","visible"},{"page-link-range","sequential"},{"page-selected-color","red"},{"page-display-total","false"},{"layout","vertical"},{"menu-separator-char-vertical","|"},{"img-position","left"},{"page-total-color","red"},{"paginate","true"},{"ordered-list","false"},{"page-controls","only-nextprepage"},{"img-display","both"},{"align","left"},{"pagination-type","nextprepage"},{"page-position","bottom"},{"page-control-type","link"}});
				
                if ("none".equals(menuTag.getStyleValue("display"))){                    
                menuTag.setDisplay("false");                    
                }
                
				if (TidMobileTag.isDefined(menuTag.getStyleValue("paginate"))){
                menuTag.setPaginate(menuTag.getStyleValue("paginate"));
                }
				menuTag.setAlign("left");
				{
				TitleTag titleTag = new TitleTag();
				titleTag.setText("Year", false, true );
				titleTag.setStyleValues(new String[][]{{"font-size","-1"},{"font-weight","bold"},{"align","center"},{"include","true"}});
				menuTag.addTitleTag( titleTag );
				}
				menuTag.setDynamicInfo("generic","html_wi_imode","","menu","paginate",wd.getContext());
				
           String displayAs = menuTag.getStyleValue("display-as");
	       if ("combo-button".equals(displayAs) || "combo".equals(displayAs)){
				bodyTag.setHasForm(true);
		   }
         
				chainedMenuTag.incNumMenus();
				menuTag.setChainedMenu(true);
				chainedMenuTag.addDescendantTag( menuTag );
				}
				{
				MenuTag menuTag = null;
				menuTag = new MenuTag("Month");
				menuTag.setBind("${_MYMW_DATE_MON_}");
				menuTag.setOptionsbind("${_MYMW_MENU_MONTHS}");
				menuTag.setStyle("paginate");
				menuTag.setTitle("Month");
				menuTag.setStyleValues(new String[][]{{"show-menu-separator","false"},{"page-label-type","linktoeachpage"},{"visibility","visible"},{"page-link-range","sequential"},{"page-selected-color","red"},{"page-display-total","false"},{"layout","vertical"},{"menu-separator-char-vertical","|"},{"img-position","left"},{"page-total-color","red"},{"paginate","true"},{"ordered-list","false"},{"page-controls","only-nextprepage"},{"img-display","both"},{"align","left"},{"pagination-type","nextprepage"},{"page-position","bottom"},{"page-control-type","link"}});
				
                if ("none".equals(menuTag.getStyleValue("display"))){                    
                menuTag.setDisplay("false");                    
                }
                
				if (TidMobileTag.isDefined(menuTag.getStyleValue("paginate"))){
                menuTag.setPaginate(menuTag.getStyleValue("paginate"));
                }
				menuTag.setAlign("left");
				{
				TitleTag titleTag = new TitleTag();
				titleTag.setText("Month", false, true );
				titleTag.setStyleValues(new String[][]{{"font-size","-1"},{"font-weight","bold"},{"align","center"},{"include","true"}});
				menuTag.addTitleTag( titleTag );
				}
				menuTag.setDynamicInfo("generic","html_wi_imode","","menu","paginate",wd.getContext());
				
           String displayAs = menuTag.getStyleValue("display-as");
	       if ("combo-button".equals(displayAs) || "combo".equals(displayAs)){
				bodyTag.setHasForm(true);
		   }
         
				chainedMenuTag.incNumMenus();
				menuTag.setChainedMenu(true);
				chainedMenuTag.addDescendantTag( menuTag );
				}
				{
				MenuTag menuTag = null;
				menuTag = new MenuTag("Day");
				menuTag.setBind("${_MYMW_DATE_DAY_}");
				menuTag.setOptionsbind("${_MYMW_MENU_DAYS}");
				menuTag.setStyle("paginate");
				menuTag.setTitle("Day");
				menuTag.setStyleValues(new String[][]{{"show-menu-separator","false"},{"page-label-type","linktoeachpage"},{"visibility","visible"},{"page-link-range","sequential"},{"page-selected-color","red"},{"page-display-total","false"},{"layout","vertical"},{"menu-separator-char-vertical","|"},{"img-position","left"},{"page-total-color","red"},{"paginate","true"},{"ordered-list","false"},{"page-controls","only-nextprepage"},{"img-display","both"},{"align","left"},{"pagination-type","nextprepage"},{"page-position","bottom"},{"page-control-type","link"}});
				
                if ("none".equals(menuTag.getStyleValue("display"))){                    
                menuTag.setDisplay("false");                    
                }
                
				if (TidMobileTag.isDefined(menuTag.getStyleValue("paginate"))){
                menuTag.setPaginate(menuTag.getStyleValue("paginate"));
                }
				menuTag.setAlign("left");
				{
				TitleTag titleTag = new TitleTag();
				titleTag.setText("Day", false, true );
				titleTag.setStyleValues(new String[][]{{"font-size","-1"},{"font-weight","bold"},{"align","center"},{"include","true"}});
				menuTag.addTitleTag( titleTag );
				}
				menuTag.setDynamicInfo("generic","html_wi_imode","","menu","paginate",wd.getContext());
				
           String displayAs = menuTag.getStyleValue("display-as");
	       if ("combo-button".equals(displayAs) || "combo".equals(displayAs)){
				bodyTag.setHasForm(true);
		   }
         
				chainedMenuTag.incNumMenus();
				menuTag.setChainedMenu(true);
				chainedMenuTag.addDescendantTag( menuTag );
				}
			documentTag.addChainedMenuReference( chainedMenuTag );
			           
	       if (chainedMenuTag.getStyleValueAsBoolean("ajax")){
				documentTag.setAjaxEnabled(true);
		   }
         
			
           String displayAs = chainedMenuTag.getStyleValue("display-as");
	       if ("combo-disabled".equals(displayAs) || "combo".equals(displayAs)){
				bodyTag.setHasForm(true);
		   }
         
			pTag.addDescendantTag( chainedMenuTag );
			}
		bodyTag.addDescendantTag( pTag );
		}
		{
		PTag pTag = null;
		pTag = new PTag("p2");
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
			ActionTag actionTag = null;
			actionTag = new ActionTag();
			actionTag.setStyle("novalidate accept");
			actionTag.setId("back");
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