import requests
import json

def set_header():
    # 헤더 설정
    header = {
        'Authorization': "Basic a2V5OjVjMmQ5OWVmZWJiNTE1MjhjZTFjMWZmZDdiOTI5ZWZh"  # 본인 인증키
    }

    # 주소 설정
    sessionid = "ARoMI"  # Session id -> 내가 설정하는 값
    url = "https://builder.pingpong.us/api/builder/6040407ae4b078d873a16e71/integration/v0.2/custom/" + sessionid

    # Request Body 설정
    payload = {
        'request': {
            'dialog': []
        }
    }

    return header, url, payload

def send_request(input_text, header, url, payload):
    # 전송할 대화 목록(dialog)에 입력 추가
    payload["request"]["dialog"].append(input_text)

    # Request 전송
    # post 방식, json 옵션 사용 시 JSON 포멧의 데이터를 전송할 수 있으며,
    # 이때 Content-Type 요청 헤더는 application/json로 자동 설정됨
    response = requests.post(url, json=payload, headers=header)

    return response

def get_response(response, payload, MAX_TURN=5):
    # Response 확인 및 대화 데이터 출력
    json_data = response.text  # json 포멧의 응답 데이터
    data = json.loads(json_data)  # json 포멧을 dictionary 포멧으로 변환
    output_text = data.get("response").get("replies")[0].get("text")  # 대화 데이터 추출
    print("ARoMI: {0}".format(output_text))  # 대화 출력

    # dialog에 대화 내역 추가
    payload["request"]["dialog"].append(output_text)

    # 최대 5턴으로 전송 가능 대화 제한
    if len(payload["request"]["dialog"]) >= MAX_TURN:
        while len(payload["request"]["dialog"]) >= MAX_TURN:
            payload["request"]["dialog"].pop(0)

    return payload
