def getFieldNotNone(obj : dict, fieldName : str):
    something = obj.get(fieldName)
    if not something:
        raise ValueError("给定的 JSON 对象不含有 %s 字段。对象内容：%s" % (fieldName, obj))
    else:
        return something