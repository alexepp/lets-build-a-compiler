import sys

look = '' # lookahead Character

def upcase(c):
    return c.upper()
    
# Read new character from input stream
def getchar():
    global look
    look = sys.stdin.read(1)

# Report an error
def error(s):
    print ''
    print 'Error: ', s, '.'
    raw_input()

# Report error and halt
def abort(s):
    error(s)
    exit()

# Output a string with tab
def emit(s):
    print '\t' + s,

# Output a string with tab and CRLF
def emitln(s):
    emit(s)
    print ''

# Report what was expected
def expected(s):
    abort(s + ' expected')

# match a specific input character
def match(x):
    if look != x:
        expected("'''" + x + "'''")
    else:
        getchar()
        skipwhite()

# Recognize an alpha character
def isalpha(c):
    return c.isalpha()

# Recognize whie space
def iswhite(c):
    return c in [' ', '\t']
    
# Recognize alphanumeric
def isalnum(c):
    return isalpha(c) or isdigit(c)
    
# Recognize a decimal digit
def isdigit(c):
    return c.isdigit()

# Recognize an addop
def isaddop(c):
    return c in ['+', '-']
    
# Get an identifier
def getname():
    token = ''
    if not isalpha(look):
        expected('Name')
    while isalnum(look):
        token = token + upcase(look)
        getchar()
    r = token
    skipwhite()
    return r

# Get a number
def getnum():
    value = ''
    if not isdigit(look):
        expected('Integer')
    while isdigit(look):
        value = value + look
        getchar()
    r = value
    skipwhite()
    return r

# Skip over leading white space
def skipwhite():
    while iswhite(look):
        getchar()

# Initialize
def init():
    getchar()
    skipwhite()

# Parse and translate an identifier
def ident():
    name = getname()
    if look == '(':
        match('(')
        match(')')
        emitln('CALL ' + name)
    else:
        emitln('MOV EAX, ' + name)
    
# Parse and translate a math factor
def factor():
    if look == '(':
        match('(')
        expression()
        match(')')
    elif isalpha(look):
        ident()
    else:
        emitln('MOV EAX, ' + getnum())
    
# Parse and translate a maths expression
def term():
    factor()
    while look in ['*', '/']:
        emitln('PUSH EAX')
        if look == '*':
            multiply()
        elif look == '/':
            divide()
    
# Parse and translate a maths expression
def expression():
    if isaddop(look):
        emitln('XOR EAX, EAX') # clear EAX
    else:
        term()
    while isaddop(look):
        emitln('PUSH EAX')
        if look == '+':
            add()
        elif look == '-':
            subtract()

# Parse and translate an assignment statement
def assignment():
    name = getname()
    match('=')
    expression()
    emitln('MOV ' + name + ', EAX')
            
# Recognize and translate an add
def add():
    match('+')
    term()
    emitln('POP ECX')
    emitln('ADD EAX, ECX')
    
# Recognize and translate a subtract
def subtract():
    match('-')
    term()
    emitln('POP ECX')
    emitln('SUB EAX, ECX')
    emitln('NEG EAX')

# Recognize and translate a multiply
def multiply():
    match('*')
    factor()
    emitln('POP ECX')
    emitln('IMUL ECX')

# Recognize and translate a divide
def divide():
    match('/')
    factor()
    emitln('MOV ECX, EAX')
    emitln('POP EAX')
    emitln('XOR EDX, EDX')
    emitln('IDIV ECX')
    
# Main Program
if __name__ == '__main__':
    init()
    assignment()
    if look != '\n':
        expected('Newline')
    raw_input()
