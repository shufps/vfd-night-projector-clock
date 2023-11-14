$fn=64;
use <metric_thread.scad>

P = 1;
DE = 42.5;
HM42 = 5;
H1 = HM42;
D1 = 50;

difference() {
    translate([0,0,0.1]) cylinder(r=D1/2,h=H1-0.2);
    metric_thread(diameter=DE, pitch=P, length=HM42,internal=true);
}



