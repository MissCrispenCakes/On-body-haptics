$fn = 32;

module roundrect( width, depth, height, r_c ) {
	hull() {
		translate( [-(width/2)+r_c, -(depth/2)+r_c, 0] ) cylinder( r=r_c, h=height, center=true );
		translate( [(width/2)-r_c, (depth/2)-r_c, 0 ] ) cylinder( r=r_c, h=height, center=true );
		translate( [-(width/2)+r_c, (depth/2)-r_c, 0] ) cylinder( r=r_c, h=height, center=true );
		translate( [(width/2)-r_c, -(depth/2)+r_c, 0] ) cylinder( r=r_c, h=height, center=true );
	}
}

module standoff( diameter, hole, height, holeHeight) {
    difference()
    {
        cylinder(d=diameter, h=height, center=true);
        translate([0, 0, (height-holeHeight) / 2 + 0.01]) cylinder(d=hole, h=holeHeight, center=true);
    }
}
overallWidth = 95;
overallDepth = 44;
baseThickness = 2;
cornerRadius = 3;
beltDepth = 30;
beltWidth = 4;
beltRadius = 2;
beltOffset = 4;

batteryWall = 2;
batteryCavityWidth = 65;
batteryCavityDepth = 37;
batteryCavityHeight = 7;
batteryWidth = batteryCavityWidth + (2 * batteryWall);
batteryDepth = batteryCavityDepth + (1.5 * batteryWall);
batteryHeight = batteryCavityHeight + batteryWall;
batteryWireCutoutWidth = 5;
batteryWireCutoutDepth = 7;

standoffX = 58;
standoffY = 23;
standoffDiameter = 7.5;
standoffHole = 3.4;
standoffHeight = 5;
standoffHoleDepth = 4.5;

/* Base plate */
difference()
{
    roundrect(overallWidth,overallDepth,baseThickness,cornerRadius);
    union()
    {
        translate([-(overallWidth/2)+beltOffset+(beltWidth/2), 0, 0]) roundrect(beltWidth, beltDepth, 2 * baseThickness, beltRadius);
        translate([(overallWidth/2)-beltOffset-(beltWidth/2), 0, 0]) roundrect(beltWidth, beltDepth, 2 * baseThickness, beltRadius);
    }
}

/* Battery compartment */
translate([0, 0, (batteryHeight/2 + baseThickness/2 - 0.01)]) difference()
{
    roundrect(batteryWidth, batteryDepth, batteryHeight, cornerRadius);
    translate([0, 0, -(batteryWall/2)]) union()
    {
        cube([batteryCavityWidth, batteryCavityDepth, batteryCavityHeight], center=true);
        translate([(batteryWall + 0.01) / 2, -((batteryCavityDepth/2) + batteryWall + 0.01) / 2, 0]) cube([batteryCavityWidth + batteryWall + 0.01, (batteryCavityDepth/2 + 5) + batteryWall + 0.01, batteryCavityHeight], center=true);
        translate([(batteryWidth - batteryWireCutoutWidth)/2+0.01, 0, 0]) cube([batteryWireCutoutWidth, batteryWireCutoutDepth, batteryHeight + 2.01], center=true);
    }
}

/* Standoffs */
translate([0, 0, batteryHeight + (baseThickness/2) + (standoffHeight/2) - 0.01])
union()
{
    translate([standoffX/2, standoffY/2, 0]) standoff(standoffDiameter, standoffHole, standoffHeight, standoffHoleDepth);
    translate([-standoffX/2, standoffY/2, 0]) standoff(standoffDiameter, standoffHole, standoffHeight, standoffHoleDepth);
    translate([standoffX/2, -standoffY/2, 0]) standoff(standoffDiameter, standoffHole, standoffHeight, standoffHoleDepth);
    translate([-standoffX/2, -standoffY/2, 0]) standoff(standoffDiameter, standoffHole, standoffHeight, standoffHoleDepth);
}