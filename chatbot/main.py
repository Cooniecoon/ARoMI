from google_web_STT import GoogleWebSTT
from chatbot import ChatBot
from TTS import TTS
from weather import get_weather_info

import socket
import json


with open('message_code.json', 'r') as f:
    messages = json.load(f)

# 연결할 서버(수신단)의 ip주소와 port번호
with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()
TCP_PORT = 7777

# 송신을 위한 socket 준비
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))


try:
    stt = GoogleWebSTT()
    chatbot = ChatBot()
    tts = TTS()

    print("대화를 시작합니다.")
    
    while True:
        text = stt.sound_to_text()
        print("나: {0}".format(text))

        if "날씨 알려 줘" in text:
            weather_data = get_weather_info()
            print("나: {0}".format(weather_data))
            tts.text_to_sound(weather_data)

        else:
            chatbot_output, flag = chatbot.get_response(text)
            print("ARoMI: {0}".format(chatbot_output))
            tts.text_to_sound(chatbot_output)

except KeyboardInterrupt:
    tts.driver.quit()
    print("대화를 종료합니다.")
    pass