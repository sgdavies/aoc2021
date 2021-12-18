use std::fmt;

#[derive(Debug)]
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

#[derive(Debug)]
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
    
    fn add(left: Snailfish, right: Snailfish) -> Snailfish {
        Snailfish { left: Box::new(Element::Snailfish(left)), right: Box::new(Element::Snailfish(right)) }
    }

    fn reduce(&mut self) {
        loop {
            if let Some(_explode) = self.explode() {
                //
            } else if let Some(_split) = self.split() {
                //
            } else {
                // no more reducing to do
                return;
            }
        }
    }

    fn explode(&mut self) -> Option<()> {
        if let Some(e_left) = Snailfish::explode_element(&*self.left, 1) {
            self.left = Box::new(e_left);
            Some(())
        } else if let Some(e_right) = Snailfish::explode_element(&*self.right, 1) {
            self.right = Box::new(e_right);
            Some(())
        } else {
            None
        }
    }

    fn explode_element(elem: &Element, _depth: u8) -> Option<Element> {
        match elem {
            Element::Snailfish(_snail) => {
                Some(Element::Regular(77))
            },
            Element::Regular(_) => None,
        }
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
    // println!("{}", Snailfish::parse_str(&"1,2]"));
    let snail_one = Snailfish::parse_str(&"[1,2]");
    let snail_two = Snailfish::parse_str(&"[[3,4],5]");
    let mut snail_one = Snailfish::add(snail_one, snail_two);
    println!("{}", snail_one);
    snail_one.reduce();
    println!("{}", snail_one);
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
