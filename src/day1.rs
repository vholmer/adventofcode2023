use std::fs::File;
use std::io::{self, BufRead, BufReader};

pub fn a() -> io::Result<()> {
    let file = File::open("data/1/a.txt")?;
    let reader = BufReader::new(file);

    let mut sum: i64 = 0;

    for line in reader.lines() {
        let line_tmp = line?;

        let first_digit_index: usize = line_tmp.find(char::is_numeric).unwrap();
        let last_digit_index: usize = line_tmp.rfind(char::is_numeric).unwrap();

        let first_digit: char = line_tmp.chars().nth(first_digit_index).unwrap();
        let last_digit: char = line_tmp.chars().nth(last_digit_index).unwrap();

        let combined_digit = format!("{}{}", first_digit, last_digit)
            .parse::<i64>()
            .unwrap();

        sum += combined_digit;
    }

    println!("Answer 1A: {}", sum);

    Ok(())
}

pub fn b() -> io::Result<()> {
    let file = File::open("data/1/a.txt")?;
    let reader = BufReader::new(file);

    let mut sum: i64 = 0;

    for line in reader.lines() {
        let line_tmp = line?;

        let mut cur_substr = String::new();

        //println!("Original line: {}", line_tmp);

        for char in line_tmp.chars() {
            cur_substr.push(char);

            cur_substr = cur_substr.replace("one", "o1e");
            cur_substr = cur_substr.replace("two", "t2o");
            cur_substr = cur_substr.replace("three", "t3e");
            cur_substr = cur_substr.replace("four", "f4r");
            cur_substr = cur_substr.replace("five", "f5e");
            cur_substr = cur_substr.replace("six", "s6x");
            cur_substr = cur_substr.replace("seven", "s7n");
            cur_substr = cur_substr.replace("eight", "e8t");
            cur_substr = cur_substr.replace("nine", "n9e");
        }

        //println!("Replaced line: {}", cur_substr);

        let first_digit_index: usize = cur_substr.find(char::is_numeric).unwrap();
        let last_digit_index: usize = cur_substr.rfind(char::is_numeric).unwrap();

        let first_digit: char = cur_substr.chars().nth(first_digit_index).unwrap();
        let last_digit: char = cur_substr.chars().nth(last_digit_index).unwrap();

        let combined_digit: i64 = format!("{}{}", first_digit, last_digit)
            .parse::<i64>()
            .unwrap();

        //println!("Combined digit: {}", combined_digit);
        //println!("--------------");

        sum += combined_digit;
    }

    println!("Answer 1B: {}", sum);

    Ok(())
}
