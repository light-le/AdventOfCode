use std::{collections::{HashMap, HashSet}, fs, str::Split};

fn solve_part1(card_str: Split<'_, &str>) -> u32 {
    let mut total_points: u32 = 0;
    for (_, card) in card_str.enumerate() {
        let (_card_id, card_numbers) = card.split_at(card.find(":").unwrap() + 2);
        let (winning, actual) = card_numbers.split_at(card_numbers.find("|").unwrap());

        let winning_cards = winning.trim().split_whitespace();
        let actual2 = actual.replace("|", "");
        let actual_cards = actual2.trim().split_whitespace();

        let mut winning_book: HashSet<&str> = HashSet::new();

        for wcard in winning_cards {
            winning_book.insert(wcard);
        }
        let mut card_points: u32 = 0;
        for acard in actual_cards{
            if winning_book.contains(acard) {
                card_points = if card_points == 0 {1} else {card_points*2};
            }
        }
        total_points += card_points;
    }
    total_points
}

fn solve_part2(card_str: Split<'_, &str>) -> u32 {
    let mut total_copies: HashMap<u8, u32> = HashMap::new();
    
    for (l, line) in card_str.enumerate() {
        let current_card_num = l + 1;
        let (_card_id, card_numbers) = line.split_at(line.find(":").unwrap() + 2);
        let (winning, actual) = card_numbers.split_at(card_numbers.find("|").unwrap());
    
        let winning_cards = winning.trim().split_whitespace();
        let actual2 = actual.replace("|", "");
        let actual_cards = actual2.trim().split_whitespace();
    
        let mut winning_book: HashSet<&str> = HashSet::new();
    
        for wcard in winning_cards {
            winning_book.insert(wcard);
        }
        
        let mut card_num = current_card_num;
        let current_card_count = total_copies.get(&(current_card_num as u8)).copied().unwrap_or(1);
        
        for acard in actual_cards {
            if winning_book.contains(acard) {
                card_num += 1;
                let card_copy = total_copies.entry(card_num as u8).or_insert(1);
                *card_copy += current_card_count;
            }
        }
        total_copies.entry(current_card_num as u8).or_insert(1);
    }
    total_copies.values().sum()
}


fn main() {
    let day4 = fs::read_to_string("src/input/day4.txt").expect("could not read file");
    let lines = day4.split("\n");

    let part1_answer = solve_part1(lines.clone());
    println!("part1 answer is {part1_answer}");
    
    
    let part2_answer = solve_part2(lines.clone());
    println!("part2 answer is {part2_answer}");

}