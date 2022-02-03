# collect nfa inputs
alphabet = input('enter alphabet, space separated\n').split()
alphabet.sort()

nfaStates = input('enter states, space separated\n').split()
nfaStates.sort()

nfaStarts = input('enter start states, space separated\n').split()
nfaStarts.sort()

nfaAccepts = input('enter accept states, space separated\n').split()
nfaAccepts.sort()

transitionTable = {}

print()

print('provide a space separated list of next state, given current state and input symbol')
for state in nfaStates:
    transitionTable[state] = {}
    for symbol in alphabet:
        transitionTable[state][symbol] = input('%s %s -> ' % (state, symbol)).split()

print()


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
f = open("dfa.fa", "w")
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