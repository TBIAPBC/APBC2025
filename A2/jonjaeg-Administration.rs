use std::collections::HashSet; // For storing unique solutions
use std::io; // For reading input from stdin
use std::fs; // For reading input from a file
use std::io::Read; // For reading strings from input

use clap::{Arg, Command}; // For parsing command-line arguments

fn main() {
    // Define the command-line arguments using the `clap` crate
    let args = Command::new("Authority Assignment Solver")
        .version("0.1.0")
        .about("Solves partitioning cities into authorities under cost constraints")
        .arg(Arg::new("optimize")
            .short('o')
            .long("optimize")
            .help("Optimize mode: find minimum cost solution"))
        .arg(Arg::new("filename")
            .required(false) // This argument is optional
            .help("Text file to process"))
        .get_matches();

    // Check if the "optimize" flag is set
    let optimize = args.contains_id("optimize");

    // Read input data (either from a file or stdin)
    let mut contents = String::new();
    if let Some(filename) = args.get_one::<String>("filename") {
        // If a filename is provided, read the file's contents
        contents = fs::read_to_string(filename)
            .unwrap_or_else(|err| {
                eprintln!("Error reading file {}: {}", filename, err);
                std::process::exit(1);
            });
    } else {
        // If no filename is provided, read from standard input (stdin)
        io::stdin().read_to_string(&mut contents)
            .unwrap_or_else(|err| {
                eprintln!("Error reading from stdin: {}", err);
                std::process::exit(1);
            });
    }

    // Parse the input into capitals, cost matrix, and cost limit
    let (capital_letters, matrix, cost_limit) = parse_input(&contents);

    // Convert capital letters into strings for easier manipulation
    let capitals: Vec<String> = capital_letters.iter().map(|&c| c.to_string()).collect();
    let n = capitals.len();

    // Ensure the number of capitals is even (required for pairing)
    if n % 2 != 0 {
        eprintln!("Error: Number of capitals must be even.");
        std::process::exit(1);
    }

    // Create a list of city indices (0 to n-1)
    let cities: Vec<usize> = (0..n).collect();
    let mut solutions = HashSet::new(); // To store unique solutions
    let mut bound = cost_limit; // Initialize the cost bound

    // Precompute the minimal edge costs for each city
    let minimal_edges = compute_minimal_edges(&matrix);

    // Perform depth-first search with branch-and-bound optimization
    dfs(
        &mut cities.clone(), // Clone the list of cities to avoid modifying the original
        &mut vec![], // Start with an empty list of current pairs
        0, // Initial cost is 0
        &mut bound, // Pass the cost bound as a mutable reference
        &matrix, // Cost matrix
        &mut solutions, // Store solutions here
        &capitals, // City names
        optimize, // Whether to optimize for minimum cost
        &minimal_edges, // Precomputed minimal edges
    );

    // Output the results
    if optimize {
        // If in optimize mode, print the minimum cost
        println!("{}", bound);
    } else {
        // Otherwise, print all unique solutions
        let mut sorted_solutions: Vec<String> = solutions.into_iter().collect();
        sorted_solutions.sort(); // Sort solutions lexicographically
        for sol in sorted_solutions {
            println!("{}", sol);
        }
    }
}

// Parse the input text into capitals, cost matrix, and cost limit
fn parse_input(input: &str) -> (Vec<char>, Vec<Vec<u32>>, u32) {
    let mut lines = input.lines();

    // First line contains the number of cities and the cost limit
    let first_line = lines.next().unwrap();
    let parts: Vec<&str> = first_line.split_whitespace().collect();
    let _n: usize = parts[0].parse().unwrap(); // Number of cities (not used directly)
    let cost_limit: u32 = parts[1].parse().unwrap(); // Cost limit

    // Second line contains the capital letters representing the cities
    let capitals: Vec<char> = lines
        .next()
        .unwrap()
        .split_whitespace()
        .map(|s| s.chars().next().unwrap())
        .collect();

    // Remaining lines contain the cost matrix
    let matrix: Vec<Vec<u32>> = lines
        .map(|line| {
            line.split_whitespace()
                .map(|s| {
                    if s == "-" {
                        u32::MAX // Represent no-cost/self connections as maximum value
                    } else {
                        s.parse::<u32>().unwrap()
                    }
                })
                .collect()
        })
        .collect();

    (capitals, matrix, cost_limit)
}

