import sys


# collect nfa inputs
if len(sys.argv) == 2:
    if sys.argv[1].split('.')[-1] == 'nfa':
        # input file specified
        
        outputFilename = sys.argv[1].split('.')[0] + '.fa'
        
        infile = open(sys.argv[1], 'r')
        source = infile.read().splitlines()

        nfaStarts = list(set(source[0].split(', ')))
        nfaStarts[0] = nfaStarts[0][1:]
        nfaStarts[-1] = nfaStarts[-1][:-1]
        nfaStarts.sort()
        
        nfaAccepts = list(set(source[1].split(', ')))
        nfaAccepts[0] = nfaAccepts[0][1:]
        nfaAccepts[-1] = nfaAccepts[-1][:-1]
        nfaAccepts.sort()

        transitionTable = {}

        nfaStates = set()
        alphabet = set()

        for line in source[2:]:
            if line:
                triple = line.split()

                nfaStates.add(triple[0])
                alphabet.add(triple[1])
                nfaStates.add(triple[2])

                if triple[0] not in transitionTable.keys():
                    transitionTable[triple[0]] = {}

                transitionTable[triple[0]][triple[1]] = triple[2:]
                transitionTable[triple[0]][triple[1]].sort()
        
        alphabet = list(alphabet)
        alphabet.sort()

        nfaStates = list(nfaStates)
        nfaStates.sort()            

        for state in nfaAccepts or nfaStarts:
            if state not in transitionTable.keys():
                    transitionTable[state] = {}
                    
                    for symbol in alphabet:
                        transitionTable[state][symbol] = []
    elif len(sys.argv[1].split('.')) == 1:
        # cmd line specified
        outputFilename = sys.argv[1] + '.fa'

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
    else:
        exit('invoke this program with a .nfa file, or an output name')
else:
    exit("too many arguments")


# initialize translation supports
stateCounter = 1
nfaQueue = []
nfaProcessed = []
nfa_dfa = {}

transitionString = ""

class node:
    def __init__(self, nfaStates):
        global stateCounter
        self.dfaState = stateCounter
        stateCounter += 1
        
        self.nfaStates = nfaStates

startNode = node(nfaStarts)
nfaQueue.append(startNode)


# work through nfa, creating dfa
while (nfaQueue):
    currentNode = nfaQueue.pop(0)
    nfa_dfa[str(currentNode.nfaStates)] = currentNode.dfaState
    
    for symbol in alphabet:
        nextStates = set()
        
        for state in currentNode.nfaStates:

            for i in transitionTable[state][symbol]:
                nextStates.add(i)

        nextStates = list(nextStates)
        nextStates.sort()
        
        if (str(nextStates) not in nfa_dfa.keys()):
            tempNode = node(nextStates)
            nfaQueue.append(tempNode)

            nfa_dfa[str(tempNode.nfaStates)] = tempNode.dfaState
        
        transitionString += str(currentNode.dfaState) + ' ' + str(symbol) + ' ' + str(nfa_dfa[str(nextStates)]) + '\n'
        
    transitionString += '\n'


# write start state, accept states, and transitions
f = open(outputFilename, "w")

f.write(str(nfa_dfa[str(nfaStarts)]))

acceptsString = '\n{'
for a in nfaAccepts:
    for set in nfa_dfa.keys():
        if a in list(set):
            acceptsString += str(nfa_dfa[set]) + ", "
acceptsString = acceptsString[:-2] + '}\n\n' 
f.write(acceptsString)

f.write(transitionString[:-2])

f.close()