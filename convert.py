import sys
import re
from tracemalloc import start

print('''\n
             .-.                               ___    .-.              
            /    \                            (   )  /    \            
 ___ .-.    | .`. ;    .---.                .-.| |   | .`. ;    .---.  
(   )   \   | |(___)  / .-, \              /   \ |   | |(___)  / .-, \ 
 |  .-. .   | |_     (__) ; |   .------.  |  .-. |   | |_     (__) ; | 
 | |  | |  (   __)     .'`  |  (________) | |  | |  (   __)     .'`  | 
 | |  | |   | |       / .'| |             | |  | |   | |       / .'| | 
 | |  | |   | |      | /  | |             | |  | |   | |      | /  | | 
 | |  | |   | |      ; |  ; |             | '  | |   | |      ; |  ; | 
 | |  | |   | |      ' `-'  |             ' `-'  /   | |      ' `-'  | 
(___)(___) (___)     `.__.'_.              `.__,'   (___)     `.__.'_.                                                                                                                             
''')

# collect nfa inputs
if sys.argv[1] == '-h' or sys.argv[1] == '--help':
    #help flag
    exit("Usage:\n\t python3 convert.py <Filename>.nfa: Read from .nfa file\n\t python3 convert.py: Custom input\n")
elif len(sys.argv) == 1:
    #CLI Custom Input
    outputFilename = sys.argv[0] + '.fa'
    alphabet = input('enter alphabet, space separated\n').split()
    alphabet.sort()
    nfaStates = input('enter states, space separated\n').split()
    nfaStates.sort()
    nfaStarts = input('enter start states, space separated\n').split()
    nfaStarts.sort()
    nfaAccepts = input('enter accept states, space separated\n').split()
    nfaAccepts.sort()
    transitionTable = {}
    print('provide a space separated list of next state, given current state and input symbol')
    for state in nfaStates:
        transitionTable[state] = {}
        for symbol in alphabet:
            transitionTable[state][symbol] = input('%s %s -> ' % (state, symbol)).split()
elif len(sys.argv) == 2:
     # verify input file specified and continue
    if sys.argv[1].split('.')[-1] == 'nfa':
        outputFilename = sys.argv[1].split('.')[0] + '.fa'
        infile = open(sys.argv[1], 'r')
        source = infile.read().splitlines()

        #parse starting node
        nfaStarts = list(set(source[0].split(', ')))
        nfaStarts[0] = nfaStarts[0][1:]
        nfaStarts[-1] = nfaStarts[-1][:-1]
        print("Starting node: " + str(nfaStarts))

        #parse accept node(s)
        nfaAccepts = list(set(source[1].split(', ')))
        nfaAccepts[0] = nfaAccepts[0][1:]
        nfaAccepts[-1] = nfaAccepts[-1][:-1]
        nfaAccepts.sort()
        print("Accept node(s): " + str(nfaAccepts))

        #define behavior and sets for NFA
        transitionTable = {}
        nfaStates = set()
        alphabet = set()

        for line in source[2:]:
            if line:
                statement = line.split()
                state1 = statement[0]
                transition = statement[1]
                states = statement[2:]

                # <state> {transition} <state>
                nfaStates.add(state1)
                alphabet.add(transition)
                for state in states:
                    nfaStates.add(state)

                #if state is not in table, add it.
                if state1 not in transitionTable.keys():
                    transitionTable[state1] = {}
                for edge in states:
                    if edge not in transitionTable.keys():
                        transitionTable[edge] = {}
                    
                #add state transition(s) and sort set
                transitionTable[state1][transition] = states
                transitionTable[state1][transition].sort()
        
        #format and print values
        alphabet = list(alphabet)
        alphabet.sort()
        nfaStates = list(nfaStates)
        nfaStates.sort()            
        print("Found states: " + str(nfaStates))
        print("Found alphabet: " + str(alphabet))
        print("Transition Table: " + str(transitionTable))
    else:
        exit('invoke this program with a .nfa file, or an output name')

else:
    exit("too many arguments")

# initialize translation supports
stateCounter = 1
nfaQueue = []
nfaProcessed = [] #use this
converted_set = {}
transitionString = ""
class node:
    def __init__(self, nfaStates):
        global stateCounter
        self.dfaState = stateCounter
        stateCounter += 1
        self.nfaStates = nfaStates

#initalize queue 
startNode = node(nfaStarts)
nfaQueue.append(startNode)

print("Transition keys: " + str(transitionTable[state].keys()))
# work through nfa, creating dfa
#THE JUICE
while (nfaQueue):
    #print("STATE COUNTER: " + str(stateCounter))
    currentNode = nfaQueue.pop(0)
    converted_set[str(currentNode.nfaStates)] = currentNode.dfaState
    
    #for every set state, go through alphabet. Branch and bound??
    for symbol in alphabet:
        nextStates = set()

        #for every nfa neighbor, check to see if symbol goes to it. 
        for state in currentNode.nfaStates:
            if symbol in transitionTable[state].keys():
                for transition in transitionTable[state][symbol]:
                    nextStates.add(transition)
        nextStates = list(nextStates)
        nextStates.sort()
    
        if (str(nextStates) not in str(converted_set.keys()) and nextStates not in nfaProcessed):
            #print("CONVERSION SET: " + str(converted_set))
            #print("CONVERSION SET KEYS: " + str(converted_set.keys()))
            #print("NEXT NODES SET: " + str(nextStates) + "\n")
            tempNode = node(nextStates)
            nfaQueue.append(tempNode)
            nfaProcessed.append(tempNode)
            converted_set[str(tempNode.nfaStates)] = tempNode.dfaState
        transitionString += str(currentNode.dfaState) + " " + str(symbol) + " " + str(converted_set[str(nextStates)]) + '\n'    
    transitionString += '\n'
    
#check iterated nodes to determine if it contains an accepted set
#TODO add 'contains_accepted' as node attribute so we can skip this other loop
dfaAccepts = []
acceptStrings = re.findall('[0-9]+', str(nfaAccepts))
for group in nfaProcessed:
   for valid in acceptStrings:
       if valid in re.findall('[0-9]+', str(group.nfaStates)):
           dfaAccepts.append(group.dfaState)
dfaAccepts.sort()

print("\nMachine output: \n" + transitionString)
# write start state, accept states, and transitions
f = open(outputFilename, "w")
f.write(str(converted_set[str(nfaStarts)]))
acceptsString = '\n{ '
for state in dfaAccepts:
    acceptsString = acceptsString + str(state) + " "
acceptsString = acceptsString + "}\n\n"
f.write(acceptsString)
f.write(transitionString)
f.close()
print(str(sys.argv[1].split('.')[0]) + ".fa has been writen." )