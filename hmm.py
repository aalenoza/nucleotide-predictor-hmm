import re  # import regular expressions for pattern matching and searching in sequences

def parse_hmm_input_from_file(file_name):
    # open the file 'hmm.in' and read its content
    with open(file_name, "r") as file:
        # read all lines in the file, strip leading/trailing whitespace, and split into a list of lines
        lines = file.read().strip().split("\n")
    
    # extract the number of sequences from the first line
    num_sequences = int(lines[0])
    
    # extract the sequence(s) from the subsequent lines
    sequences = lines[1:num_sequences + 1]
    
    # extract the states (possible hidden states) from the next line
    states = lines[num_sequences + 1].split()
    
    # extract the observable states from the next line
    observables = lines[num_sequences + 2].split()
    
    # extract the transition probabilities for each state from the following lines
    num_states = len(states)
    observable_values = []  # initialize a list to store the observable probabilities
    for i in range(num_states):
        # map each observable probability to a float and store in observable_values
        observable_values.append(list(map(float, lines[num_sequences + 3 + i].split())))
    
    # extract the number of cases from the line after the observable values
    num_cases = int(lines[num_sequences + 3 + num_states])
    
    # extract the cases (e.g., A1 given H1) from the remaining lines
    cases = lines[num_sequences + 3 + num_states + 1:num_sequences + 3 + num_states + 1 + num_cases]
    
    # return all extracted data as a dictionary
    return {
        "sequences": sequences,
        "states": states,
        "observables": observables,
        "observable_values": observable_values,
        "cases": cases,
    }

def compute_hidden_probabilities(states, letter, initial_probabilities, probability_dict, n):
    # iteratively compute probabilities for n steps
    for _ in range(n):
        # create a temporary dictionary to store the updated probabilities for this step
        updated_probabilities = {state: 0 for state in states}

        # iterate through each state to compute the updated probabilities
        for current_state in states:
            # calculate the probability sum for the current state
            probability_sum = sum(
                probability_dict[current_state][other_state] * initial_probabilities[other_state]
                for other_state in states  # sum over all possible previous states
            )
            # store the computed probability for the current state
            updated_probabilities[current_state] = probability_sum

        # update the initial_probabilities with the new computed values
        initial_probabilities = updated_probabilities
    
    # return the computed probability for the specific letter (state)
    return initial_probabilities[letter]
        
    
def compute_observable_probabilities(states, letter, initial_probabilities, probability_dict, n):
    # compute the observable probability for a given letter (observable) and n steps
    return sum(
        probability_dict[letter][state] * compute_hidden_probabilities(states, state, initial_probabilities, probability_dict, n)
        for state in states  # sum over all possible hidden states
    )

def compute_hidden_given_observable_probability(states, hidden_letter, observable_letter, hidden_n, observable_n, initial_probabilities, probability_dict):
    # compute the probability of a hidden state given an observable state
    observable_prob = compute_observable_probabilities(states, observable_letter, initial_probabilities, probability_dict, observable_n)
    hidden_prob = compute_hidden_probabilities(states, hidden_letter, initial_probabilities, probability_dict, hidden_n)
    # calculate the conditional probability of the hidden state given the observable
    return (probability_dict[observable_letter][hidden_letter] * hidden_prob) / observable_prob    

def compute_hmm_probabilities(file_name, output_file_name):
    # parse input data from the file using the parsing function
    sequences, states, observables, observable_values, cases = parse_hmm_input_from_file(file_name).values()
    
    # prepare observable probabilities as a dictionary, mapping each observable to a dictionary of state probabilities
    observable_probabilities = {observable: dict(zip(states, values)) for observable, values in zip(observables, zip(*observable_values))}

    # open the output file for writing the results
    with open(output_file_name, "w") as file:
        for sequence in sequences:
            # write the sequence to the file followed by a newline
            file.write(sequence + "\n")
            
            # initialize initial probabilities with all states set to 0
            initial_probabilities = {state: 0 for state in states}
            # set the probability of the first state in the sequence to 1 (starting point)
            initial_probabilities[sequence[0]] = 1

            # calculate transition probabilities for each state based on the sequence
            transition_probabilities = {
                next_state: {
                    current_state: (
                        # calculate the transition probability between states
                        len(re.findall(f"(?=({current_state}{next_state}))", sequence)) / count_current
                        if (count_current := len(re.findall(f"(?=({current_state}.))", sequence))) > 0
                        else 0  # avoid division by zero if current state does not occur
                    )
                    for current_state in states  # compute transition probabilities for each current state
                }
                for next_state in states  # compute for each next state
            }
            
            # combine transition probabilities and observable probabilities into one dictionary
            combined_probabilities = {**transition_probabilities, **observable_probabilities}

            # process each case (e.g., "A999 given H999") and compute the required probabilities
            for case in cases:
                # parse the hidden and observable letters and their respective indices
                hidden_letter, hidden_n, observable_letter, observable_n = re.match(r"([A-Z])(\d+) given ([A-Z])(\d+)", case).groups()
                hidden_n, observable_n = int(hidden_n), int(observable_n)
                
                # compute the probability for the current case using the hidden and observable letters and indices
                result = compute_hidden_given_observable_probability(
                    states,
                    hidden_letter,
                    observable_letter,
                    hidden_n,
                    observable_n,
                    initial_probabilities,
                    combined_probabilities,
                )
                # write the result for the current case to the file
                file.write(f"{case} = {result}\n")
            
            # add an extra newline after each sequence, except the last one
            file.write("" if sequence == sequences[-1] else "\n")


# input file and output file
compute_hmm_probabilities("hmm.in", "hmm.out")  # run the HMM computation with input and output file names
