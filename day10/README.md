Day 10 part two attempt in brainfuck

Not very successful.

- Algorithm for calculating completion score was fine, but hit runtime issues (see below)
- Sorting the results was always going to be tricky in this language! I was OK with printing the 
scores and sorting out-of-band

Unfortunatley for the algorithm though, the values for some scores were far too high -- the highest 
I saw was 2.8E10.  Which doesn't bode well when your only ops are ++ and --!

For example: more than 5 minutes to process a single line:
```$ time ./brainfuck.py 10.bf just_the_second_data_line 
192702489 0

real    5m29.523s```

That was fun enough that I had time to reimplement the interpreter in C and try again,
which was much better but still taking far too long - still averaging 1min/line:
```:$ time ./brain_c 10.bf first_10_lines_of_data
Program length: 8774
Data length: 1011
2716659 20716289193 971405784 338464181 8742409 716301167 23518196819 27531

real    10m56.984s```

The most obvious algorithmic improvement is to do less.  We could probably find the median row
without doing all the calculations - after the first few the addition step makes next to no 
difference.  So there's a way forward by outputing [score_for_first_N, steps_remaining] ;
then sort those smaller numbers (e.g. cancel down to the minimum step, etc).  Even this though 
isn't enough as we need the precise value of the median at the end.

As a halfway I've ended up modifying the program to output a part-calculation plus the remaining scores
and a quick-n-dirty Python script to calculate final scores, do the median, etc.  A shame not to be able
to complete it in BF but I feel I have reached the limits of what it's capable of!