// Compute the minimal non-zero edge cost for each city
fn compute_minimal_edges(matrix: &Vec<Vec<u32>>) -> Vec<u32> {
    let n = matrix.len();
    let mut minimal_edges = vec![u32::MAX; n];

    for i in 0..n {
        for j in 0..n {
            if i != j {
                minimal_edges[i] = minimal_edges[i].min(matrix[i][j]);
            }
        }
    }
    minimal_edges
}

// Estimate the minimal remaining cost to pair up unpaired cities
fn estimate_remaining_cost(unpaired: &Vec<usize>, minimal_edges: &Vec<u32>) -> u32 {
    let mut estimate = 0;
    for &city in unpaired {
        estimate += minimal_edges[city];
    }
    estimate / 2 // Divide by 2 because each edge involves two cities
}

// Depth-First Search with branch-and-bound optimization
fn dfs(
    unpaired: &mut Vec<usize>, // List of unpaired cities
    current_pairs: &mut Vec<(usize, usize)>, // Current pairs of cities
    current_cost: u32, // Current cost of the solution
    bound: &mut u32, // Cost bound for pruning
    cost_matrix: &Vec<Vec<u32>>, // Cost matrix
    solutions: &mut HashSet<String>, // Set of unique solutions
    city_names: &Vec<String>, // Names of the cities
    optimize: bool, // Whether to optimize for minimum cost
    minimal_edges: &Vec<u32>, // Precomputed minimal edges
) {
    // Base case: If all cities are paired
    if unpaired.is_empty() {
        if current_cost <= *bound {
            // Generate a string representation of the solution
            let mut pair_strings: Vec<String> = current_pairs.iter()
                .map(|&(i, j)| {
                    let (a, b) = if city_names[i] < city_names[j] {
                        (i, j)
                    } else {
                        (j, i)
                    };
                    format!("{}{}", city_names[a], city_names[b])
                })
                .collect();
            pair_strings.sort(); // Sort pairs lexicographically
            let result = pair_strings.join(" ");

            if optimize {
                // Update the bound if a better solution is found
                *bound = current_cost.min(*bound);
            } else {
                // Add the solution to the set of unique solutions
                solutions.insert(result);
            }
        }
        return;
    }

    // Prune branches that cannot lead to a better solution
    if optimize {
        let hopeful_cost = current_cost + estimate_remaining_cost(unpaired, minimal_edges);
        if hopeful_cost > *bound {
            return; // Stop exploring this branch
        }
    }

    // Try pairing the first unpaired city with every other unpaired city
    let first = unpaired[0];
    for i in 1..unpaired.len() {
        let second = unpaired[i];
        let pair_cost = cost_matrix[first][second];
        if pair_cost == u32::MAX {
            continue; // Skip invalid pairs
        }
        let new_cost = current_cost.saturating_add(pair_cost);
        if new_cost > *bound {
            continue; // Prune branches exceeding the bound
        }

        // Temporarily modify unpaired and current_pairs
        let second = unpaired.remove(i);
        let first = unpaired.remove(0);
        current_pairs.push((first, second));

        // Recurse with the updated state
        dfs(
            unpaired,
            current_pairs,
            new_cost,
            bound,
            cost_matrix,
            solutions,
            city_names,
            optimize,
            minimal_edges,
        );

        // Restore unpaired and current_pairs
        current_pairs.pop();
        unpaired.insert(0, first);
        unpaired.insert(i, second);
    }
}
