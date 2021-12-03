{
    if ($1 == "forward") {
	h += $2;
	d2 += (d*$2);
    }
    else if ($1 == "down") {
	d += $2;
    }
    else if ($1 == "up") {
	d -= $2;
    }
    else
	print "Unknown: " $1;
}
END {
	print h*d " ("h ", " d")";
	print h*d2 " ("h ", " d2")";
}
