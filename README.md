# nfa-to-dfa

This tool converts a Nondeterministic Finite Automata (NFA) into a Deterministic Finite Automata (DFA)

## Using convert.py
You may provide an input NFA in one of two ways.

1. Define the NFA via a CLI
   - When invoking the program, provide a name for the output file
      - ```> python3 convert.py <outputName>```
   - After walking you through the NFA definition, it will create a DFA in the form of <outputName>.fa

2. Define the NFA via an input file
   - When invoking the program, provide an input file of type .nfa
      - ```> python3 convert.py <inputName>.nfa```
   - This will create a DFA in the form of <inputName>.fa
   
## Formatting a .nfa file

The input .nfa should be formatted as follows:
1. The first line holds a set of states the NFA could initially be on, enclosed in curly braces, delimted by commas
2. The second line holds a set of states that the NFA will accept, enclosed in curly braces, delimted by commas
3. The following lines will define the state transitions, as a tuple, for each state you wish to define.
    - The first symbol is the current state.
    - The second symbol will be the transition symbol.
    - The following symbol (or symbols, delimted by space) will define the set of all states the automata will transition into.

###### example.nfa
```
{1}
{1, 3}

1 a 2 3
1 b 1

2 a 3
2 b 1

3 a 3
3 b 3
```
