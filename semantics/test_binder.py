import unittest

from parser.dumper import Dumper
from parser.parser import parse
from semantics.binder import Binder

class TestBinder(unittest.TestCase):
    
    def parse_bind(self, text):
        tree = parse(text)
        tree.accept(Binder())
        return tree.accept(Dumper(semantics=True))

    def check(self, text, expected):
        self.assertEqual(self.parse_bind(text), expected)

    ############### TESTS ##############################

    def test_echappement(self):
        self.check("let var a := 3 function f() = let function g() = a in g() end in f() end", 
        "let var a/*e*/ := 3 function f() = let function g() = a/*2*/ in g() end in f() end")

    def test_echappement2(self):
        self.check("let var a := 3 var b := 4 function f(c: int) = a + c in f(b) end",
        "let var a/*e*/ := 3 var b := 4 function f(c: int) = (a/*1*/ + c) in f(b) end")
        
    ################ FIN TESTS ########################

    if __name__ == '__main__':
        unittest.main()

