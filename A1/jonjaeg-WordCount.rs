// Import necessary crates and modules
use clap::{Arg, Command}; // For parsing command-line arguments
use std::collections::HashMap; // For storing word counts
use std::fs; // For reading files
use std::io::{self, Read}; // For reading input (file or stdin)

fn main() -> io::Result<()> {
    // Define the command-line arguments using the `clap` crate
    let args = Command::new("Word Count")
        .arg(Arg::new("ignore_case")
            .short('I') // Short flag: -I
            .help("Ignore case (convert to lowercase)") // Description of the flag
            .action(clap::ArgAction::SetTrue)) // Sets the flag to true if provided
        .arg(Arg::new("list")
            .short('l') // Short flag: -l
            .help("List words with frequencies") // Description of the flag
            .action(clap::ArgAction::SetTrue)) // Sets the flag to true if provided
        .arg(Arg::new("filename")
            .required(false) // This argument is optional
            .help("Text file to process")) // Description of the argument
        .get_matches(); // Parse the arguments

    // Read input either from a file or stdin
    let mut contents = String::new();
    if let Some(filename) = args.get_one::<String>("filename") {
        // If a filename is provided, read the file's contents
        contents = fs::read_to_string(filename)?;
    } else {
        // If no filename is provided, read from standard input (stdin)
        io::stdin().read_to_string(&mut contents)?;
    }

    // Check if the "ignore_case" flag is set
    let ignore_case = args.get_flag("ignore_case");
    // Check if the "list" flag is set
    let list_words = args.get_flag("list");





    // Create a HashMap to store word counts
    let mut word_counts: HashMap<String, usize> = HashMap::new();
    let mut total_words = 0; // Counter for total words

    // Define a regular expression to split words on non-alphanumeric characters
    let re = regex::Regex::new(r"[^\p{L}\p{N}]+").unwrap();

    // Iterate over the words in the input
    for raw_word in re.split(&contents) {
        if raw_word.is_empty() {
            continue; // Skip empty words
        }

        // Convert the word to lowercase if "ignore_case" is set, otherwise use it as is
        let word = if ignore_case {
            raw_word.to_lowercase()
        } else {
            raw_word.to_string()
        };

        total_words += 1; // Increment the total word count
        *word_counts.entry(word).or_insert(0) += 1; // Increment the count for the word
    }



    
    if list_words {
        // If the "list" flag is set, display the word frequencies
        let mut word_vec: Vec<(String, usize)> = word_counts.into_iter().collect();

        // Sort the words by descending frequency, then alphabetically
        word_vec.sort_by(|a, b| b.1.cmp(&a.1).then(a.0.cmp(&b.0)));

        // Print each word and its frequency
        for (word, count) in word_vec {
            println!("{}\t{}", word, count);
        }
    } else {
        // If the "list" flag is not set, display the total number of unique words
        // and the total number of words
        println!("{} / {}", word_counts.len(), total_words); // Format: unique words / total words
    }

    Ok(()) // Indicate successful execution
}
