use std::fs;
use std::collections::HashMap;

fn main() {
    let day1 = fs::read_to_string("src/input/day1.txt").expect("Should have been able to read the file");
    let lines = day1.split('\n');

    let mut total: u32 = 0;
    for line in lines {
        let chars = line.split("");
        let mut first_char: String = "".to_string();
        let mut last_char: &str = "";
        for char in chars {
            match char.parse::<u8>() {
                Ok(_) => {
                    if first_char == "" {
                        first_char = char.to_string();
                    }
                    last_char = char;
                },
                Err(_) => continue,
            };
        }
        // println!("First char is {first_char} and last_char is {last_char} of line {line}");
        let numeric_string = first_char + last_char;
        let number: u8 = numeric_string.parse().expect("number is not a number");
        total += number as u32;
    }
    println!("part 1 answer is {total}");
    
    let mut total2: u32 = 0;
    let mut letter_map = HashMap::new();
    
    letter_map.insert(String::from("one"), "1");
    letter_map.insert(String::from("two"), "2");
    letter_map.insert(String::from("three"), "3");
    letter_map.insert(String::from("four"), "4");
    letter_map.insert(String::from("five"), "5");
    letter_map.insert(String::from("six"), "6");
    letter_map.insert(String::from("seven"), "7");
    letter_map.insert(String::from("eight"), "8");
    letter_map.insert(String::from("nine"), "9");
    
    let lines2 = day1.split('\n');
    for line in lines2 {
        let mut first_char: String = String::from("");
        let mut last_char: String = String::from("");
        
        for (c, char) in line.chars().enumerate() {
            match char.to_string().parse::<u8>() {
                Ok(_) => {
                    if first_char == "" {
                        first_char = char.to_string();
                    }
                    last_char = char.to_string();
                }
                Err(_) => {
                    for (letter, number_str) in &letter_map {
                        if line[c..].starts_with(letter) {
                            if first_char == "" {
                                first_char = number_str.to_string();
                            }
                            last_char = number_str.to_string();
                        }
                    }
                }
            }
        }
        let numeric_string = first_char + &last_char;
        let number: u8 = numeric_string.parse().expect("number is not a number");
        total2 += number as u32;
    }
    println!("part2 answer is {total2}")
}
