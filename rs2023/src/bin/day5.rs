use std::{array, cmp, collections::HashMap, fs, sync::mpsc, thread::{self, spawn}};

fn parse_section_text(text: &str) -> Vec<(u64, u64, u64)> {
    let mut section_map: Vec<(u64, u64, u64)> = Vec::new();
    let section_line = text.split("\n");

    for (l, line) in section_line.enumerate() {
        if l == 0 {
            continue;
        }
        let mut numstring = line.trim().splitn(3, " ");
        let dest: u64 = numstring.next().unwrap().parse().expect("could not get dest");
        let source: u64 = numstring.next().unwrap().parse().expect("could not get source");
        let steps: u64 = numstring.next().unwrap().parse().expect("could not get steps");

        section_map.push((dest, source, steps));
    }
    section_map
}

fn build_almanac(text: Vec<&str>) -> [Vec<(u64, u64, u64)>; 7] {
    let almanac: [Vec<(u64, u64, u64)>; 7] = array::from_fn::<_, 7, _>(|i| parse_section_text(text[i]));
    almanac
}

fn get_part1_seeds(seed: &str) -> Vec<u64> {
    let mut seed_splits = seed.split_ascii_whitespace();
    let _seed_str: &str = seed_splits.next().unwrap();
    
    let mut part1_seeds: Vec<u64> = Vec::new();
    
    for seed_value in seed_splits {
        part1_seeds.push(seed_value.parse::<u64>().expect("could not convert str to u64"));
    }
    part1_seeds
}

fn get_part2_seeds(seed: &str) -> Vec<u64> {
    let mut seed_splits = seed.split_ascii_whitespace();
    let _seed_str: &str = seed_splits.next().unwrap();

    let mut part2_seeds: Vec<u64> = Vec::new();

    let mut source_seed: u64 = 0;
    for (ss, seed_value) in seed_splits.enumerate() {
        if ss % 2 == 0 {
            source_seed = seed_value.parse().expect("could not convert");
        } else {
            for step in 0..seed_value.parse::<u64>().expect("could not convert") {
                part2_seeds.push(source_seed+step);
            }
            // let p2_seed_count: usize = part2_seeds.len();
        }
    }
    
    part2_seeds
}

fn find_lowest_location(seeds: Vec<u64>, almanac: &[Vec<(u64, u64, u64)>; 7]) -> u64{
    let mut locations: Vec<u64> = Vec::new();
    for seed in seeds {
        let mut value = seed;
        for section in almanac {
            for (dest, source, steps) in section {
                if value >= *source && value < source + steps {
                    value = dest + (value - source);
                    break
                }
            }
        }
        locations.push(value);
        
    }

    *locations.iter().min().unwrap()
}

fn get_location(seed: u64, almanac: &[Vec<(u64, u64, u64)>; 7]) -> u64 {
    let mut value = seed;
    for section in almanac {
        for (dest, source, steps) in section {
            if value >= *source && source + steps > value {
                value = dest + (value - source);
                break
            }
        }
    }
    value
}

fn concurrent_lookup (seeds: Vec<u64>, almanac: &[Vec<(u64, u64, u64)>; 7]) -> u64 {
    let (tx, rx) = mpsc::channel();
    let mut min_location: u64 = 1000000000000;
    for t in 0..8 {
        let this_seed = seeds[t].clone();
        let tx = tx.clone();
        // let new_almanac = almanac.clone();
        thread::spawn(move || {
            let value = this_seed;
            // let value = get_location(this_seed, almanac);
            tx.send(value).unwrap();
        });
    }
    drop(tx);
    for location_received in rx {
        min_location = cmp::min(min_location, location_received);
    }
    min_location
}


fn find_lowest_location_concurrency(seeds: Vec<u64>, almanac: &[Vec<(u64, u64, u64)>; 7]) -> u64 {
    let mut min_location: u64 = 1000000000000;
    let threads: usize = 8;

    // let mut received_count: u64 = 0;
    for s in (0..seeds.len()).step_by(threads) {
        let seeds_round = seeds[s..s+threads].to_vec();
        let new_min_location = cmp::min(min_location, concurrent_lookup(seeds_round, almanac));
        if new_min_location < min_location {
            min_location = new_min_location;
            println!("min location is now {min_location}")
        }

        if s % 1000000 == 0 {
            let pct = s*100/seeds.len();
            println!("{s} {pct}%");
        }
    }
    min_location
}


fn main () {
    let day5 = fs::read_to_string("src/input/day5.txt").expect("cannot read file");
    let sections = day5.split("\n\n");

    let mut seed: &str = "";
    let mut almanac_text: Vec<&str> = Vec::new();
    
    for (s, section) in sections.enumerate() {
        if s == 0 {
            seed = section;
        } else if  s > 0 {
            almanac_text.push(section);
        }
    }

    let almanac = build_almanac(almanac_text);
    
    println!("Finished building almanac");
    
    let part1_seeds = get_part1_seeds(seed);    
    let part1_answer = find_lowest_location(part1_seeds, &almanac);
    // assert_eq!(part1_answer, 35);
    // assert_eq!(part1_answer, 424490994);
    println!("part1 answer is {part1_answer}");


    let part2_seeds = get_part2_seeds(seed);
    println!("begin finding lowest location for part 2");
    let part2_answer = find_lowest_location_concurrency(part2_seeds, &almanac);
    // assert_eq!(part2_answer, 46);
    // assert_eq!(part2_answer, 15290096);
    println!("part2 answer is {part2_answer}");
}