import requests
from bs4 import BeautifulSoup

baseUrl = 'http://www.10000recipe.com/'


def CrawlingBetweenRanges(mydb, startRecipeId, endRecipeId):
    for i in range(startRecipeId, endRecipeId):
        if i % 10 == 0:
            print("count: " + str(i))
        res = PageCrawler('recipe/' + str(i))
        if res is None:
            continue

        menuId = mydb.insert_menu(res[0][0], baseUrl + 'recipe/' + str(i))
        for key, value in res[1].items():
            for name in value:
                if key == "[재료]" or key == "[양념]":
                    mydb.insert_ingredient(menuId, name)

        #recipe오더는 안함
        # for recipeOrder in res[2]:
        #   mydb.insert_recipeOrder(recipeOrder, menuId)


def PageCrawler(recipeUrl):
    url = baseUrl + recipeUrl

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    recipe_title = []  # 레시피 제목
    recipe_source = {}  # 레시피 재료
    # recipe_step = [] #레시피 순서

    try:
        res = soup.find('div', 'view2_summary')
        res = res.find('h3')
        recipe_title.append(res.get_text())
        res = soup.find('div', 'view2_summary_info')
        recipe_title.append(res.get_text().replace('\n', ''))
        res = soup.find('div', 'ready_ingre3')
    except(AttributeError):
        return

    # 재료 찾는 for문 가끔 형식에 맞지 않는 레시피들이 있어 try/ except 해준다
    try:
        for n in res.find_all('ul'):
            source = []
            title = n.find('b').get_text()
            recipe_source[title] = ''
            for tmp in n.find_all('li'):
                tempSource = tmp.get_text().replace('\n', '').replace(' ', ' ')
                source.append(tempSource.split("    ")[0])

            recipe_source[title] = source
    except (AttributeError):
        return

    # 요리 순서 찾는 for문
    # res = soup.find('div', 'view_step')
    # i = 0
    # for n in res.find_all('div', 'view_step_cont'):
    #     i = i + 1
    #     recipe_step.append(str(i) + '#' + n.get_text().replace('\n',' '))
    # 나중에 순서를 구분해주기 위해 숫자와 #을 넣는다.

    # 블로그 형식의 글은 스탭이 정확하게 되어있지 않기 때문에 제외해준다
    # if not recipe_step:
    #     return

    # recipe_all = [recipe_title, recipe_source, recipe_step]
    recipe_all = [recipe_title, recipe_source]
    print(recipe_all)
    return (recipe_all)