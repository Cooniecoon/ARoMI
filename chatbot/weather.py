import requests    # conda install -c anaconda requests
from bs4 import BeautifulSoup    # conda install -c anaconda beautifulsoup4

def get_weather_info():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')

    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('div', {'class':'weather_box'})

    address = data1.find('span', {'class':'btn_select'}).text
    # print('현재 위치: '+address)
    current_temp = data1.find('span',{'class': 'todaytemp'}).text
    # print('현재 온도: '+current_temp+'℃')

    data2 = data1.findAll('dd')
    dust = data2[0].text[-2:]
    # print('현재 미세먼지: '+dust)
    ultra_dust = data2[1].text[-2:]
    # print('현재 초미세먼지: '+ultra_dust)

    weather_data = "현재 온도는 {0}도에 미세먼지는 {1}입니다.".format(current_temp, dust)
    # print(weather_data)

    return weather_data