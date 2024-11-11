use std::{cmp, collections::HashMap, fs};

fn main() {
    let day2 = fs::read_to_string("src/input/day2.txt").expect("Could not read file day2.txt");
    let lines = day2.split("\n");

    let mut part1_cube_map: HashMap<String, u8> = HashMap::new();

    part1_cube_map.insert(String::from("red"), 12);
    part1_cube_map.insert(String::from("green"), 13);
    part1_cube_map.insert(String::from("blue"), 14);

    let mut possible_id_sum: u32 = 0;
    for (l, line) in lines.enumerate() {
        possible_id_sum += l as u32 + 1;
        let (_, info) = line.split_at(line.find(": ").unwrap()+2);
        let cube_sets = info.split("; ");
        'game: for cube_set in cube_sets {
            let cube_counts = cube_set.split(", ");
            for cube_count in cube_counts {
                let (cubec, cube_col) = cube_count.split_at(cube_count.find(" ").unwrap()+1);
                let cuben: u8 = cubec.trim().parse().expect(concat!("could not parse ", stringify!($cubec)));
                if cuben > part1_cube_map.get(cube_col).copied().unwrap() {
                    possible_id_sum -= l as u32 + 1;
                    break 'game
                }

            }
        }
    }
    println!("part 1 answer is {possible_id_sum}");


    let mut fewest_sum: u64 = 0;
    let lines2 = day2.split("\n");
    for line in lines2 {
        let (_, info) = line.split_at(line.find(":").unwrap() + 2);
        let mut minimum_cube: HashMap<&str, u8> = HashMap::new();
        let cube_sets = info.split("; ");
        for cube_set in cube_sets {
            let cube_counts = cube_set.split(", ");
            for cube_count in cube_counts {
                let (cubec, cube_col) = cube_count.split_at(cube_count.find(" ").unwrap() + 1);
                let cuben: u8 = cubec.trim().parse().expect("Could not convert to u8");
                let max_cube = minimum_cube.entry(cube_col).or_insert(0);
                *max_cube = cmp::max(*max_cube, cuben);
            }
        }

        let mut line_sum: u64 = 1;
        for (_, value) in minimum_cube {
            line_sum *= value as u64;
        }
        fewest_sum += line_sum;
    }
    println!("part 2 answer is {fewest_sum}")
}