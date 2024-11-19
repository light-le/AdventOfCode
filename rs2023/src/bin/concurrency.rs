use std::{cmp, collections::HashMap, sync::mpsc, thread, time::Duration};

fn main() {
    // let memory = vec![0, 1, 2, 3, 4, 5, 6, 7];
    let memory: Vec<u8> = (0..80).collect();
    let mapping: HashMap<u8, u8> = HashMap::from([
        (0, 11), (1,13), (2, 17), (3, 19), (4, 23)
    ]);

    let mut min_result: u8 = 200;
    for m in (0..80).step_by(8) {
        let mem = memory[m..m+8].to_vec();
        let concurrent_result = concurrent_mapping(mem, &mapping);
        println!("{concurrent_result:?}");
        min_result = cmp::min(min_result, *concurrent_result.iter().min().unwrap());
    } 


    println!("{min_result:?}");
}

fn concurrent_mapping(memory: Vec<u8>, mapping: &HashMap<u8, u8>) -> Vec<u8> {
    let (tx, rx) = mpsc::channel();
    let mut result: Vec<u8> = Vec::new();

    // let mut handles = vec![];

    for t in 0..8 {
        let this_value = memory[t].clone();
        let new_mapping = mapping.clone();
        let tx = tx.clone();
        thread::spawn(move || {
            let next_value = new_mapping.get(&this_value).copied().unwrap_or(this_value);
            tx.send(next_value).unwrap();
            thread::sleep(Duration::from_secs(1));
        });
        // handles.push(handle);
    }

    // for handle in handles {
    //     handle.join().unwrap();
    // }
    drop(tx);

    for rec in rx {
        println!("{rec}");
        result.push(rec);
    }

    result
}