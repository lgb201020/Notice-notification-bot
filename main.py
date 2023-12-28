import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time


URL = "학과 홈페이지 공지사항 url"
mytoken = "slack-bot token"

def to_find_notice(url):
    res =  requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    """
    웹 서버로부터 응답 받은 객체 중에서 text 속성(HTML 소스 코드)을 선택하고, 
    우리가 받은 HTML 소스 코드를 lxml 파서를 통해 BeautifulSoup 객체로 만든다(응답받은 데이터를 soup 변수에 할당한다)
    """

    to_find_notice2 = soup.findAll("td", attrs={"class" : "_artclTdRdate"})
    notice_date = []
    for nt in to_find_notice2:
        strdata_of_date = str(list(nt)[0])
        date_data = datetime.strptime(strdata_of_date, "%Y.%m.%d")
        notice_date.append(date_data)
    return sorted(notice_date, reverse=True)


def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )



while True:
    try:
        if to_find_notice(URL)[0]==datetime.today():
            text_notification = "전자공 공지사항에 새로운 공지글이 올라왔어요."
            post_message(mytoken,"#notice_notification",text_notification )
        else:
            time.sleep(3600)
            
    except Exception as e:
        print(e)
        text_error = "오류가 발생했어요."
        post_message(mytoken,"#notice_notification",text_error )
        time.sleep(1)
