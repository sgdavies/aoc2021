[Oh dear oh dear...
 Input file is controlled - it only contains ()[]{}<> and \n
 \n  (  )  <  >  [  ]   {   }
 10 40 41 60 62 91 93 123 125
 Not sure if I'm going to be able to do the maths properly, so for now just store counts
 Memory layout:
 | )-count | ]-count | }-count | >-count | 0 (marker) | stack ... | 0 ...
 'stack' tracks openings. (=1 <=2 [=3 {=4 so ((<{{[ would be 112443 0...
]

>>>> Skip past the count stores in cells 0-3
,[  Read character.  If it's blank cell stays unchanged (0) and we skip to the end
   ----- ----- [ Take 10 (newline) ie skip the rest if this is the end of the line
     ----- ----- ----- ----- ----- ----- Take 30; if cell is now zero then char was o-paren
     [ +> ]
   ]
 ,
 ]
