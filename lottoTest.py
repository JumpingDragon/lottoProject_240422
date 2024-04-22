import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1116"

html = requests.get(url).text
# print(html)

soup = BeautifulSoup(html, 'html.parser')

# 로또 추첨일
date = soup.find('p', class_='desc').text  # class_='desc'를 {'class':'desc'}로 그대로 바꿀 수 있음 (대괄호 포함)
lottoDate = datetime.strptime(date, "(%Y년 %m월 %d일 추첨)")
print(lottoDate)

# 로또당첨 번호 6개 리스트로 변환하여 반환
lottoNum = soup.find('div', {'class':'num win'}).find('p').text.strip().split('\n')
print(lottoNum)

lottoNumList = []
for num in lottoNum:
    lottoNumList.append(int(num))
print(lottoNumList)

# 보너스 번호 반환
bonusNum = int(soup.find('div', {'class':'num bonus'}).find('p').text.strip())
print(bonusNum)
