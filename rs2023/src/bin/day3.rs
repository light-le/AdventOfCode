use std::{cmp, collections::HashMap, fs};

fn contains_symbols(s: &str) -> bool{
    let mut answer: bool = false;
    for char in s.chars() {
        if !char.is_ascii_digit() && char != '.' {
            answer = true;
            break
        } 
    }
    answer
}

fn find_gears(s: &str) -> Vec<usize> {
    let mut gears: Vec<usize> = Vec::new();
    for (c, char) in s.chars().enumerate() {
        if char == '*' {
            gears.push(c);
        }
    }
    gears
}


fn main() {
    let day3 = fs::read_to_string("src/input/day3.txt").expect("Could not read day3.txt");
    let lines: std::str::Split<'_, &str> = day3.split("\n");

    let height = lines.clone().count();
    let mut totalp1: u32 = 0;

    let mut linevec: Vec<String> = Vec::new();
    for line in lines.clone() {
        linevec.push(line.to_string());
    }
    let width = linevec[0].len();

    for (l, line) in lines.clone().enumerate() {
        let mut num_str: String = String::new();
        let mut num_i: i16 = -1;
        for (c, char) in line.chars().enumerate() {
            if char.is_ascii_digit() {
                num_str.push(char);
                num_i = if num_i == -1 {c as i16} else {num_i};

                if c == width - 1 {
                    if num_i != -1 {
                        for row in &linevec[cmp::max(0, l as i16-1) as usize..cmp::min(height, l+2)] {
                            if contains_symbols(&row[cmp::max(0, num_i - 1) as usize..cmp::min(width, c+1)]) {
                                let number: u32 = num_str.parse().expect("Could not convert str to number");
                                totalp1 += number;
                                break
                            }
                        }   
                    }
                    num_i = -1;
                    num_str.clear();
                }
            } else {
                if num_i != -1 {
                    for row in &linevec[cmp::max(0, l as i16-1) as usize..cmp::min(height, l+2)] {
                        if contains_symbols(&row[cmp::max(0, num_i - 1) as usize..cmp::min(width, c+1)]) {
                            let number: u32 = num_str.parse().expect("Could not convert str to number");
                            totalp1 += number;
                            break
                        }
                    }   
                }
                num_i = -1;
                num_str.clear();
            }
        }
    }
    println!("part 1 answer is {totalp1}");
    
    let mut gear_map: HashMap<String, Vec<u32>> = HashMap::new();
    
    
    let mut totalp2: u32 = 0;
    for (l, line) in lines.enumerate() {
        let mut num_str: String = String::new();
        let mut num_i: i16 = -1;
        for (c, char) in line.chars().enumerate() {
            if char.is_ascii_digit() {
                num_str.push(char);
                num_i = if num_i == -1 {c as i16} else {num_i};
                
                if num_i == (width - num_str.len()) as i16 {
                    let number: u32 = num_str.parse().expect("Could not convert str to number");
                    for r in cmp::max(0, l as i16-1) as usize..cmp::min(height, l+2) {
                        let row = &linevec[r];
                        let gears = find_gears(&row[cmp::max(0, num_i - 1) as usize..cmp::min(width, c+1)]);
                        for gear in gears {
                            let true_gear = if num_i == 0 {gear} else {gear + num_i as usize - 1};
                            let gear_id: String = true_gear.to_string() + "," + r.to_string().as_str();
                            let ratios = gear_map.entry(gear_id).or_insert(Vec::new());
                            ratios.push(number);
                        }
                    }
                    num_i = -1;
                    num_str.clear();
                }
            } else {
                if num_i != -1 {
                    let number: u32 = num_str.parse().expect("Could not convert str to number");
                    for r in cmp::max(0, l as i16-1) as usize..cmp::min(height, l+2) {
                        let row = &linevec[r];
                        let gears = find_gears(&row[cmp::max(0, num_i - 1) as usize..cmp::min(width, c+1)]);
                        for gear in gears {
                            let true_gear = if num_i == 0 {gear} else {gear + num_i as usize - 1};
                            let gear_id: String = true_gear.to_string() + "," + r.to_string().as_str();
                            let ratios = gear_map.entry(gear_id).or_insert(Vec::new());
                            ratios.push(number);
                        }
                    }
                    num_i = -1;
                    num_str.clear();
                }
            }
        }
    }

    for (_gear, ratios) in gear_map {
        if ratios.len() == 2 {
            totalp2 += ratios[0] * ratios[1];
        }
    }
    println!("part 2 answer is {totalp2}");
}