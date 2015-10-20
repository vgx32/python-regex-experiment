

class NFAState(object):
    """ a single state in a Nondeterministic finite state automaton"""
    def __init__(self, letter, finish=False):
        self.letter = letter
        self.finish = finish
        self.nexts = dict()

    def addNextState(self, state):
        nextState = self.nexts.get(state.letter)
        if nextState:
            nextState.append(state)
        else:
            self.nexts[state.letter] = [state]

    def __str__(self):
        result = "letter " + str(self.letter) + "\nfinish: " + str(self.finish) + "\nnexts: \n" + str(self.nexts)
        for k in self.nexts.keys():
            result += "\n" + str(k) + ":\n"
            for state in self.nexts[k]:
                result += str(state)
        return result

REGEX_OPS = {'\\': "escape", 
             '*' : "zeromore", 
             '+' : "onemore", 
             '?' : "zeroone", 
             '.' : "dot", 
             '|' : "or"}

class NFA(object):
    """ represents a container object for a Nondeterministic Finite Automaton """
    def __init__(self, pattern):
        self.pattern = pattern
        self.currentStates = []
        self.startState = self._parsePattern(pattern)
        self.reset()

# parses the regex pattern into an NFA and returns the first state of the NFA
    def _parsePattern(self, pattern):
        stateStack = []
        for c in pattern:
            if c not in REGEX_OPS:
                n = NFAState(c)
                stateStack.append(n)
            else :
                if c == '+':
                    repeatedState = stateStack.pop()
                    repeatedState.addNextState(repeatedState)
                    stateStack.append(repeatedState)
                # elif c == '.':
                    
            

        prevState = stateStack.pop()
        prevState.finish = True 
        while stateStack:
            curState = stateStack.pop()
            curState.addNextState(prevState)
            prevState = curState

# add a non-character first state
        firstState = NFAState(chr(0))
        firstState.addNextState(prevState)
        return firstState

# puts the NFA back to its first state
    def reset(self):
        if self.currentStates != [self.startState]:
            self.currentStates = [self.startState]

# advances to the next state(s) in the NFA
# returns true if advancement is successful otherwise false
    def advanceStates(self, letter):
        newStates = []
        for s in self.currentStates:
            if letter in s.nexts:
                newStates.extend(s.nexts[letter])
        if newStates:
            self.currentStates = newStates
        return newStates != []


# returns true if any of the current NFA states are finished states
    def finished(self):
        for n in self.currentStates:
            if n.finish:
                return True
        return False

    def __str__(self):
        return "NFA: \n" + str(self.startState) + "\n\nCurrent States: " + str(self.currentStates)
        

