
import pdb

class NFAState(object):

    def __init__(self, letter, finish=False):
        self.letter = letter
        self.finish = finish
        self.nexts = dict()

    def addNextState(self, state, letter=None):
        if not letter:
            letter = state.letter
        
        nextStates = self.nexts.get(letter)
        if nextStates: 
            # state already contains a transition for this letter
            nextStates.append(state)
        else:
            self.nexts[letter] = [state]

    def getNextStates(self):
        result = []
        for k in self.nexts.keys():
            result.extend(self.nexts[k])
        return set(result)

    def __str__(self):
        result = "letter: " + str(self.letter) + "\nfinish: " + str(self.finish) + "\nnexts: \n" + str(self.nexts)
        for k in self.nexts.keys():
            result += "\n" + str(k) + ":\n"
        return result

class NFAFrag():

    def __init__(self, enterState):
        self.enterStates = [enterState]
        self.exitStates = self.enterStates 
    
    # creates a transition from self's exitStates to all states in stateList
    # updates self's exitStates to stateList
    def appendToExitStates(self, stateList, letter=None):
        self._appendStates(self.exitStates, stateList, letter)

    #  creates transition from self's enter states to stateList
    def appendToEnterStates(self, stateList, letter=None):
        self._appendStates(self.enterStates, stateList, letter)

    # creates a transition from fromStates to toStates, if letter is specified, then it's used as
    # the transition character for all states
    def _appendStates(self, fromStates, toStates, letter=None):
        for fs in fromStates:
            for ts in toStates:
                fs.addNextState(ts, letter)

    # appends other to the exitStates of self, updating self's exitStates to be other's exitStates
    def appendFragment(self, other):
        self.appendToExitStates(other.enterStates)
        self.exitStates = other.exitStates
        return self

    # if self doesn't start with NC transition, then prepend an NC transition enterState to self
    # merge other's exitStates with self's and append other to self's enterStates
    def addSplitBranch(self, other):
        if not self.isInitialNoChar():
            ncStartState = [NFAState(NO_CHAR)]
            self._appendStates(ncStartState, self.enterStates)
            self.enterStates = ncStartState

        # merge exit states
        self.exitStates.extend(other.exitStates)

        self.appendToEnterStates(other.enterStates)

    def isInitialNoChar(self):
        return self.startsWithSingleChar(NO_CHAR)

    def isSplit(self):
        return self.startsWithSingleChar(ALTERNATE) and self.exitStates == self.enterStates 

    def isGroupStart(self):
        return self.startsWithSingleChar(GROUP_START)

    def startsWithSingleChar(self, c):
        return len(self.enterStates) == 1 and self.enterStates[0].letter == c

    def __str__(self):
        result = ""
        result += "Enter States: \n" + str(list(map(str, self.enterStates)))
        result += "\nExit States: \n" + str(list(map(str, self.exitStates)))

REGEX_OPS = {'*' , 
             '+' , 
             '?' , 
             '.' , 
             '|' ,
             '(' ,
             ')' }

# 
# represents a state that doesn't require an input to advance to it
NO_CHAR = chr(257)
# transition on any char '.'
ANY_CHAR = chr(258)
# 
# alternate between two patterns '|'
ALTERNATE = chr(259)
# '('
GROUP_START = chr(260)
# 
START_STATE = chr(261)

class NFA(object):
    """ represents a container object for a Nondeterministic Finite Automaton """
    def __init__(self, pattern):
        self.pattern = pattern
        self.currentStates = set()
        self.startState = self._parsePattern(pattern)
        self.reset()

