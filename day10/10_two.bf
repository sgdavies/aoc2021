[Oh dear oh dear...
 Input file is controlled - it only contains ()[]{}<> and \n
 \n  (  )  <  >  [  ]   {   }
 10 40 41 60 62 91 93 123 125
 Not sure if I'm going to be able to do the maths properly, so for now just store counts
 In the remainder of the comments I'm going to alias the chars since eg square-brackets are control chars
 nl: newline; op: open paren; cp: close paren; oa: open angle; ca: close angle;
 os: open square; cs: close square; ob: open bracket; cb close bracket
 Memory layout:
 | invalid count | nl count | cp count | ca count | cs count | cb count | 0: marker | stack ... | 0 ...
 'stack' tracks openings. op=1 oa=2 os=3 ob=4 so op op oa ob os would be 11243 0...
 'invalid count' is states that should never happen

 In part b, we score each one as follows:
 cp : 1 point
 cs : 2 points
 cb : 3 points
 ca : 4 points
]

>>> >>> > Skip past the count stores in cells 1::6 and marker cell 7
, Read first character 000000 0m x*
[  
   When reading we use 3 cells in the stack: value | flag | store
   Value gets messed with as we go; at end of switch statement value and flag are zero
   and store is the char value: 1 for op etc
   at end of block we then move the store into the first location and step ready to read next
   >+<  Set flag 000000 0m bbb x* 1f
   ----- ----- Take 10: nl
   [ Not nl
     ----- -----  ----- -----  ----- ----- Take 30: total=40 = op
     [ Not op
       - Take 1: total=41 = cp
       [ Not cp
         ----- -----  ----- ---- Take 19; total=60 = oa
         [ Not oa
           -- Take 2: total 62 = ca
           [ Not ca
             ----- -----  ----- -----  ----- ---- Take 29: total 91 = os
             [ Not os
               -- Take 2: total 93 = cs
               [ Not cs
                 ----- -----  ----- -----  ----- ----- Take 30: total 123 = ob
                 [ Not ob
                   -- Take 2: total 125 = cb
                   [ Not cb
                     Unrecognised state; clear line and increment invalid flag; then read until next nl
                     >-< Unset flag
                     Clear value: first restore to original value to avoid underflow 
                     +++++ +++++  nl
                     +++++ +++++  +++++ +++++  +++++ +++++ op
                     + cp
                     +++++ +++++  +++++ ++++ oa
                     ++ ca
                     +++++ +++++  +++++ +++++  +++++ ++++ os
                     [ [-] < ]  Running clear; stops on m : iaaaaa 0m* 000
                     <<< <<< + >>> >>> >  Increment invalid flag; go back to m; go to v : one before f
                     + [ , ----- ----- ]  Do==while
                   ]>
                   [- = cb
                     If p is ob: pop p ; else clear line and report corrupt cb
                     + Keep using f as a flag
                     << --- ob=3 so take three from p
                     [ p wasn't ob: corrupt : bbb p'* 0 1f
                       >>- <<+++ Clear flag; replace previous p value
                       [ [-] < ]  Running clear; stops on m : aaaaa 0m* 000
                       <+>  aaaaa1 0m* 0 0f  m is equivalent to old p
                       + [ , ----- ----- ] Do==while : read to end of line
                     ] >>
                     [ p was ob : clear flag and reset stack pointer; loop expects pointer to be at f
                       -<
                     ]
                   ]<
                 ]>
                 [- = ob
                   > +++  Set s to 3=ob
                   <
                 ]<

               ]>
               [- = cs
                 If p is os: pop p ; else clear line and report corrupt cs
                 + Keep using f as a flag
                 << -- os=2 so take two from p
                 [ p wasn't os: corrupt : bbb p'* 0 1f
                   >>- <<++ Clear flag; replace previous p value
                   [ [-] < ]  Running clear; stops on m : aaaaa 0m* 000
                   <<+>>  aaaa1a 0m* 0 0f  m is equivalent to old p
                   + [ , ----- ----- ] Do==while : read to end of line
                 ] >>
                 [ p was os : clear flag and reset stack pointer; loop expects pointer to be at f
                   -<
                 ]
               ]<

             ]>
             [- = os
               > ++  Set s to 2=os
               <
             ]<
           ]>
           [- = ca
             If p is oa: pop p ; else clear line and report corrupt ca
             + Keep using f as a flag: aaaaa 0m bbb p 0 1f*
             << ---- oa=4 so take four from p
             [ p wasn't oa: corrupt : bbb p'* 0 1f
               >>- <<++++ Clear flag; replace previous p value
               [ [-] < ]  Running clear; stops on m : aaaaa 0m* 000
               <<<+>>>  aaa1aa 0m* 0 0f  m is equivalent to old p
               + [ , ----- ----- ] Do==while : read to end of line
             ] >> 
             [ p was oa : p already zero so we just clear flag and reset stack pointer; loop expects pointer to be at f
               -<
             ]
           ]<
         ]>
         [- =oa
           > ++++  Set s to 4=oa
           <
         ]<
       ]>    aaaaa 0m bbb 0 f* 
       [- =cp    aaaaa 0m bbb p x0' 0f* 0
         If p is op: pop p ; else clear line and report corrupt cp
         + Keep using f as a flag: aaaaa 0m bbb p 0 1f*
         << - op=1 so take one from p
         [ p wasn't op: corrupt : bbb p'* 0 1f
           >>- <<+  Clear flag; replace previous p value
           [ [-] < ]  Running clear; stops on m : aaaaa 0m* 000
           <<<<+>>>>  aa1aaa 0m* 0 0f  m is equivalent to old p
           + [ , ----- ----- ] Do==while : read to end of line
         ] >>  Either aa1aaa 0m 0 0f* or aaaaa 0m bbb 0p' 0 1f*
         [ p was op : p is already zero so we just clear flag and reset stack pointer; loop expects pointer to be at f
           -<
         ]
       ]<  aaaaa 0m bbb 0* 0 0f == aaaaa 0m bbb 0* 0f
     ]>
     [- =op aaaaa 0m x0' 0f* 0
       > +  Set s to 1=op
       <
     ]<
   ]> 000000 0m x=0 f* : x is 0 because either we cleared it or it was 0 already; f is 1 or 0
   [- =nl: Check flag and then unset it; end block on flag location 000000 0m 0 0f*
     For newlines we are going to clear the line so don't use the store
     If the stack is not empty: then line is incomplete and we should increment the incomplete counter
     << Either 00000 0m* or 00000 0m bbbb b*
     [  Stack not empty: incomplete
       Part two: calculate vals as we track back and print them
       Stack is 000000 0m sN :: s2 s1* 0=score 0
       For each s in stack: multiply score so far by 5; then add to s; we already store the correct value in s

[ New attempt; as soon as the score is largish the biggest factor by far is the *5
  So: calculate the first few; then output that value; followed by a count of how many remain
  Rough final value is first_val * 5**rem_count
  >[-<+++++>]<<  1
  >[-<+++++>]<<  2
  >[-<+++++>]<<  3
  >[-<+++++>]<<  4
  >[-<+++++>]<<  5
  >[-<+++++>]<<  6
  >.[-] <  Now we're at m0 sN::s6* 0
  [ .[-] <]  Print each remaining one: we need the vals to calc out of band; finish at m0*
  . Print 0 as separator
]

[ debug : this should be correct for part two but it's getting stuck
       [ >  sN::s1 score*
         [ - < +++++ > ] sN::s1_plus_5score 0*
       << sN::s2* new_score
       ] until m0* total_score
       > . [-] < output the score; drain it to 0; go back to m0*
]

       Legacy part one: this won't do anything as we've ended at 0m*:
       [ [-] <] Run back to first empty cell: marker cell #7; clear cells as we go 000000 0m* 0 0f
       <<< << + >>> >> Increment counter in cell 2 then move back to stack: cell 7; 010000 0m* 0 0f
     ]
     >> Move back to flag location: which is now near the start of the stack 010000 0m 0 0f*
   ]< End switch and point at val location 0a0000 0m 0* 0f s

   >>[-<<+>>]<< Copy store to val
   [>] Go to next cell if we stored something otherwise carry on here; a0000 0m s 0*
   , read: loop unless next char is blank (null byte or EOF) a0000 0m s y*
]
<[<] Go back to marker cell a0000 0m* s1 s2 s3
[ Debug only: Now print the result: counts of each val
<<< <<<.>.>.>.>.>.
> aaaaaa 0* ]
And let's calculate the part one answer then:
cp: 3 points
cs: 57 points
cb: 1197 points
ca: 25137 points
We have memory:
| inv | inc | cp | ca | cs | cb | 0*
<<<< [ - >>>> +++ <<<< ] >>>>  Add cp=3 to m cp times

<< [ - >>  xxxxXx Am* a
     > +++++ +++++  Am 10*
     [ - < +++++ > ]  A plus 50m 0*
     < +++++ ++  A plus 57m* 0
    <<] >>          This has added cs=57 to m cs times
xxxxxx m* 0

< [ - >  xxxxxX m* a b
    1197 is 12*10*10 take 3
    > +++++ +++++  m 10* b
    [ - > +++++ +++++ m 9 10*
      [- << +++++ +++++ ++ >>] m X 0*
    <] m 0* 0
    < ---
  <] >

25137 is 27*30*31 plus 27 !
<<< [ - >>> xxxXxx m* a b
      >        +++++ +++++  +++++ +++++  +++++ ++       m A* b
      [ - >    +++++ +++++  +++++ +++++  +++++ +++++    m A B*
        [ - << +++++ +++++  +++++ +++++  +++++ +++++ +  >> ] m A 0*
      <] m 0* 0
      < +++++ +++++  +++++ +++++  +++++ ++
    <<<] >>>

.
