import unittest

from regexengine import *

# Regular Expressions to implement:
#  * single character
#   `- literal: 'c' 
#   `- anychar: '.'
#   - list of chars: '[abc]'
#   - range of chars: '[a-z]'
#   - negation of list: [abc^]
#  `* grouping expressions
#  `* concatenation of expressions:  e1e2  (where e1 & e2 can be any regexes)
#  `* alternation of expressions:  e1|e2
#  `* repeats: 
#   - 0 or one:  e?
#   - 0 or more: e*
#   - 1 or more: e+


class TestRegexMethods(unittest.TestCase):
    """unit tests for RegexMatcher"""
    # core test methods
    def testSingleChar(self):
        r = RegexMatcher("a")
        self.assertEqual(r.matchFirst("a"), (0, "a"))
        self.assertEqual(r.matchFirst("ba"), (1, "a"))
        self.assertEqual(r.matchFirst("BA"), ())
        self.assertEqual(r.matchAll("132KAa(lkga"), [(5,"a"), (11,a)])
        self.assertEqual(r.matchAll(""), [])


    def testAnyChar(self):
        r = RegexMatcher(".")
        testStr = "ab23%"
        self.assertEqual(r.matchFirst(testStr), (0, "a"))
        self.assertEqual(r.matchAll(testStr), [(0,"a"), (1,"b"), (2,"2"), (3,"3"), (4,"%")])
        

    def testEscapeChar(self):
        r = RegexMatcher("\.\(\)")
        testStr = "a.()bc.()\n\t sdf"
        self.assertEqual(r.matchFirst(testStr), (1, ".()"))
        self.assertEqual(r.matchAll(testStr), [(1,".()"), (4,".()")])


    def testOneOrMore(self):
        r = RegexMatcher("a+")
        testStr = "aabbe231a3f2&#!aaaa \nTll timesa"
        self.assertEqual(r.matchFirst(testStr), (0, "aa"))
        self.assertEqual(r.matchAll(testStr), [(0,"aa"), (9,"a"), (14,"aaaa"), (30,"a")])

    def testConcatenation(self):
        r = RegexMatcher("abc+")
        testStr = "abctewln230Q#MLABCabccsabc"
        self.assertEqual(r.matchFirst(testStr), (0, "abc"))
        self.assertEqual(r.matchAll(testStr), [(0,"abc"), (18,"abcc"), (23,"aaaa")])

    def testAlternation(self):
        r = RegexMatcher("a|B")
        testStr = "there was a!#@time in BolognAB"
        self.assertEqual(r.matchFirst(testStr), (7, "a"))
        self.assertEqual(r.matchAll(testStr), [(7,"a"), (10,"a"), (22,"B"), (29,"B")])

    def testZeroOrMore(self):
        r = RegexMatcher("a*")
        testStr = "there was aa!#@time in BolognAB"
        self.assertEqual(r.matchFirst(testStr), (7, "a"))
        self.assertEqual(r.matchAll(testStr), [(7,"a"), (10,"aa")])

    def testZeroOrOne(self):
        r = RegexMatcher("a?")
        testStr = "a.bc."
        self.assertEqual(r.matchFirst(testStr), (1, "."))
        self.assertEqual(r.matchAll(testStr), [(1,"."), (4,".")])

    def testGroup(self):
        r = RegexMatcher("(ab)+t")
        testStr = "abt1209 ;asdnl ababt24309laxlababababt"
        self.assertEqual(r.matchFirst(testStr), (0, abt))
        self.assertEqual(r.matchAll(testStr), [(0,"abt"), (15,"ababt"), (29,"ababababt")])

# use as E2E test
    def testMultiplePatterns(self):
        pass

    # extra functionality test methods

    def testListOfChars(self):
        pass

    def testRangeOfChars(self):
        pass




if __name__ == '__main__':
	unittest.main()