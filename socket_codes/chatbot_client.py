import speech_recognition as sr
import socket
import json
from time import sleep

from socket_funcs import *

# import upper directory
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import chatbot.chatbot_dialog as chatbot

with open('message_code.json', 'r') as f:
    messages = json.load(f)



def ChatBot(header, url, payload):

    # 주변 환경 노이즈 측정 후, 음성 인식 threshold값 조절
    with m as source: r.adjust_for_ambient_noise(source)

    # print("Set minimum energy threshold to {}".format(r.energy_threshold))


    print("대화를 시작합니다.")

    # 음성대화 파트
    with m as source:
        audio = r.listen(source)  # 사용자 음성 입력
        try:
            input_text = r.recognize_google(audio, language="ko-KR")
            print("나: {0}".format(input_text))
        except sr.UnknownValueError:
            print("음성을 이해하지 못했습니다.")
            pass
         
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        else:
            # 사용자 입력 대화 전송
            response = chatbot.send_request(input_text, header, url, payload)
            # 챗봇 반응 출력
            payload = chatbot.get_response(response, payload)



# 연결할 서버(수신단)의 ip주소와 port번호
with open('AWS_IP.txt', 'r') as f:
    TCP_IP = f.readline()

TCP_PORT = 7777
eye_checker = socket.socket()
eye_checker.connect((TCP_IP, TCP_PORT))

sleep(1)
TCP_PORT = 9999
pose_emotion = socket.socket()
pose_emotion.connect((TCP_IP, TCP_PORT))

print('connected')
# Request 설정
header, url, payload = chatbot.set_header()

r = sr.Recognizer()
m = sr.Microphone()

while True:
    msg = eye_checker.recv(1)
    pe_msg=pose_emotion.recv(4)
    pe_msg=pe_msg.decode()
    pe_msg=pe_msg.split(',')
    print('pose, emotion :',pe_msg)
    if msg.decode() == messages['chatbot']:
        ChatBot(header, url, payload)
        print('eye contacted')
    elif msg.decode() == messages['pass']:
        print('eye not contacted')
        continue

    
    else:
        break
