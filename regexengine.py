
from nfa import NFA

# Regular Expressions to implement:
#  * single character
#  	- literal: 'c'
#  	- anychar: '.'
#  	- list of chars: '[abc]'
#  	- range of chars: '[a-z]'
#  * concatenation of expressions:  e1e2  (where e1 & e2 can be any regexes)
#  * alternation of expressions:  e1|e2
#  * repeats: 
#  	- 0 or one:  e?
#  	- 0 or more: e*
#  	- 1 or more: e+


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

        
# returns a tuple of (int, str) that contains the integer of the index
# of the first char matching the pattern in input string and the str that
# matches the pattern
# if no match if found, returns a () empty tuple
    def matchFirst(self, inStr, searchStart=0):
        i = searchStart
        startIndex = i
        self.stateMachine.reset()
        while i < len(inStr):
            curChar = inStr[i]
            advanced = self.stateMachine.advanceStates(curChar)
            if self.stateMachine.finished():
                return (startIndex, inStr[startIndex : i+1])

            i += 1
            if not advanced:
                self.stateMachine.reset()
                startIndex = i
        return ()

# same as match_first, except returns a list of all (int, str)
# pairs that match the pattern sent to set_pattern
# if no matches returns []
    def matchAll(self, inStr):
        result = []
        prevMatch = self.matchFirst(inStr, 0)
        while prevMatch:
            result.append(prevMatch)
            startIndex, match = prevMatch
            iOfLastMatch = startIndex + len(match)
            # inStr = inStr[iOfLastMatch:]
            prevMatch = self.matchFirst(inStr, iOfLastMatch)
        return result

    def __str__(self):
        return self.pattern + "\n" + str(self.stateMachine)