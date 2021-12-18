#[derive(Debug)]
enum Element {
    Regular(u8),
    Snailfish(Snailfish)
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
println!("parse left: {}", s);
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
println!("parse right: {}", s);
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
    
}

fn main() {
    println!("Hello, world!");
    println!("{:?}", Snailfish::parse_str(&"[1,2]"));
    println!("{:?}", Snailfish::parse_str(&"[[3,4],2]"));
    println!("{:?}", Snailfish::parse_str(&"[1,[5,6]]"));
    println!("{:?}", Snailfish::parse_str(&"[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"));
    // println!("{:?}", Snailfish::parse_str(&"1,2]"));
}
