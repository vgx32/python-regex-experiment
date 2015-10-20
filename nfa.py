

class NFAState(object):
    """ a single state in a Nondeterministic finite state automaton"""
    def __init__(self, letter, finish=False):
        self.letter = letter
        self.finish = finish
        self.nexts = dict()

    def addNextState(self, state, letter=None):
        if not letter:
            letter = state.letter
        for l in state.letter:
            # print(l)
            nextState = self.nexts.get(l)
            if nextState:
                nextState.append(state)
            else:
                self.nexts[l] = [state]

    def __str__(self):
        result = "letter: " + str(self.letter) + "\nfinish: " + str(self.finish) + "\nnexts: \n" + str(self.nexts)
        for k in self.nexts.keys():
            result += "\n" + str(k) + ":\n"
            for state in self.nexts[k]:
                result += str(state)
        return result

REGEX_OPS = {'\\': "escape", 
             '*' : "zeromore", 
             '+' : "onemore", 
             '?' : "zeroone", 
             '.' : "anychar", 
             '|' : "alternate"}

# represents a state that doesn't require an input to advance to it
NO_CHAR = chr(257)

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
                if c == '+' or c == '*':
                    # add transition via previous state's letter back to itself
                    repeatedState = stateStack.pop()
                    repeatedState.addNextState(repeatedState)
                    if c == '*': 
                        # transitioning to this state shouldn't require input
                        repeatedState.letter = NO_CHAR
                    stateStack.append(repeatedState)
                elif c == '|':
                    # all current states in stack are a valid path; set finish=True
                    # on the top state & chain all states in stack together
                    split = NFAState(NO_CHAR)

                    altBranch = self._chainStateStack(stateStack)
                    split.addNextState(altBranch)
                    # put state chain back onto the stack & repeat the above steps
                    stateStack.append(split)
                elif c == '?':
                    zerooneState = stateStack.pop()
                    zerooneState.letter = NO_CHAR + zerooneState.letter
                    # print(zerooneState)
                    stateStack.append(zerooneState)

        firstCharState = self._chainStateStack(stateStack)
        
# add a non-character first state
        firstState = NFAState(chr(0))
        firstState.addNextState(firstCharState)
        return firstState

# links all states in the passed stateStack parameter (top of stack being the last state
# and bottom of stack being the first state in the chain) returns the first state in the chain
    def _chainStateStack(self, stateStack):
        prevState = stateStack.pop()
        prevState.finish = True 
        while stateStack:
            curState = stateStack.pop()
         
            curState.addNextState(prevState)

            prevState = curState

        return prevState


# puts the NFA back to its start state
    def reset(self):
        if self.currentStates != [self.startState]:
            self.currentStates = [self.startState]

# advances to the next state(s) in the NFA
# returns true if advancement is successful otherwise false
    def advanceStates(self, letter):
        newStates = []
        while self.currentStates:
            sa = self.currentStates.pop()
            if sa.nexts.keys() and NO_CHAR in sa.nexts and letter not in sa.nexts:
                # auto-advance to next state by adding all possible next 
                # states from the split to list currentStates to be processed
                self.currentStates.extend(sa.nexts[NO_CHAR])
            elif letter in sa.nexts:
                newStates.extend(sa.nexts[letter])

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
        

