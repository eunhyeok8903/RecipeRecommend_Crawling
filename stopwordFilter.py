import re
from konlpy.tag import Okt

patternBlank = r'\([^)]*\)'
patternSymbol = '[^\w\s]'

class stopwordFilter:
    def __init__(self, myDB):
        self.stopword = set()
        self.okt = Okt()
        self.myDB = myDB

    # 불용어가 잘 처리되는지 확인하기 위해 DB의 재료를 ingredient.txt 로 받은 뒤
    # 불용어 처리한 재료를 ingredientListElimStopword.txt 에 다시 써서 제대로 가공됬는지 확인한다
    # (이 처리가 잘됨을 확인하면 그때 DB의 자료를 실제로 update 할것)
    def eliminateStopwordFromIngredient(self):
        self.deDuplicationStopword()
        f = open('textFile/stopwordList.txt', mode='rt', encoding='utf-8')
        for line in f:
            self.stopword.add(line.rstrip('\n'))
            if not line:
                break
        f.close()

        # self.makeIngredientToText()

        rf = open('textFile/ingredientList.txt', mode='rt', encoding='utf-8')
        wf = open('textFile/ingredientListElimStopword.txt', mode='wt', encoding='utf-8')
        #파이썬 정규 표현식 re를 사용하여 ingredientList.txt 전처리(공백,특수문자제거)
        for line in rf:
            line = re.sub(pattern=patternBlank, repl='', string=line)
            line = re.sub(pattern=patternSymbol, repl='', string=line)

            line = line.rstrip('\n')
            ingredientArr = line.split(' ')
            writeStr = str()
            for ingredient in ingredientArr:
                if ingredient not in self.stopword: #불용어인지 확인
                    # writeStr += (' ' + ingredient)
                    writeStr += (ingredient)
            if writeStr != str():
                writeStr = writeStr.lstrip(' ') + '\n'
                wf.write(writeStr)
            if not line:
                break

    #재료 받아오기
    def makeIngredientToText(self):
        #iname받아오기 'SELECT (iname) FROM ingredient'
        ingredientList = self.myDB.select_ingredient_iname()

        f = open('textFile/ingredientList.txt', mode='wt', encoding='utf-8')
        for ingredient in ingredientList:
            f.write(ingredient['iname'] + '\n') #iname
        f.close()

    #받아온 재료 중복 제거
    def deDuplicationStopword(self):
        f = open('textFile/stopwordList.txt', mode='rt', encoding='utf-8')
        mySet = set()
        for line in f:
            mySet.add(line.rstrip('\n'))
            if not line:
                break
        f.close()

        f = open('textFile/stopwordList.txt', mode='wt', encoding='utf-8')
        for ingredient in mySet:
            f.write(ingredient+ '\n')
        f.close()