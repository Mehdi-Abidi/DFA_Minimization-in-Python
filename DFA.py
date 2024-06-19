from graphviz import Digraph
from IPython.display import Image
from tabulate import tabulate

def visualize_dfa(states, alphabet, transitions, start_state, accepting_states):
    # Create a new Digraph object
    dot = Digraph()

    # Add states to the graph
    for state_group in states:
        state_str = ','.join(state_group)

    # Add transitions to the graph
    for (current_state, symbol), next_state in transitions.items():
        dot.edge(','.join(current_state), ','.join(next_state), label=symbol)

    # Highlight accepting states
    for state_group in accepting_states:
        dot.node(','.join(state_group), shape='doublecircle')

    # Add arrow to the start state
    if start_state:
        start_state_str = ','.join(start_state)
        dot.node('start', shape='none')
        dot.edge('start', start_state_str, label='', style='dashed')  # Arrow to start state

    try:
        # Save the graph to a file
        dot.render(filename='minimized_dfa', format='png', cleanup=True)
        display(Image(filename='minimized_dfa.png'))
    except Exception as e:
        print("Error occurred during rendering:", e)



def minimize_dfa(states, alphabet, transitions, start_state, accepting_states):
    # Perform reachability analysis
    reachable_states = set()    
    stack = [start_state]
    while stack:
        current_state = stack.pop()
        reachable_states.add(current_state)
        for symbol in alphabet:
            next_state = transitions.get((current_state, symbol))
            if next_state and next_state not in reachable_states:
                stack.append(next_state)

    print(f"Reachable states: {reachable_states}")  # Print reachable states

    # Initialize two sets of states: non-accepting and accepting states
    P0 = reachable_states - set(accepting_states)
    P1 = set(accepting_states)

    # Create the initial partition P
    P = [P0, P1]

    while True:
        P_prime = P.copy()

        for S in P_prime:
            partition_map = {}
            for state in S:
                state_group = []
                for symbol in alphabet:
                    next_state = transitions.get((state, symbol))
                    if next_state:
                        for i, p in enumerate(P):
                            if next_state in p:
                                state_group.append(i)
                                break
                state_group = tuple(sorted(state_group))
                if state_group not in partition_map:
                    partition_map[state_group] = set()
                partition_map[state_group].add(state)

            new_partitions = list(partition_map.values())
            if len(new_partitions) > 1:
                print("Current Partitions:", P)  # Debug print
                print("New Partitions:", new_partitions)  # Debug print
                P.remove(S)
                P.extend(new_partitions)

        if P == P_prime:
            break

    minimized_states = [sorted(list(part)) for part in P]

    # Update the determination of the minimized start state
    minimized_start_state = next(iter([part for part in minimized_states if start_state in part]))

    minimized_transitions = {}
    for part in P:
        representative = next(iter(part))
        for symbol in alphabet:
            next_state = transitions.get((representative, symbol))
            for group in P:
                if next_state in group:
                    minimized_transitions[(tuple(part), symbol)] = group
                    break

    minimized_accepting_states = [part for part in P if part.intersection(accepting_states)]

    # Call the visualization function here
    visualize_dfa(minimized_states, alphabet, minimized_transitions, minimized_start_state, minimized_accepting_states)

    return minimized_states, minimized_transitions, minimized_start_state, minimized_accepting_states


# Take user input for DFA details
states = input("Enter states (comma-separated): ").strip().split(',')
alphabet = input("Enter alphabet symbols (comma-separated): ").strip().split(',')
transitions = {}
for state in states:
    for symbol in alphabet:
        next_state = input(f"Enter transition for ({state}, {symbol}): ").strip()
        transitions[(state, symbol)] = next_state

start_state = input("Enter start state: ").strip()
accepting_states = input("Enter accepting states (comma-separated): ").strip().split(',')
table_data = []
print("Original Dfa: ")
# Add headers
headers = ["States"] + ["Input Symbol: {}".format(symbol) for symbol in alphabet]
#table_data.append(headers)

# Add transitions for each state
for state in states:
    row = [state]
    for symbol in alphabet:
        next_state = transitions.get((state, symbol), "-")  # Default to '-' if transition doesn't exist
        row.append(next_state)
    table_data.append(row)

# Print the transitions table using tabulate in GitHub format
print(tabulate(table_data, headers=headers, tablefmt="github"))
# Call the DFA minimization function with your input
minimized_states, minimized_transitions, minimized_start_state, minimized_accepting_states = minimize_dfa(states, alphabet, transitions, start_state, accepting_states)

# Print the minimized states
print("Minimized States:")
for state_group in minimized_states:
    print(state_group)

# Print the minimized transitions
print("\nMinimized Transitions:")
for (current_state, symbol), next_state in minimized_transitions.items():
    print(f"{current_state} --({symbol})--> {next_state}")

# Print the minimized start state
print("\nMinimized Start State:")
print(minimized_start_state)
