use std::fmt;

const DEPTH: u8 = 4;

#[derive(Clone, Debug)]
enum Element {
    Regular(u8),
    Snailfish(Snailfish)
}

impl Element {
    fn value(&self) -> u32 {
        match self {
            Element::Regular(val) => *val as u32,
            Element::Snailfish(snail) => snail.magnitude(),
        }
    }
}

enum LR {
    Left(u8),
    Right(u8),
    Neither,
}

#[derive(Clone, Debug)]
struct Snailfish {
    left: Box<Element>,
    right: Box<Element>
}

impl Snailfish {
    fn parse_str(s: &str) -> Snailfish {
        // Expect slice of form "[left,right]"
        let (snail, len) = Snailfish::parse_sub_str(s);
        assert!(len == s.len());
        snail
    }
    
    fn parse_sub_str(s: &str) -> (Snailfish, usize) {
        // Expect slice of form "[left,right]..."
        // Returns a snailfish and number of chars consumed
        if !s.starts_with("[") {
            println!("Bad string: {}", s);
            assert!(false);
        }
        let s = &s[1..];
        let (left, l_consumed) = match &s[..1] {
            "[" => {
                let (snail, len) = Snailfish::parse_sub_str(&s[..]);
                (Element::Snailfish(snail), len)
            },
            _   => {
                let comma = s.find(",").unwrap();
                let value = s[..comma].parse::<u8>().unwrap();
                (Element::Regular(value), comma)
            }
        };

        let s = &s[l_consumed..];
        assert!(s.starts_with(','));
        let s = &s[1..];
        let (right, r_consumed) = match &s[..1] {
            "[" => {
                let (snail, len) = Snailfish::parse_sub_str(&s[..]);
                (Element::Snailfish(snail), len)
            },
            _   => {
                let end_bracket = s.find("]").unwrap();
                let value = s[..end_bracket].parse::<u8>().unwrap();
                (Element::Regular(value), end_bracket)
            }
        };

        // +3 for "[" "," and "]"
        (Snailfish { left: Box::new(left), right: Box::new(right) },
         l_consumed + r_consumed + 3)
    }
    
    fn add(&mut self, other: Snailfish) {
        self.left = Box::new(Element::Snailfish(self.clone()));
        self.right = Box::new(Element::Snailfish(other));
    }

    fn reduce(&mut self) {
        loop {
            if let Some(_explode) = self.explode(1) {
                //
            } else if let Some(_split) = self.split() {
                //
            } else {
                // no more reducing to do
                return;
            }
        }
    }