# parses the regex pattern into an NFA and returns the first state of the NFA
    def _parsePattern(self, pattern):
        fragStack = []
        for c in pattern:
            if c not in REGEX_OPS:
                newFrag = NFAFrag(NFAState(c))
                
                fragStack.append(newFrag)
            else :
                if c == '+' or c == '*':
                    # add NO_CHAR transition from topFrag's exitStates to enterStates
                    newFrag = NFAFrag(NFAState(NO_CHAR))
                    topFrag = fragStack.pop()
                    newFrag.appendFragment(topFrag)
                    
                    newFrag.appendToExitStates(newFrag.enterStates, NO_CHAR)

                    # repeatedState.addNextState(repeatedState)
                    if c == '*':
                    # add a NO_CHAR transition to skip over entire fragment
                        newFrag.appendToEnterStates(newFrag.exitStates, NO_CHAR)

                    fragStack.append(newFrag)
                elif c == '?':
                    zeroOneFrag = fragStack.pop()
                    # add a NO_CHAR state to begining of zero-oned frag for auto-skip
                    zeroOneFragInit =  NFAFrag(NFAState(NO_CHAR))
                    zeroOneFragInit.appendFragment(zeroOneFrag)
                    zeroOneFrag = zeroOneFragInit

                    # link start states to end states via a NO_CHAR
                    zeroOneFrag.appendToEnterStates(zeroOneFrag.exitStates, NO_CHAR)
                    
                    fragStack.append(zeroOneFrag)
                elif c == '.':
                    # anycharState = NFAState(ANY_CHAR)
                    # stateStack.append(anycharState)
                    newFrag = NFAFrag(NFAState(ANY_CHAR))
                    fragStack.append(newFrag)
                elif c == '|': 
                    # on alternation, chain all preceding fragments together,
                    # push back on stack and push splitfrag on top
                    splitFrag = NFAFrag(NFAState(ALTERNATE))

                    altBranch = self._chainStackGroup(fragStack)
                    fragStack.append(altBranch)
                    
                    # put state chain back onto the stack & repeat the above steps
                    fragStack.append(splitFrag)
                elif c == '(':
                    # mark start of group on stack
                    groupStartFrag =  NFAFrag(NFAState(GROUP_START))
                    fragStack.append(groupStartFrag)

                elif c == ')':
                    # chain stack until the group start fragment is seen
                    group = self._chainStackGroup(fragStack)
                    fragStack.append(group)

        nfaFrag = self._chainStackGroup(fragStack)
        
        # pattern was a well-formed regular expression w/ matching parens
        if not fragStack:
            # set all end states to be finish states
            for s in nfaFrag.exitStates:
                s.finish = True

            # add a non-character first state
            firstState = NFAState(START_STATE)
            firstFrag = NFAFrag(firstState)
            firstFrag.appendFragment(nfaFrag)

            return firstState
        else:
            # notify library user that an error occurred in parsing pattern
            return None

# chains all fragments in fragStack into a single fragment until stack is empty or
# or a groupStart fragment has been seen
    def _chainStackGroup(self, fragStack):
        prevFrag = fragStack.pop()
        while fragStack:
            curFrag = fragStack.pop()

            if curFrag.isGroupStart():
                return prevFrag

            if curFrag.isSplit():
                # split branch is below the split frag operator
                curFrag = fragStack.pop()
                curFrag.addSplitBranch(prevFrag)

            else:
                curFrag.appendFragment(prevFrag)

            prevFrag = curFrag
        return prevFrag

# puts the NFA back to its start state
    def reset(self):
        self.currentStates = set([self.startState])

# advances to the next state(s) in the NFA
# returns true if advancement is successful otherwise false
    def advanceStates(self, letter):
        newStates = set()

        self.currentStates = self._autoAdvanceNoChars(self.currentStates)

        while self.currentStates:
            curState = self.currentStates.pop()
            if ANY_CHAR in curState.nexts:
                # any char state transition
                newStates.update(set(curState.nexts[ANY_CHAR]))
            elif letter in curState.nexts:
                newStates.update(set(curState.nexts[letter]))

        newStates = self._autoAdvanceNoChars(newStates)

        if newStates:
            self.currentStates = newStates
        return newStates != set()

    # auto-advance all no-char transitions in stateSet
    def _autoAdvanceNoChars(self, stateSet):
        prevLen = 0
        curLen = len(stateSet)
        while prevLen != curLen:
            addedStates = set()
            prevLen = curLen
            for s in stateSet:
                if NO_CHAR in s.nexts:
                    addedStates.update(set(s.nexts[NO_CHAR]))
            stateSet.update(addedStates)
            curLen = len(stateSet)
        return stateSet

# returns true if any of the current NFA states are finished states
    def finished(self):
        for n in self.currentStates:
            if n.finish:
                return True
        return False

    def __str__(self):
        result = "NFA: \n" + str(self.startState)
        seenStates = set()
        seenStates.add(self.startState)
        
        toExamine = []
        toExamine.extend(self.startState.getNextStates())
        
        prevLen = 0

        while len(seenStates) != prevLen:
            prevLen = len(seenStates)
            newToExamine = []
            for s in toExamine:
                if s not in seenStates:
                    result += "\n" + str(s)
                    seenStates.add(s)
                    newToExamine.extend(s.getNextStates().difference(seenStates))
            toExamine = newToExamine
        result += "\n\n Current States: \n" + str(list(map(str, self.currentStates)))
        return result
        

