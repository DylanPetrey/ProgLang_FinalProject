import sys

ERROR = -1
SEMICOLON = 0       # ;
PRINT = 1           # print
INPUT = 2           # get
ASSIGN = 3          # =
IF = 4              # if
THEN = 5            # then
ELSE = 6            # else
END = 7             # end
AND = 8             # and
OR = 9              # or
PLUS = 10           # +
MINUS = 11          # -
MULT = 12           # *
DIVIDE = 13         # /
MODULO = 14         # %
GREATERTHAN = 15    # >
GREATER_EQUAL = 16  # >=
LESSTHAN = 17       # <
LESS_EQUAL = 18     # <=
DOUBLE_EQUAL = 19   # ==
NOT_EQUAL = 20      # !=
PARENOPEN = 21      # (
PARENCLOSE = 22     # )
NOT = 23            # not
ID_TOKEN = 24       # Variable name
INT_TOKEN = 25      # Int
STRING_TOKEN = 26   # String
ENDSTREAM = 27      # End

NAMES = ["SEMICOLON", "PRINT", "INPUT", "ASSIGN", "IF", "THEN", "ELSE", "END",
         "AND", "OR", "PLUS", "MINUS", "MULT", "DIVIDE", "MODULO", "GREATERTHAN",
         "GREATER_EQUAL", "LESSTHAN", "LESS_EQUAL", "DOUBLE_EQUAL", "NOT_EQUAL",
         "PARENOPEN", "PARENCLOSE", "NOT", "ID_TOKEN", "INT_TOKEN", "STRING_TOKEN",
         "ENDSTREAM"]


def isIdStart(c):
    return c == "_" or (c.isalpha())


def isIdChar(c):
    return c == "_" or c.isalpha() or c.isdigit()


def isOperator(c):
    return c == "+" or c == "-" or c == "*" or c == "/" or c == "%"


def lexId(input):
    lexeme = input[0]
    i = 1
    while i < len(input) and isIdChar(input[i]):
        lexeme = lexeme + input[i]
        i = i + 1
    if lexeme == "print":
        return [[PRINT], input[i:]]
    elif lexeme == "get":
        return [[INPUT], input[i:]]
    elif lexeme == "if":
        return [[IF], input[i:]]
    elif lexeme == "then":
        return [[THEN], input[i:]]
    elif lexeme == "else":
        return [[ELSE], input[i:]]
    elif lexeme == "end":
        return [[END], input[i:]]
    elif lexeme == "and":
        return [[AND], input[i:]]
    elif lexeme == "or":
        return [[OR], input[i:]]
    elif lexeme == "not":
        return [[NOT], input[i:]]
    else:
        return [[ID_TOKEN, lexeme], input[i:]]


def lexPercent(input):
    lexeme = input[0]
    i = 1
    while i < len(input) and input[i].isdigit():
        lexeme = lexeme + input[i]
        i = i + 1
    return [[INT_TOKEN, int(lexeme)], input[i:]]


def stringId(input):
    lexeme = input[0]
    i = 1
    while i < len(input) and not input[i] == "\"":
        lexeme = lexeme + input[i]
        i = i + 1

    lexeme = lexeme + input[i]
    i = i + 1
    return [[STRING_TOKEN, lexeme], input[i:]]


def nextToken(input):
    i = 0
    while i < len(input) and input[i].isspace():
        i = i + 1
    if i >= len(input):
        return [[ENDSTREAM, None], []]
    elif input[i] == ";":
        return [[SEMICOLON], input[i + 1:]]
    elif input[i] == "+":
        return [[PLUS], input[i + 1:]]
    elif input[i] == "-":
        return [[MINUS], input[i + 1:]]
    elif input[i] == "*":
        return [[MULT], input[i + 1:]]
    elif input[i] == "/":
        return [[DIVIDE], input[i + 1:]]
    elif input[i] == "%":
        return [[MODULO], input[i + 1:]]
    elif input[i] == ">":
        if i + 1 < len(input) and input[i + 1] == "=":
            return [[GREATER_EQUAL], input[i + 2:]]
        return [[GREATERTHAN], input[i + 1:]]
    elif input[i] == "<":
        if i + 1 < len(input) and input[i + 1] == "=":
            return [[LESS_EQUAL], input[i + 2:]]
        return [[LESSTHAN], input[i + 1:]]
    elif input[i] == "=":
        if i + 1 < len(input) and input[i + 1] == "=":
            return [[DOUBLE_EQUAL], input[i + 2:]]
        return [[ASSIGN], input[i + 1:]]
    elif input[i] == "!" and i + 1 < len(input) and input[i + 1] == "=":
        return [[NOT_EQUAL], input[i + 2:]]
    elif input[i] == "\"":
        return stringId(input[i:])
    elif input[i] == "(":
        return [[PARENOPEN], input[i + 1:]]
    elif input[i] == ")":
        return [[PARENCLOSE], input[i + 1:]]
    elif isIdStart(input[i]):
        return lexId(input[i:])
    elif input[i].isdigit():
        return lexPercent(input[i:])
    else:
        return [[ERROR, "Unrecognized Symbol"], input[i:]]


# Test Driver Program
# print out result of lexer
def printToken(t):
    if len(t) >= 2:
        print(NAMES[t[0]] + "(" + str(t[1]) + ")")
    else:
        print(NAMES[t[0]])


if __name__ == '__main__':
    # Can also open a file (name provided on the commandline) and read from it.
    # may also read characters as needed instead of into a big list like this
    file_object = open("lexerInput", "r")
    input = file_object.readlines()
    for iterator in input:
        tmp = nextToken(iterator)
        while tmp[0][0] != ENDSTREAM and tmp[0][0] != ERROR:
            printToken(tmp[0])
            tmp = nextToken(tmp[1])
        if tmp[0][0] == ERROR:
            print("Error: " + tmp[0][1])
    file_object.close();
