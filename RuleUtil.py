SYMBOLS = ('+', '-', '*', '/', '(', ')')
BRACKETS = ('(', ')')
OPERATORS = ('+', '-', '*', '/')
SYMBOL_PRIORITY = {
    '+' : 0,
    '-' : 0,
    '*' : 1,
    '/' : 1,
    '(' : -1
}

def convertToPostfixExpr(infixExpr : str) -> list:
    result = []
    operStack = []
    word = ""
    for ch in infixExpr:
        if ch in SYMBOLS:
            # 遇到运算符，将之前的单词压结果栈
            if word:
                result.append(word)
                word = ""
            op = ch
            # 运算符处理
            if not operStack or op == '(':
                # 空栈或是左括号，直接压栈
                operStack.append(op)
            elif op == ')':
                # 右括号，将两个括号之间所有运算符出栈并压结果栈
                while operStack and operStack[-1] != '(':
                    result.append(operStack.pop())
                if not operStack:
                    # 未找到左括号
                    raise ValueError("括号不匹配")
                operStack.pop()
            else:
                while operStack:
                    # 比较优先级
                    lastOp = operStack[-1]
                    cmpRes = compareSymbolPriortity(op, lastOp)
                    if cmpRes <= 0:
                        # 相同或栈顶操作符更优先时，弹出栈顶元素并压结果栈
                        result.append(operStack.pop())
                    else:
                        # 当前操作符更优先时，当前操作符压栈
                        operStack.append(op)
                        break
                if not operStack:
                    operStack.append(op)
        else:
            word += ch
    # 剩余内容压栈
    if word:
        result.append(word)
    result.extend(operStack)
    # 结果校验
    operCnt = 0
    numCnt = 0
    for elem in result:
        if elem in OPERATORS:
            operCnt += 1
        elif elem not in BRACKETS:
            numCnt += 1
        else:
            raise ValueError("括号不匹配")
    if operCnt + 1 != numCnt:
        raise ValueError("表达式 %s 不合法" % infixExpr)
    return result

def compareSymbolPriortity(left : str, right : str) -> int:
    return SYMBOL_PRIORITY.get(left) - SYMBOL_PRIORITY.get(right)

def isOperator(symbol : str) -> bool:
    return symbol in OPERATORS

def calculateWithOperator(left : int, right : int, oper : str):
    if oper == '+':
        return left + right
    elif oper == '-':
        return left - right
    elif oper == '*':
        return left * right
    elif oper == '/':
        return left / right
    else:
        raise ValueError("不支持的运算符 %s" % oper)

if __name__ == '__main__':
    print(convertToPostfixExpr("a+b-a*((c+d)/e-f)+g"))