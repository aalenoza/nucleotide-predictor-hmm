# Using Hidden Markov Models for Predicting Region of Coding DNA

## Table of Contents
1. [Introduction](#1-introduction)  
2. [Features](#2-features)  
3. [Setup and Installation](#3-setup-and-installation)  
4. [How to Use](#4-how-to-use)  
   - [Input Format](#input-format)  
   - [Output Format](#output-format)  
5. [Code Explanation](#5-code-explanation)  
   - [Functions Overview](#functions-overview)  
   - [Flow of Execution](#flow-of-execution)  
6. [Example Usage](#6-example-usage)
   - [Run the script](#run-the-script)   
7. [Known Issues and Limitations](#7-known-issues-and-limitations)  
8. [Credits](#8-credits)   

---

## 1. Introduction

This Python script implements a **Hidden Markov Model (HMM)** to predict regions of coding DNA based on a sequence of observable and hidden states. The program reads input from a file, processes sequences using HMM principles, and outputs computed probabilities for specified cases.

---

## 2. Features

- Parses input sequences and associated probabilities from a file.  
- Dynamically computes transition and observation probabilities.  
- Handles complex queries such as probabilities of hidden states given observable states.  
- Outputs results in a structured format.  

---

## 3. Setup and Installation

1. **Requirements:**
   - Python 3.8 or higher.
   - No external libraries required (uses Python's built-in re library for regular expression processing).


2. **Installation:**
   - Clone or download the repository containing this script.
   - Place the script (`hmm.py`) and input file (`hmm.in`) in the same directory.

---

## 4. How to Use

### Input Format
The input file (`hmm.in`) should follow this structure:

```
<number_of_sequences>
<sequence_1>
<sequence_2>
...
<sequence_n>
<list_of_hidden_states>  # Hidden states (e.g., A C G T)
<list_of_observables>  # Observables (e.g., H L)
<observable_state_probabilities>  # One line for each state (e.g., 0.6 0.9)
<number_of_cases>
<case_1>  # e.g., A1 given H1
<case_2>
...
<case_m>
```

Example:
```
1
GGCACTGAA
A C G T
H L
0.2 0.3
0.3 0.2
0.3 0.2
0.2 0.3
18
G1 given H1
G1 given L1
...
```
A sample input file (`sample.in`) is provided for reference.

### Output Format
The output file (`hmm.out`) will list results as follows:
```
<sequence_1>
<case_1> = <probability>
<case_2> = <probability>
...
<sequence_2>
...
```
A sample output file (`sample.out`) is provided for reference.

---

## 5. Code Explanation

### Functions Overview

- **`parse_hmm_input_from_file(file_name)`**  
  Parses the input file and extracts sequences, states, probabilities, and cases.

- **`compute_hidden_probabilities(states, letter, initial_probabilities, probability_dict, n)`**  
  Computes probabilities of hidden states for `n` steps.

- **`compute_observable_probabilities(states, letter, initial_probabilities, probability_dict, n)`**  
  Computes probabilities of observables based on hidden states for `n` steps.

- **`compute_hidden_given_observable_probability(...)`**  
  Calculates conditional probabilities of hidden states given observable states using Bayes' Rule.

- **`compute_hmm_probabilities(file_name, output_file_name)`**  
  Main function that orchestrates parsing input, computing probabilities, and writing results to the output file.

### Flow of Execution
1. Parse input data from the file.
2. Compute transition and observable probabilities for each sequence.
3. Process each case and compute the required probability.
4. Write the results to an output file.

---

## 6. Example Usage

**Input File (`hmm.in`):**
```
1
GGCACTGAA
A C G T
H L
0.2 0.3
0.3 0.2
0.3 0.2
0.2 0.3
18
G1 given H1
G1 given L1
...
```

#### **Run the Script:**
```
python hmm.py
```

**Output File (`hmm.out`):**
```
GGCACTGAA
G1 given H1 = 0.375
G1 given L1 = 0.2857142857142857
...
```

---

## 7. Known Issues and Limitations
- Assumes the input file is correctly formatted.
- Handles single-letter states and observables; multi-character identifiers may cause issues.
- Does not validate probability sums (e.g., transition probabilities should sum to 1).
 

