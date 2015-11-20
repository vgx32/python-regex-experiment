
from nfa import NFA
import pdb
# Regular Expressions to implement:
#  * single character
#  	- literal: 'c'
#  	- anychar: '.'
#  * concatenation of expressions:  e1e2  (where e1 & e2 can be any regexes)
#  * alternation of expressions:  e1|e2
#  * repeats: 
#  	- 0 or one:  e?
#  	- 0 or more: e*
#  	- 1 or more: e+
#  * grouping (23|1)+


class RegexMatcher(object):
    """ A basic regex parser for ascii characters -- initialize with a
        pattern passed to either the class constructor or set_pattern
        
        Use match* functions to find matches in input strings
    """
    def __init__(self, pattern):
        self.setPattern(pattern)
        # pass

# generates the state machine for the regex specified by pattern
    def setPattern(self, pattern):
        self.pattern = pattern
        self.stateMachine = NFA(pattern)

    def findLongestMatch(self, inStr, i):
        self.stateMachine.reset()
        j = i
        prevFinishedIndex = -1
        while j < len(inStr) and self.stateMachine.advanceStates(inStr[j]):
            j += 1
            if self.stateMachine.finished():
                prevFinishedIndex = j

        if prevFinishedIndex != -1:
            return inStr[i:prevFinishedIndex]
        else:
            return ""

# returns a tuple of (int, str) that contains the integer of the index
# of the first char matching the pattern in input string and the str that
# matches the pattern
# if no match if found, returns a () empty tuple
    def matchFirst(self, inStr, searchStart=0):
        self.stateMachine.reset()
        for i in range(searchStart, len(inStr)):
            match = self.findLongestMatch(inStr, i)
            if match:
                return (i, match)
            
        return ()

# same as matchFirst, except returns a list of all (int, str)
# pairs that match the pattern sent to set_pattern
# if no matches returns []
    def matchAll(self, inStr):
        result = []
        prevMatch = self.matchFirst(inStr, 0)
        while prevMatch:
            result.append(prevMatch)
            startIndex, match = prevMatch
            iOfLastMatch = startIndex + len(match)
            prevMatch = self.matchFirst(inStr, iOfLastMatch)

        return result

    def __str__(self):
        return self.pattern + "\n" + str(self.stateMachine)