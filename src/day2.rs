use std::fs::File;
use std::collections::HashMap;
use std::vec::Vec;
use std::io::{self, BufRead, BufReader};

enum Color {
	Blue,
	Red,
	Green,
}

struct Game {
	id: i64,
	rules: Vec<(Color, i64)>,
	rounds: Vec<(Color, i64)>
}

impl Game {
	pub fn new(id: i64, rules: Vec<(Color, i64)>) -> Game {
		Game {
			id,
			rules,
			rounds: Vec::new()
		}
	}

	// TODO: Add a function here for summing IDs given rules
}

pub fn a() -> io::Result<()> {
	let file = File::open("data/2/a.txt")?;
	let reader = BufReader::new(file);

	for line in reader.lines() {
		let mut line_tmp = line?;

		if let Some(stripped) = line_tmp.strip_prefix("Game ") {
			line_tmp = stripped.to_string();
		}
		else {
			panic!("Woops!");
		}

		let colon_split: Vec<&str> = line_tmp.split(':').collect();
		let round_split: Vec<&str> = colon_split[1].split(';').collect();

		let rounds: Vec<(Color, i64)> = Vec::new();

		for round_str in round_split {
			let color_split: Vec<&str> = round_str.split(',').collect();

			for color_str in color_split {
				let color_tmp = color_str;

				// TODO:
				// Here we have something like '3 blue'
				// Next step is split on ' ' and then finally start pushing tuples to the rounds vec.
			}
		}
		
		// Construct Game object
		let id = colon_split[0].parse::<i64>().unwrap();
		let rules: Vec<(Color, i64)> = vec![(Color::Red, 12), (Color::Green, 13), (Color::Blue, 14)];
		
	}

	Ok(())
}
