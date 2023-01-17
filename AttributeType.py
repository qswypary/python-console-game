import RuleUtil

ALLOWED_NAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

class AttributeType:
    name = ""
    baseAttrTypeMap = {}
    rulePostfixExpr = []

    @staticmethod
    def isValidName(name : str) -> bool:
        for ch in name:
            if ch not in ALLOWED_NAME_CHARS:
                return False
        return True

    def __init__(self, name : str, baseAttrTypes : list, ruleStr : str) -> None:
        if not AttributeType.isValidName(name):
            raise ValueError("属性名称 %s 不合法。允许的字符：%s" % (name, ALLOWED_NAME_CHARS))
        self.name = name
        self.baseAttrTypeMap = { attrType.getName() : attrType for attrType in baseAttrTypes }
        self.rulePostfixExpr = RuleUtil.convertToPostfixExpr(ruleStr)

    def getName(self) -> str:
        return self.name

    def getBaseAttrTypeByName(self, name : str):
        return self.baseAttrTypeMap.get(name)

    def calculate(self, values : dict) -> int:
        # 自己有指定值，直接返回
        if self.name in values.keys():
            return values.get(self.name)
        # 根据算式递归计算
        varStack = []
        for word in self.rulePostfixExpr:
            if RuleUtil.isOperator(word):
                # 对栈顶元素进行运算
                rightValue = varStack.pop()
                leftValue = varStack.pop()
                resultValue = \
                    RuleUtil.calculateWithOperator(leftValue, rightValue, word)
                # 运算结果压栈
                varStack.append(resultValue)
            elif AttributeType.isValidName(word):
                # 递归计算该属性值压栈
                attrType = self.getBaseAttrTypeByName(word)
                if not attrType:
                    raise ValueError("找不到依赖属性 %s" % word)
                varStack.append(attrType.calculate(values))
            else:
                # 转为数字压栈
                try:
                    value = float(word)
                except ValueError:
                    raise ValueError("不合法的运算数 %s" % word)
                varStack.append(value)
        # 返回结果
        return varStack.pop()

if __name__ == '__main__':
    # 仅为测试数据，请勿模仿该用法
    atk = AttributeType('ATK', [], '20')
    defend = AttributeType('DEF', [], '10')
    dmg = AttributeType('DMG', [atk, defend], "(ATK-DEF*0.5)*2")
    resist = AttributeType('RESIST', [defend], "DEF/(DEF+60)")
    finalDmg = AttributeType('FINAL_DMG', [dmg, resist], "DMG*(1-RESIST)")
    print(finalDmg.calculate({'ATK' : 200, 'DEF' : 100}))