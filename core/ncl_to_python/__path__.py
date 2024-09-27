import sys
import os

def LoadSearchPaths():
    for i,j,y in os.walk(os.getcwd()):
        if(str(i).find('__pycache__') == -1 and str(i).find('.vscode') == -1):
            sys.path.append(i)
