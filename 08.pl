#!/usr/bin/perl
use strict;
use warnings;
#  1
# 2 3
#  4
# 5 6
#  7
sub solve_row {
my $in_str = shift;
my $out_str = shift;
my @in_words = sort { length $a <=> length $b } split / /, $in_str; 
my @out_words = split / /, $out_str;

my @sorted_words;
foreach (@in_words) {
	push @sorted_words, join "", sort split //, $_;
}
my ($w2, $w3, $w4, $w5a,$w5b,$w5c, $w6a,$w6b,$w6c, $w7) = @sorted_words;
my ($num1, $num7, $num4, $num8) = ($w2, $w3, $w4, $w7);
my ($num2,$num3,$num5,$num6,$num9,$num0);
my $seg2;

# 2,3,5 all have 5 segments.  Both of 1's segments match 3 (but not 2,5)
foreach ($w5a, $w5b, $w5c) {
	#if (length $w2 =~ s/[$_]//gr == 0) {
	if (length $num1 =~ s/[$_]//gr == 0) {
		$num3 = $_;
		$seg2 = $w4 =~ s/[$_]//gr;  # all of 4 overlaps 3 apart from topleft segment
		last;
	}
}
# Now find the 5 - the only one which overlaps with topleft segment
foreach ($w5a, $w5b, $w5c) {
	if (length $seg2 =~ s/[$_]//gr == 0) {
		$num5 = $_;
	} elsif ($_ ne $num3) {
		$num2 = $_;
	}
}
# TODO : fixme -- this is confusing 6/9/0
# 6 doesn't fully overlap 1 but 0 and 9 do ; 5-1 == 9-1
my $x51 = $num5 =~ s/[$num1]//gr;
#print "5-1 $x51\n";
foreach ($w6a, $w6b, $w6c) {
	my $x_1 = $_    =~ s/[$num1]//gr;
	#print "x_1 $x_1 _ $_\n";
	if ($x51 eq $x_1) {
		#print "$_ is nine\n";
                $num9 = $_;
	} elsif (length $num1 =~ s/[$_]//gr == 1) {
		$num6 = $_;
	} else {
		$num0 = $_;
	}
}

my %vals = ( $num1, 1, $num2, 2, $num3, 3, $num4, 4, $num5, 5, $num6, 6, $num7, 7, $num8, 8, $num9, 9, $num0, 0 );

my @sorted_out;
foreach (@out_words) {
	push @sorted_out, join "", sort split //, $_;
}
my $ans = 1000*$vals{$sorted_out[0]} + 100*$vals{$sorted_out[1]} + 10*$vals{$sorted_out[2]} + $vals{$sorted_out[3]};
return $ans
}

my $in_test = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab";
my $out_test = "cdfeb fcadb cdfeb cdbaf";
print solve_row($in_test, $out_test), "\n";

my $file = "08.dat";
open(my $in,  "<",  $file)  or die "Can't open $file: $!";
my $total = 0;
while (<$in>) {
	if ($_ =~ /(.+) \| (.+)\n/) {
		$total += solve_row($1, $2);
	}
}
print "Total: $total\n";
