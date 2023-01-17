import os
import sys

def convertToTrueFilePath(relativePath : str):
    """指定相对于项目根目录的相对路径（以正斜杠分割，如：configs/config.json），
    该方法将其转换为适合当前系统的绝对路径返回"""
    return os.path.abspath(os.path.normpath(sys.path[0] + "/../../" + relativePath))

if __name__ == "__main__":
    print(convertToTrueFilePath("configs/config.json"))