$fn=10;

module leg() {
    cube([0.6, 1.2, 0.25]);
    translate([0, 1.2, 0]) cube([0.6, 0.25, 2]);
}

color("#404040") cube([13.20, 8.5, 7], center=true);
color("lightgray") {
    translate([-2.54-1.27-0.3, -8.5/2-1.45, -3.5]) rotate([0, 0, 0]) leg();
    translate([-1.27-0.3, -8.5/2-1.45, -3.5]) rotate([0, 0, 0]) leg();
    translate([+2.54+1.27-0.3, -8.5/2-1.45, -3.5]) rotate([0, 0, 0]) leg();
    translate([+2.54+1.27+0.3, +8.5/2+1.45, -3.5]) rotate([0, 0, 180]) leg();
    translate([-2.54-1.27+0.3, +8.5/2+1.45, -3.5]) rotate([0, 0, 180]) leg();
}
//translate([0, 0, 0]) cube([5, 11.4, 1], center=true);