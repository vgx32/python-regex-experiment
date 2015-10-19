
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
    def __init__(self, initString):
        self.setPattern(initString)
        # pass

# generates the state machine for the regex specified by initString
    def setPattern(self, initString):
        self.initString = initString
        pass

# private method to create an NFA from the passed initString
    def _buildNFA(self, initString):
        pass

# returns a tuple of (int, str) that contains the integer of the index
# of the first char matching the pattern in input string and the str that
# matches the pattern
# if no match if found, returns a () empty tuple
    def matchFirst(self, inputStr):
        pass

# same as match_first, except returns a list of all (int, str)
# pairs that match the pattern sent to set_pattern
# if no matches returns []
    def matchAll(self, inputStr):
        pass

    def __str__(self):
        return self.initString