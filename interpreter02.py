import sys

class Interpreter(object):

    def __init__(self):
        self.look = ''
        self.Table = {}
        self.init()
        self.run()
    
    def run(self):
        while self.look != '.':
            if self.look == '?':
                self.input()
            elif self.look == '!':
                self.output()
            else:
                self.assignment()
            self.newline()
    
    # Read new character from input stream
    def getchar(self):
        self.look = sys.stdin.read(1)

    # Report an error
    def error(self, s):
        print ''
        print 'error: ', s, '.'
        raw_input()

    # Report error and halt
    def abort(self, s):
        self.error(s)
        exit()

    # Report what was expected
    def expected(self, s):
        self.abort(s + ' expected')

    # Match a specific input character
    def match(self, x):
        if self.look == x:
            self.getchar()
        else:
            self.expected(x)

    # Recognize an alpha character
    def isalpha(self, c):
        return c.isalpha()

    # Recognize a decimal digit
    def isdigit(self, c):
        return c.isdigit()

    # Recognize an addop
    def isaddop(self, c):
        return c in ['+', '-']

    # Recognize alphanumeric
    def isalnum(self, c):
        return c.isalnum()
      
    # Get an identifier
    def getname(self):
        if not self.isalpha(self.look):
            self.expected('Name')
        r = self.look.upper()
        self.getchar()
        return r

    # Get a number
    def getnum(self):
        value = 0
        if not self.isdigit(self.look):
            self.expected('Integer')
        while self.isdigit(self.look):
            value = 10 * value + int(self.look)
            self.getchar()
        return value

    # Parse and translate a maths factor
    def factor(self):
        if self.look == '(':
            self.match('(')
            r = self.Expression()
            self.match(')')
        elif self.isalpha(self.look):
            r = self.Table[self.getname()]
        else:
            r = self.getnum()
        return r
        
    # Parse and translate a maths term
    def term(self):
        value = self.factor()
        while self.look in ('*', '/'):
            if self.look == '*':
                self.match('*')
                value = value * self.factor()
            elif self.look == '/':
                self.match('/')
                value = value / self.factor()
        return value
        
    # Parse and translate an expression
    def expression(self):
        if self.isaddop(self.look):
            value = 0
        else:
            value = self.term()
        while self.isaddop(self.look):
            if self.look == '+':
                self.match('+')
                value = value + self.term()
            elif self.look == '-':
                self.match('-')
                value = value - self.term()
        return value

    # Initialize the variable area
    def inittable(self):
        for i in range(ord('A'), ord('Z')+1):
            self.Table[chr(i)] = 0

    # Parse and translate an assignment statement
    def assignment(self):
        name = self.getname()
        self.match('=')
        self.Table[name] = self.expression()
            
    # Recognize and skip over a newline
    def newline(self):
        if self.look == '\n':
            self.getchar()
            
    # Initialize
    def init(self):
        self.inittable()
        self.getchar()

    # Input routine
    def input(self):
        self.match('?')
        n = self.getname()
        self.Table[n] = int(raw_input())
        
    # Output routine
    def output(self):
        self.match('!')
        print self.Table[self.getname()]
    
# Main Program
if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run()
