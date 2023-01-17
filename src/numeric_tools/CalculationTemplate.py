import RuleUtil
import NameUtil

class CalculationTemplate:
    name = ""
    baseTemplateMap = {}
    rulePostfixExpr = []

    def __init__(self, name : str, baseTemplates : list, ruleStr : str) -> None:
        NameUtil.checkNameNoPassRaiseError(name)
        self.name = name
        if baseTemplates:
            self.baseTemplateMap = { template.getName() : template for template in baseTemplates }
        else:
            self.baseTemplateMap = {}
        self.rulePostfixExpr = RuleUtil.convertToPostfixExpr(ruleStr)

    def __repr__(self) -> str:
        return "CalculationTemplate{"\
            + ("name=%s" % self.name)\
            + (", baseTemplateMap=%s" % self.baseTemplateMap)\
            + (", rulePostfixExpr=%s" % self.rulePostfixExpr)\
            + "}"

    def getName(self) -> str:
        return self.name

    def getBaseTemplateByName(self, name : str):
        return self.baseTemplateMap.get(name)

    def calculate(self, values : dict) -> int:
        # 自己有指定值，直接返回
        if self.name in values.keys():
            return values.get(self.name)
        # 没有算式，也没有指定值的情况下抛错
        if not self.rulePostfixExpr:
            raise ValueError("模板 %s 缺少指定值；没有指定算式的数值模板必须传入指定的值" % self.name)
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
            elif NameUtil.isValidName(word):
                # 递归计算该属性值压栈
                template = self.getBaseTemplateByName(word)
                if not template:
                    raise ValueError("找不到依赖模板 %s" % word)
                varStack.append(template.calculate(values))
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
    atk = CalculationTemplate('ATK', [], '20')
    defend = CalculationTemplate('DEF', [], '10')
    dmg = CalculationTemplate('DMG', [atk, defend], "(ATK-DEF*0.5)*2")
    resist = CalculationTemplate('RESIST', [defend], "DEF/(DEF+60)")
    finalDmg = CalculationTemplate('FINAL_DMG', [dmg, resist], "DMG*(1-RESIST)")
    print(finalDmg.calculate({'ATK' : 200, 'DEF' : 100}))