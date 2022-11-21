% Use this editor as a MiniZinc scratch book
var int: a;   var int: b; var int: c; var int: d; var int: e;

constraint a >= 5 \/ a == 0; constraint a<= 9;
constraint b >= 4 \/ b == 0; constraint b <= 7 ;
constraint c >= 2 \/ c == 0; constraint c <= 5 ;
constraint d >= 2 \/ d == 0; constraint d<= 4 ;
constraint e >= 1 \/ e == 0; constraint e <= 3 ;
constraint a+b+c+d+e == 10;

solve maximize 1500*a + 2000*b + 1000*c + 1500*d + 750*e;

output ["a=\(a)\t b=\(b)\t c=\(c)\t d=\(d)\t e=\(e)\n"];