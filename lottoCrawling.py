import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import pymysql

def get_lottoNum(count):  # 로또 추첨 회차를 입력받음
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={count}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # 로또 추첨일
    date = soup.find('p', class_='desc').text  # class_='desc'를 {'class':'desc'}로 그대로 바꿀 수 있음 (대괄호 포함)
    lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")
    # 로또당첨 번호 6개 리스트로 변환하여 반환
    lottoNum = soup.find('div', {'class': 'num win'}).find('p').text.strip().split('\n')
    lottoNumList = []
    for num in lottoNum:
        lottoNumList.append(int(num))
    # 보너스 번호 반환
    bonusNum = int(soup.find('div', {'class': 'num bonus'}).find('p').text.strip())

    lottoDic = {'lottoDate': lottoDate, 'lottoNumber': lottoNumList, 'BonusNumber': bonusNum}

    return lottoDic

def get_recent_lottoCnt():  # 최신 로또 회차 크롤링 함수
    url = "https://dhlottery.co.kr/common.do?method=main"  # 동행복권 사이트 첫 페이지 주소
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    recent_cnt = soup.find('strong', {'id':'lottoDrwNo'}).text.strip()
    recent_cnt = int(recent_cnt)
    return recent_cnt

# print(get_recent_lottoCnt())

lottoDf_list = []

for cnt in range(1, get_recent_lottoCnt()+1):
    lottoResult = get_lottoNum(cnt)

    lottoDf_list.append({
        'count': cnt,  # 로또 추첨 회차
        'lottoDate': lottoResult['lottoDate'],  # 로또 추첨일
        'lottoNum1': lottoResult['lottoNumber'][0],  # 로또 당첨 번호 중 첫번째 번호
        'lottoNum2': lottoResult['lottoNumber'][1],  # 로또 당첨 번호 중 두번째 번호
        'lottoNum3': lottoResult['lottoNumber'][2],  # 로또 당첨 번호 중 세번째 번호
        'lottoNum4': lottoResult['lottoNumber'][3],  # 로또 당첨 번호 중 네번째 번호
        'lottoNum5': lottoResult['lottoNumber'][4],  # 로또 당첨 번호 중 다섯번째 번호
        'lottoNum6': lottoResult['lottoNumber'][5],  # 로또 당첨 번호 중 여섯번째 번호
        'bonusNum': lottoResult['BonusNumber']  # 로또 보너스 번호
    })
    print(f"{cnt} 회 처리 중...")

# print(lottoDf_list)

lottoDF = pd.DataFrame(data=lottoDf_list, columns=['count', 'lottoDate', 'lottoNum1',
                                         'lottoNum2', 'lottoNum3', 'lottoNum4',
                                         'lottoNum5', 'lottoNum6', 'bonusNum'])

print(lottoDF)

engine = create_engine("mysql+pymysql://root:12345@localhost:3306/lottodb?charset=utf8mb4")
engine.connect()

lottoDF.to_sql(name="lotto_tbl", con=engine, if_exists='append', index=False)
