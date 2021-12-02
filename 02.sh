# ./02.sh filename

# Hack for part one :-)
echo $((((`grep down $1 | cut -d ' ' -f 2 | paste -sd+ - | bc` - `grep up $1 | cut -d ' ' -f 2 | paste -sd+ - | bc`)) * `grep forward $1 | cut -d ' ' -f 2 | paste -sd+ - | bc`))

# Part 2 requires more 'finesse'
h=0
d=0
a=0
# cat $1 | while read... doesn't work as the | creates a subshell - so value updates don't propagate back
while read line
do
	c=`echo $line | cut -d ' ' -f 1`
	v=`echo $line | cut -d ' ' -f 2`
	case "$c" in
		forward)
			h=$(($h + $v))
			d=$(($d + (($a * $v)) ))
			;;
		down)
			a=$(($a + $v))
			;;
		up)
			a=$(($a - $v))
                        ;;
		*)
			echo "Unknown command $c ($line)"
			exit 1
	esac
	#echo $line h$h d$d a$a
done < "$1"
echo $(($h * $d))
