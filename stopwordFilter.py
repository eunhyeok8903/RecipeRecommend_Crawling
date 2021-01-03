import re
from konlpy.tag import Okt
from konlpy.tag import Mecab

patternBlank = r'\([^)]*\)'
patternSymbol = '[^\w\s]'

class stopwordFilter:
    def __init__(self, myDB):
        self.stopword = set()
        self.mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
        self.myDB = myDB
        self.typoList = dict()

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
        for line in rf:
            line = re.sub(pattern=patternBlank, repl='', string=line)
            line = re.sub(pattern=patternSymbol, repl='', string=line)

            line = line.rstrip('\n')
            #mecab dictionary에서 우선순위처리와 단어등록해줘야하고 마지막으로 아래에서 불용어처리해주어야함
            temp=self.mecab.nouns(line)
            temp=" ".join(temp)
            ingredientArr = temp.split(' ')
            writeStr = ""
            #불용어처리
            for ingredient in ingredientArr:
                print(ingredient)
                if ingredient not in self.stopword and ingredient!="":
                    wf.write(ingredient+'\n')
            if not line:
                break

    def makeIngredientToText(self):
        ingredientList = self.myDB.select_ingredient_iname()
        f = open('textFile/ingredientList.txt', mode='wt', encoding='utf-8')
        for ingredient in ingredientList:
            f.write(ingredient['iname'] + '\n')
        f.close()


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

    def initTypoChanger(self):
        self.typoList.append({'typos' : ["머스타드, 머스터드"],
                              'except' : [],
                              'wrong' : '머스타드'})
        self.typoList.append({'typos' : ["양파"],
                              'except': [],
                              'wrong' : '양파'})
        self.typoList.append({'typos' : ["카레여왕"],
                              'except': [],
                              'wrong' : '카레'})
        self.typoList.append({'typos' : ["쌀국수"],
                              'except': ['소스', '스톡'],
                              'wrong' : '쌀국수'})
        self.typoList.append({'typos' : ["파프리카"],
                              'except': [],
                              'wrong' : '파프리카'})
        self.typoList.append({'typos' : ["베이컨"],
                              'except': [],
                              'wrong' : '베이컨'})
        self.typoList.append({'typos' : ["베이컨"],
                              'except': [],
                              'wrong' : '베이컨'})
        self.typoList.append({'typos' : ["우동면"],
                              'except': [],
                              'wrong' : '우동면'})
        self.typoList.append({'typos': ["오트밀"],
                              'except': [],
                              'wrong': '오트밀'})

    def typoChanger(self, line):
        for typo in self.typoList:

            aFlag = False
            tFlag = False
            for e in typo['except']:
                if line.find(e) != -1:
                    aFlag = True
            for t in typo['typos']:
                if line.find(t) != -1:
                    tFlag = True
            if aFlag is False and tFlag is True:
                return typo['wrong']
        return line