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
    def test1SingleChar(self):
        r = RegexMatcher("a")
        self.assertEqual(r.matchFirst("a"), (0, "a"))
        self.assertEqual(r.matchFirst("ba"), (1, "a"))
        self.assertEqual(r.matchFirst("BA"), ())
        self.assertEqual(r.matchAll("132KAa(lkga"), [(5,"a"), (10,"a")])
        self.assertEqual(r.matchAll(""), [])

    def test2_Concatenation1_basic(self):
        r = RegexMatcher("abc")
        testStr = "abctewln230Q#MLABCabccsabc"
        self.assertEqual(r.matchFirst(testStr), (0, "abc"))
        self.assertEqual(r.matchAll(testStr), [(0,"abc"), (18,"abc"), (23,"abc")])

    def test2_Concatenation2_advanced(self):
    
        r = RegexMatcher("abc+")
        testStr = "abctewln230Q#MLABCabccsabc"
        self.assertEqual(r.matchFirst(testStr), (0, "abc"))
        self.assertEqual(r.matchAll(testStr), [(0,"abc"), (18,"abcc"), (23,"abc")])
        

    def test4OneOrMore(self):
        r = RegexMatcher("a+")
        testStr = "aabbe231a3f2&#!aaaa \nTll timesa"
        self.assertEqual(r.matchFirst(testStr), (0, "aa"))
        self.assertEqual(r.matchAll(testStr), [(0,"aa"), (8,"a"), (15,"aaaa"), (30,"a")])

    def test4OneOrMore_advanced(self):
        r = RegexMatcher("a+b")
        testStr = "aaabbe231a3f2&#!aaaa \nTll timeaabsab"
        self.assertEqual(r.matchFirst(testStr), (0, "aaab"))
        self.assertEqual(r.matchAll(testStr), [(0,"aaab"), (30,"aab"), (34,"ab")])

    
    def test6Alternation(self):
        r = RegexMatcher("a|B")
        testStr = "there was a!#@time in BolognAB"
        self.assertEqual(r.matchFirst(testStr), (7, "a"))
        self.assertEqual(r.matchAll(testStr), [(7,"a"), (10,"a"), (22,"B"), (29,"B")])

    def test7ZeroOrMore(self):
        r = RegexMatcher("a*")
        testStr = "there was aa!#@time in BolognAB"
        self.assertEqual(r.matchFirst(testStr), (7, "a"))
        self.assertEqual(r.matchAll(testStr), [(7,"a"), (10,"aa")])

    def test8ZeroOrOne(self):
        r = RegexMatcher("a?")
        testStr = "a.bc."
        self.assertEqual(r.matchFirst(testStr), (1, "."))
        self.assertEqual(r.matchAll(testStr), [(1,"."), (4,".")])

    def test9Group(self):
        r = RegexMatcher("(ab)+t")
        testStr = "abt1209 ;asdnl ababt24309laxlababababt"
        self.assertEqual(r.matchFirst(testStr), (0, abt))
        self.assertEqual(r.matchAll(testStr), [(0,"abt"), (15,"ababt"), (29,"ababababt")])


    def testaAnyChar(self):
        r = RegexMatcher(".")
        testStr = "ab23%"
        self.assertEqual(r.matchFirst(testStr), (0, "a"))
        self.assertEqual(r.matchAll(testStr), [(0,"a"), (1,"b"), (2,"2"), (3,"3"), (4,"%")])
        

    def testaEscapeChar(self):
        r = RegexMatcher("\.\(\)")
        testStr = "a.()bc.()\n\t sdf"
        self.assertEqual(r.matchFirst(testStr), (1, ".()"))
        self.assertEqual(r.matchAll(testStr), [(1,".()"), (4,".()")])


# use as E2E test
    def test10MultiplePatterns(self):
        pass

    # extra functionality test methods

    def test11ListOfChars(self):
        pass

    def test12RangeOfChars(self):
        pass




if __name__ == '__main__':
	unittest.main(failfast=True)