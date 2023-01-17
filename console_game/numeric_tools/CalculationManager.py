import json
from CalculationTemplate import CalculationTemplate
from console_game.common import FilenameUtil
from console_game.common import JsonUtil

JSON_TEMPLATES_ROOT = "templates"
JSON_NAME = "name"
JSON_BASE_TEMPLATES = "baseTemplates"
JSON_RULE_EXPRESSION = "ruleExpression"

class CalculationManager:
    templateMap = {}

    def __init__(self) -> None:
        pass

    def loadFromJsonFile(self, filename : str) -> None:
        # 加载文件
        with open(filename) as file:
            # JSON 解析，获取模板列表
            templateJsonObjs = json.load(file).get(JSON_TEMPLATES_ROOT)
        templateObjMap = { JsonUtil.getFieldNotNone(obj, JSON_NAME) : obj for obj in templateJsonObjs }
        # 依次创建模板
        for name in templateObjMap.keys():
            # 已经创建过的跳过
            if name not in self.templateMap.keys():
                self.createTemplateByObjAndFillMap(templateObjMap, name)

    def createTemplateByObjAndFillMap(self, objMap : dict, currName : str) -> CalculationTemplate:
        currObj = objMap.get(currName)
        baseTemplateNames = currObj.get(JSON_BASE_TEMPLATES)
        baseTemplates = []
        # 有依赖的模板才进行处理
        if baseTemplateNames:
            for baseName in baseTemplateNames:
                template = self.templateMap.get(baseName)
                if not template:
                    # 依赖的模板未创建的，先进行递归创建
                    baseObj = objMap.get(baseName)
                    if not baseObj:
                        raise ValueError("模板 %s 依赖的模板 %s 不存在" % (currName, baseName))
                    template = self.createTemplateByObjAndFillMap(objMap, baseName)
                baseTemplates.append(template)
        ruleExpr = currObj.get(JSON_RULE_EXPRESSION)
        # 填入 map 并返回
        template = CalculationTemplate(currName, baseTemplates, ruleExpr)
        self.templateMap[currName] = template
        return template

if __name__ == "__main__":
    filename = FilenameUtil.convertToTrueFilePath("configs/calculation_templates.json")
    manager = CalculationManager()
    manager.loadFromJsonFile(filename)
    print(manager.templateMap)