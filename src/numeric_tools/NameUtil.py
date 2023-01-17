ALLOWED_NAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"

def isValidName(name : str) -> bool:
    for ch in name:
        if ch not in ALLOWED_NAME_CHARS:
            return False
    return True

def checkNameNoPassRaiseError(name : str) -> None:
    if not name:
        raise ValueError("名称不能为空")
    if not isValidName(name):
        raise ValueError("名称 %s 不合法。允许的字符：%s" % (name, ALLOWED_NAME_CHARS))