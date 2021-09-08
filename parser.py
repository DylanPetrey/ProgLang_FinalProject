import sys
from lexer import *

def prettyPrintToken(tok):
    if tok[0] == SEMICOLON:
        return "';'"
    elif tok[0] == PRINT:
        return "'print'"
    elif tok[0] == INPUT:
        return "'get'"
    elif tok[0] == ASSIGN:
        return "'='"
    elif tok[0] == IF:
        return "'if'"
    elif tok[0] == THEN:
        return "'then'"
    elif tok[0] == ELSE:
        return "'else'"
    elif tok[0] == END:
        return "'end'"
    elif tok[0] == AND:
        return "'and'"
    elif tok[0] == OR:
        return "'or'"
    elif tok[0] == MODULO:
        return "'%'"
    elif tok[0] == GREATERTHAN:
        return "'>'"
    elif tok[0] == GREATER_EQUAL:
        return "'>='"
    elif tok[0] == LESSTHAN:
        return "'<'"
    elif tok[0] == LESS_EQUAL:
        return "'<='"
    elif tok[0] == DOUBLE_EQUAL:
        return "'=='"
    elif tok[0] == NOT_EQUAL:
        return "'!='"
    elif tok[0] == PARENOPEN:
        return "'('"
    elif tok[0] == PARENCLOSE:
        return "')'"
    elif tok[0] == NOT:
        return "'not'"
    elif tok[0] == ID_TOKEN or tok[0] == INT_TOKEN or tok[0] == STRING_TOKEN:
        return "'" + str(tok[1]) + "'"
    else:
        return NAMES[tok[0]]

def parseProg(progInput):
    parseStmtlist(progInput)

def parseStmtlist(listInput):
    for stmt in listInput:
        ret = parseStmt(stmt)
        if stmt[0][0] == PRINT:
            print(ret)
    return ret

def parseStmt(stmtInput):
    if stmtInput[0][0] == PRINT:
        ret = parsePrint(stmtInput)
    elif stmtInput[0][0] == INPUT:
        ret = parseInput(stmtInput)
    elif stmtInput[1][0] == ASSIGN:
        ret = parseAssign(stmtInput)
    elif stmtInput[0][0] == IF:
        ret = parseIf(stmtInput)
    return ret

#Parses the Print Function
def parsePrint(printInput):
    #Returns error if not PRINT
    if printInput[0][0] != PRINT:
       return [-1, printInput]
    elif printInput[1][0] == ID_TOKEN:
        return parseP_Arg(printInput)
    #Returns error if the input for the print function isn't a string
    elif printInput[1][0] != STRING_TOKEN:
       return [-1, printInput[1:]]
    #Replaces \n  with a line return
    if printInput[1][1].find("\\n") > 0:
       printInput [1][1] = printInput[1][1].replace("\\n", "\n")
    #Replaces \t with a tab
    elif printInput[1][1].find("\\t") > 0:
       printInput[1][1] = printInput[1][1].replace("\\t", "\t")
    #Replaces \\ with \
    elif printInput[1][1].find("\\\\") > 0:
       printInput[1][1] = printInput[1][1].replace("\\\\", "\\")
    #Replaces \\ with a blank
    elif printInput[1][1].find("\\") > 0:
        printInput[1][1] = printInput[1][1].replace("\\", "")
    #Returns result of the print statement
    return parseP_Arg(printInput)

def parseP_Arg(pInput):
    if pInput[1][0] == STRING_TOKEN:
        return pInput[1][1]
    elif pInput[1][0] == ID_TOKEN:
        if pInput[1][1] in varDict:
            return varDict[pInput[1][1]]
        else:
            parseExpr(pInput)
    else:
        return parseExpr(pInput)

def parseInput(inputInput):
    if inputInput[0][0] != INPUT:
        return [-1, inputInput]
    elif inputInput[1][0] != ID_TOKEN:
        return [-1, inputInput[1:]]
    val = input()
    varDict.update({inputInput[1][1]: int(val)})
    return inputInput[1][1]

def parseAssign(inputInput):
    if inputInput[0][0] != ID_TOKEN:
        return [-1, inputInput]
    elif inputInput[1][0] != ASSIGN:
        return [-1, inputInput[1:]]
    elif inputInput[2][0] != INT_TOKEN and inputInput[2][0] != ID_TOKEN:
        return [-1, inputInput[1:]]
    varDict.update({inputInput[0][1]: int(parseVars(inputInput[2:]))})
    return inputInput[1][0]

def parseIf(ifInput):
    return 0

def parseVars(e_input):
    for x in range(e_input.__len__()):
        if e_input[x][0] == ID_TOKEN:
            e_input[x][1] = varDict[e_input[x][1]]
    return parseExpr(e_input)

def parseExpr(e_input):
    return parseAddExpression(e_input)

def parseAddExpression(e_input):
    operand1 = parseMultExpresssion(e_input)
    while PLUS in e_input[1] or MINUS in e_input[1]:
        operator = e_input[1][0]
        if operator == PLUS or operator == MINUS:
            operand2 = parseMultExpresssion(e_input[2:])
            operand1[1] = applyOperator(operand1, operand2, operator)
        e_input = e_input[1:]
    return operand1[1]

def parseMultExpresssion(e_input):
    operand1 = parsePrimary(e_input)
    if e_input.__len__() < 2:
        return operand1;
    while MULT in e_input[1] or DIVIDE in e_input[1] or MODULO in e_input[1]:
        operator = e_input[1][0]
        if operator == DIVIDE or operator == MULT or operator == MODULO:
            operand2 = parsePrimary(e_input[2:])
            operand1[1] = applyOperator(operand1, operand2, operator)
        e_input = e_input[1:]
    return operand1

def parsePrimary(e_input):
    operand = e_input[0]
    if PARENOPEN == operand[0]:
        operand = parseExpr(e_input[2:])
    return operand

def applyOperator(operand1, operand2, operator):
    if operator == PLUS:
        return operand1[1] + operand2[1]
    elif operator == MINUS:
        return operand1[1] - operand2[1]
    elif operator == MULT:
        return operand1[1] * operand2[1]
    elif operator == DIVIDE:
        return operand1[1] / operand2[1]
    else:
        return operand1[1] % operand2[1]


file_object = open("lexerInput.txt", "r")
inputLine = file_object.readlines()
input2 = []
statementList = []
varDict = {}

for line in inputLine:
    tmp = nextToken(line)
    input2.clear()
    while tmp[0][0] != ENDSTREAM and tmp[0][0] != ERROR:
        if tmp[0][0] == SEMICOLON:
            tmp = nextToken(tmp[1])
        else:
            input2.append(tmp[0])
            tmp = nextToken(tmp[1])
    statementList.append(input2.copy())

if tmp[0][0] != ERROR:
    input2.append(tmp[0]) # Append ENDSTREAM token
    parseProg(statementList)
