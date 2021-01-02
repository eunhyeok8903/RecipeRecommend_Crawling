from database import MysqlController
from crawling import CrawlingBetweenRanges
from stopwordFilter import stopwordFilter
import env

baseUrl = 'http://www.10000recipe.com/'

def main():
    myDB = MysqlController(env.db_host, env.db_id, env.db_password, env.db_name)

    startRecipeId = 6845000
    endRecipeId = 6949705

    #크롤링(저장할 DB, 크롤링 시작할 URI번호, 끝번호)
    # CrawlingBetweenRanges(myDB, startRecipeId, endRecipeId)

    #불용어 처리
    swFilter = stopwordFilter(myDB)
    swFilter.makeIngredientToText()
    swFilter.eliminateStopwordFromIngredient()


if __name__ == '__main__':
    main()