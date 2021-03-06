package mobi.mymem.oa;

import mobi.mymem.MyContextVariables;
import mobi.mymem.MyUtils;

import org.morfeo.tidmobile.server.oa.BasicApplicationOperation;
import org.morfeo.tidmobile.server.oa.OAException;
import org.morfeo.tidmobile.context.Context;

/* Java code generated by MyMobileWeb Plugin */
public class RigthLocalize extends BasicApplicationOperation {


@Override
public void execute(Context the_context) throws OAException {
 
	int zoom = MyUtils.NORMALZOOM;
	if (the_context.isElement(MyContextVariables.ZOOM))
		zoom = (Integer) the_context.getElement(MyContextVariables.ZOOM);
	
	double increaseLongitude = MyUtils.getIncreaseLongitude(zoom, MyUtils.getWIDTHNORMAL(the_context));
	the_context.setApplicationElement(MyContextVariables.INCREASELONGITUDE, increaseLongitude);

}

}