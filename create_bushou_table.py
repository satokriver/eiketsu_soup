import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_strat_detail(url):
    htmltext = requests.get(url).text
    soup = BeautifulSoup(htmltext, 'html.parser')
    table = soup.findAll('table')[1]
    trs = table.findAll('tr')
    strat_name = trs[0].find('ruby').contents[0] # 計略名
    strat_cost = trs[3].find('td').text # 士気
    strat_effect = trs[4].text # 効果
    table = soup.findAll('table', {'class': 'font_smaller keiryakudata'})[0]
    lis = table.findAll('tr')[1].findAll('li')
    detail_text = '\n'.join([li.text for li in lis]) # 実効果
    return strat_name, strat_cost, strat_effect, detail_text

def get_color(url):
    htmltext = requests.get(url).text
    soup = BeautifulSoup(htmltext, 'html.parser')
    table = soup.findAll('table', {'class': 'font_xxsmaller'})[0]
    rows = table.findAll('tr')[1:] # 1つ目はヘッダー列なのでスキップ
    df = pd.DataFrame()
    for row in rows:
        c = row.findAll('td')
        strat_name, strat_cost, strat_effect, detail_text = get_strat_detail(c[2].find('a').get('href'))
        ser = pd.Series([c[4].text, c[5].text, c[2].text, c[3].text, c[1].text, c[6].text, c[7].text, c[8].text, c[9].text, strat_name, strat_cost, strat_effect, detail_text])
        df = pd.concat([df, ser.to_frame().T], ignore_index=True)
    return df

df = pd.DataFrame()
blue_df = get_color('https://eiketsudb.gamewiki.jp/%e3%82%ab%e3%83%bc%e3%83%89%e3%83%aa%e3%82%b9%e3%83%88%ef%bc%88%e8%92%bc%ef%bc%89/')
df = pd.concat([df, blue_df], ignore_index=True)
red_df = get_color('https://eiketsudb.gamewiki.jp/%e3%82%ab%e3%83%bc%e3%83%89%e3%83%aa%e3%82%b9%e3%83%88%ef%bc%88%e7%b7%8b%ef%bc%89/')
df = pd.concat([df, red_df], ignore_index=True)
grean_df = get_color('https://eiketsudb.gamewiki.jp/%e3%82%ab%e3%83%bc%e3%83%89%e3%83%aa%e3%82%b9%e3%83%88%ef%bc%88%e7%a2%a7%ef%bc%89/')
df = pd.concat([df, grean_df], ignore_index=True)
black_df = get_color('https://eiketsudb.gamewiki.jp/%e6%ad%a6%e5%b0%86%e3%83%aa%e3%82%b9%e3%83%88%ef%bc%88%e7%8e%84%ef%bc%89/')
df = pd.concat([df, black_df], ignore_index=True)

df.columns = ['勢力','時代', '名前', 'コスト', 'レアリティ', '兵種', '武力', '知力', '特技', '計略名', '士気', '効果', '実効果']
df.to_csv('mylist.csv', index=None, encoding='utf-8_sig')