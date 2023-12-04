use std::collections::HashMap;
use std::fmt;
use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::str::FromStr;
use std::vec::Vec;

#[derive(Eq, Hash, PartialEq, Clone)]
enum Color {
    Red,
    Green,
    Blue,
}

impl FromStr for Color {
    type Err = ();

    fn from_str(input: &str) -> Result<Color, Self::Err> {
        match input {
            "red" => Ok(Color::Red),
            "green" => Ok(Color::Green),
            "blue" => Ok(Color::Blue),
            _ => Err(()),
        }
    }
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Color::Red => write!(f, "Red"),
            Color::Green => write!(f, "Green"),
            Color::Blue => write!(f, "Blue"),
        }
    }
}

struct Game {
    id: i64,
    rules: HashMap<Color, i64>,
    rounds: Vec<(Color, i64)>,
}

impl Game {
    pub fn new(id: i64, rules: HashMap<Color, i64>, rounds: Vec<(Color, i64)>) -> Game {
        Game { id, rules, rounds }
    }

    pub fn validate(&self) -> bool {
        let mut valid: bool = true;
        for (color, num_balls) in &self.rounds {
            match self.rules.get(color) {
                Some(rule_balls) => {
                    if num_balls > rule_balls {
                        valid = false;
                    }
                }
                None => {
                    panic!("WOOPS!");
                }
            }
        }
        valid
    }

    pub fn powers(&self) -> i64 {
		let mut max_found: HashMap<Color, i64> = HashMap::from([
			(Color::Red, 0),
			(Color::Green, 0),
			(Color::Blue, 0),	
		]);
    
    	for (color, num_balls) in &self.rounds {
    		match max_found.get(color) {
    			Some(max_color_balls) => {
    				if num_balls > max_color_balls {
    					max_found.insert(color.clone(), *num_balls);
    				}
    			}
    			None => {
    				panic!("Unknown color!");
    			}
    		}
    	}

		let mut result: i64 = 0;
		
    	for val in max_found.values() {
    		if result == 0 {
    			result += val
    		}
    		else {
    			result *= val
    		}
    	}

    	result
    }
}

pub fn a() -> io::Result<()> {
    let file = File::open("data/2/a.txt")?;
    let reader = BufReader::new(file);

    let mut sum: i64 = 0;
    let mut powersum: i64 = 0;

    for line in reader.lines() {
        let mut line_tmp = line?;

        if let Some(stripped) = line_tmp.strip_prefix("Game ") {
            line_tmp = stripped.to_string();
        } else {
            panic!("Woops!");
        }

        let colon_split: Vec<&str> = line_tmp.split(':').collect();
        let round_split: Vec<&str> = colon_split[1].split(';').collect();

        let mut rounds: Vec<(Color, i64)> = Vec::new();

        for round_str in round_split {
            let color_split: Vec<&str> = round_str.split(',').collect();

            for color_str in color_split {
                let color_tmp = color_str.trim();

                let num_color: Vec<&str> = color_tmp.split(' ').collect();

                let num_balls: i64 = num_color[0].parse::<i64>().unwrap();
                let color: Color = num_color[1].parse::<Color>().unwrap();

                rounds.push((color, num_balls));
            }
        }

        // Construct Game object
        let id = colon_split[0].parse::<i64>().unwrap();
        let rules: HashMap<Color, i64> =
            HashMap::from([(Color::Red, 12), (Color::Green, 13), (Color::Blue, 14)]);

        let game: Game = Game::new(id, rules, rounds);

        if game.validate() {
            sum += game.id;
        }

        powersum += game.powers();
    }

    println!("Answer 2A: {}", sum);
    println!("Answer 2B: {}", powersum);

    Ok(())
}