    fn explode(&mut self, depth: u8) -> Option<LR> {
        // DFS to find first element that needs exploding; explode it or return None
        // When traversing back, we may be passed an exploded value which needs adding left or right - handle that.
        // When .left explodes, the r-value b can always be immediately passed down to x [...[[a,b],x]...]
        // The l-value a must be passed back and absorbed by the parent.  Similarly for .right.
        // if left is reg - do right; if left is snail - try explode, otherwise do right

        // Don't call explode on a snail with no snails (easier for parent to handle, as they need to swap that snail for 0)
        match (&*self.left, &*self.right) {
            (Element::Regular(_), Element::Regular(_)) =>  { assert!(false, "Parent should have handled this"); },
            _ => (),
        }

        let l_explode = match &mut *self.left {
            Element::Regular(_) => None,
            Element::Snailfish(snail) => {
                match (&*snail.left, &*snail.right) {
                    (Element::Regular(lval), Element::Regular(rval)) => {
                        if depth >= DEPTH {
                            // Explode!
                            // Close the borrows so we can reassign self.left
                            let lval = *lval;
                            let rval = *rval;
                            self.left = Box::new(Element::Regular(0));
                            match &mut *self.right {
                                Element::Regular(x) => {
                                    self.right = Box::new(Element::Regular(*x+rval));
                                },
                                Element::Snailfish(rsnail) => {
                                    rsnail.add_explode_val(LR::Left(rval)); // Add the rval to the closest (leftmost) sub-element
                                },
                            };
                            Some(LR::Left(lval))  // Parent needs to consume lval in closest on left (turn to R if passed down again)
                        } else {
                            None
                        }
                    },
                    _ => {
                        match snail.explode(depth+1) {
                            None => None,
                            Some(LR::Neither) => {
                                // something exploded, but all values have already been handled
                                Some(LR::Neither)
                            },
                            Some(LR::Left(lval)) => {
                                // it exploded; we need to handle a val up-left and return Some
                                // We're already in the L-branch so we must pass the val up again
                                Some(LR::Left(lval))
                            },
                            Some(LR::Right(rval)) => {
                                // add the val to our right element. this must always succeed, so we return Neither
                                match &mut *self.right {
                                    Element::Regular(x) => {
                                        self.right = Box::new(Element::Regular(*x+rval));
                                    },
                                    Element::Snailfish(rsnail) => {
                                        rsnail.add_explode_val(LR::Left(rval)); // Note it needs to be applied in closest (l-most element)
                                    },
                                }
                                Some(LR::Neither)
                            }
                        }
                    }
                }
            },
        };

        match l_explode {
            Some(_) => l_explode,
            None => {
                match &mut *self.right {
                    Element::Regular(_) => None,
                    Element::Snailfish(snail) => {
                        match (&*snail.left, &*snail.right) {
                            (Element::Regular(lval), Element::Regular(rval)) => {
                                if depth >= DEPTH {
                                    // Explode!
                                    // Close the borrows so we can reassign self.left
                                    let lval = *lval;
                                    let rval = *rval;
                                    self.right = Box::new(Element::Regular(0));
                                    match &mut *self.left {
                                        Element::Regular(x) => {
                                            self.left = Box::new(Element::Regular(*x+lval));
                                        },
                                        Element::Snailfish(lsnail) => {
                                            lsnail.add_explode_val(LR::Right(lval)); // Add the rval to the closest (leftmost) sub-element
                                        },
                                    };
                                    Some(LR::Right(rval))  // Parent needs to consume lval in closest on left (turn to R if passed down again)
                                } else {
                                    None
                                }
                            },
                            _ => {
                                match snail.explode(depth+1) {
                                    None => None,
                                    Some(LR::Neither) => {
                                        // something exploded, but all values have already been handled
                                        Some(LR::Neither)
                                    },
                                    Some(LR::Right(rval)) => {
                                        // it exploded; we need to handle a val up-right and return Some
                                        // We're already in the R-branch so we must pass the val up again
                                        Some(LR::Right(rval))
                                    },
                                    Some(LR::Left(lval)) => {
                                        // add the val to our left element. this must always succeed, so we return Neither
                                        match &mut *self.left {
                                            Element::Regular(x) => {
                                                self.left = Box::new(Element::Regular(*x+lval));
                                            },
                                            Element::Snailfish(lsnail) => {
                                                lsnail.add_explode_val(LR::Right(lval)); // Note it needs to be applied in closest (l-most element)
                                            },
                                        }
                                        Some(LR::Neither)
                                    }
                                }
                            }
                        }
                    },
                }
            }
        }
    }

    fn add_explode_val(&mut self, _lr: LR) {
        // TODO
    }

    fn split(&self) -> Option<()> {
        None
    }

    fn magnitude(&self) -> u32 {
        3 * self.left.value() + 2 * self.right.value()
    }
}

impl fmt::Display for Snailfish {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{},{}]", self.left, self.right)
    }
}

impl fmt::Display for Element {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Element::Snailfish(snail) => write!(f, "{}", snail),
            Element::Regular(val) => write!(f, "{}", val),
        }
    }
}

fn main() {
    println!("Hello, world!");
    println!("{}", Snailfish::parse_str(&"[1,2]"));
    println!("{}", Snailfish::parse_str(&"[[3,4],2]"));
    println!("{}", Snailfish::parse_str(&"[1,[5,6]]"));
    println!("{}", Snailfish::parse_str(&"[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"));
    let mut snail_one = Snailfish::parse_str(&"[1,2]");
    snail_one.add(Snailfish::parse_str(&"[[3,4],5]"));
    println!("{}", snail_one);
    snail_one.reduce();
    println!("{}", snail_one);

    // explodes
    let mut snail = Snailfish::parse_str(&"[[[[[9,8],1],2],3],4]");
    snail.explode(1);
    println!("{}", snail);
    let mut snail = Snailfish::parse_str(&"[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]");
    snail.explode(1);
    println!("{}", snail);
    snail.explode(1);
    println!("{}", snail);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_magnitue() {
        assert_eq!(Snailfish::parse_str(&"[0,0]").magnitude(), 0);
        assert_eq!(Snailfish::parse_str(&"[[1,2],[[3,4],5]]").magnitude(), 143);
        assert_eq!(Snailfish::parse_str(&"[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude(), 1384);
        assert_eq!(Snailfish::parse_str(&"[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude(), 445);
        assert_eq!(Snailfish::parse_str(&"[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude(), 791);
        assert_eq!(Snailfish::parse_str(&"[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude(), 1137);
        assert_eq!(Snailfish::parse_str(&"[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude(), 3488);
    }
}
