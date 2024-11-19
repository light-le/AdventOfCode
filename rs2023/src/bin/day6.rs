use std::{fs, iter::{zip, Zip}, vec::IntoIter};

fn count_winning_times(time: u32, record_distance: u64) -> u32 {
    let mut winnings = 0;

    for charge_time in 1..time {
        let speed = charge_time;
        let run_time = time - charge_time;
        let distance: u64 = (run_time as u64) * (speed as u64);
        if distance > record_distance {
            winnings += 1;
        }
    }
    winnings
}


fn solve_part1(time_distances: Zip<IntoIter<&str>, IntoIter<&str>>) -> u32 {
    let mut winnings: u32 = 1;
    for (timestr, distancestr) in time_distances {
        let time: u32 = timestr.parse().expect("could not convert time str");
        let distance: u64 = distancestr.parse().expect("could not convert dist str");

        winnings *= count_winning_times(time, distance);
    }

    winnings
}


fn solve_part2(timestr: &str, distancestr: &str) -> u32 {
    let time: u32 = timestr.replace(" ", "").parse().expect("could not convert time");
    let distance: u64 = distancestr.replace(" ", "").parse().expect("could not convert distance");

    count_winning_times(time, distance)
}


fn main() {
    let day6 = fs::read_to_string("src/input/day6.txt").expect("could not read file");
    let mut lines = day6.split("\n");

    let time_text = lines.next().unwrap();
    let distance_text = lines.next().unwrap();

    let (_time_str, timestr) = time_text.split_at(time_text.find(":").unwrap()+2);
    let (_dist_str, distancestr) = distance_text.split_at(distance_text.find(":").unwrap()+2);

    let times: Vec<&str> = timestr.trim().split_ascii_whitespace().collect();
    let distances: Vec<&str> = distancestr.trim().split_ascii_whitespace().collect();

    let part1_answer = solve_part1(zip(times, distances));
    assert_eq!(part1_answer, 138915);
    println!("part1 answer is {part1_answer}");

    let part2_answer = solve_part2(timestr, distancestr);
    assert_eq!(part2_answer, 27340847);
    println!("part2 answer is {part2_answer}");
}