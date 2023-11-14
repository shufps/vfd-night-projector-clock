$fn=10;

color("lightblue") cube([6.35, 4.32, 7.44] );
color("gold") difference() {
    translate([1.02, 1.52, 7.44]) cylinder(d=2.25, h=1.02);
    translate([0, 1.52-0.2, 8]) cube([10, 0.4, 0.5]);
}
color("lightgray") {
    translate([6.25/2-2.54-0.5/2, -1.02, 0]) cube([0.5, 2.29, 0.5]);
    translate([6.25/2+2.54-0.5/2, -1.02, 0]) cube([0.5, 2.29, 0.5]);
    translate([6.25/2-0.5/2, -1.02+4.32-0.2, 0]) cube([0.5, 2.29, 0.5]);
    
}