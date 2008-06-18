package mobi.mymem.oa;

import org.morfeo.tidmobile.server.oa.BasicApplicationOperation;
import org.morfeo.tidmobile.server.oa.OAException;
import org.morfeo.tidmobile.context.Context;

/* Java code generated by MyMobileWeb Plugin */
public class Cursors_cursors_OA extends BasicApplicationOperation {


@Override
public void execute(Context the_context) throws OAException {

	/*Map cursors = new HashMap();
	cursors.put("Up", "up");
	cursors.put("Left", "le");
	cursors.put("Right", "ri");
	cursors.put("Down", "do");
	*/

	String[][] cursors = new String[9][2];
	cursors[0][0]="UP";
	cursors[0][1]="North";
	cursors[1][0]="DO";
	cursors[1][1]="South";
	cursors[2][0]="LE";
	cursors[2][1]="West";
	cursors[3][0]="RI";
	cursors[3][1]="East";
	cursors[4][0]="IN";
	cursors[4][1]="Zoom in";
	cursors[5][0]="OUT";
	cursors[5][1]="Zoom out";
	cursors[6][0]="CE";
	cursors[6][1]="center";
	cursors[7][0]="IN2";
	cursors[7][1]="Zoom in+";
	cursors[8][0]="OUT2";
	cursors[8][1]="Zoom out+";
	
	the_context.setElement("cursors",cursors);
	the_context.setElement("xx1","");
	the_context.setElement("xx2","<br/>");
	the_context.setElement("xx3","<mymw:br/>");
	the_context.setElement("xx4","<div/>");
	//the_context.setElement("cursor","");
}

}