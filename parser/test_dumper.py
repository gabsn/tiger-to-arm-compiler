import unittest

from parser.dumper import Dumper
from parser.parser import parse

class TestDumper(unittest.TestCase):

    def parse_dump(self, text):
        tree = parse(text)
        return tree.accept(Dumper(semantics=False))

    def check(self, text, expected):
        self.assertEqual(self.parse_dump(text), expected)

######################## TESTS ###########################

    def test_literal(self):
        self.check("42", "42")

    def test_priority(self):
        self.check("1+2*3", "(1 + (2 * 3))")
        self.check("2*3+1", "((2 * 3) + 1)")

    def test_comments(self):
        self.check("42 // comment", "42")

    def test_ccomments(self):
        self.check("42 /* ccomment */", "42")

###################### FIN TESTS #######################

if __name__ == '__main__':
    unittest.main()
