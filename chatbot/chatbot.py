import requests    # conda install -c anaconda requests
import json

class ChatBot:
    def __init__(self):
        self.header = {
            'Authorization': "Basic a2V5OjVjMmQ5OWVmZWJiNTE1MjhjZTFjMWZmZDdiOTI5ZWZh"  # 본인 인증키
        }

        self.sessionid = "ARoMI"
        self.url = "https://builder.pingpong.us/api/builder/6040407ae4b078d873a16e71/integration/v0.2/custom/" + self.sessionid

        self.payload = {
            'request': {
                'dialog': []
            }
        }

        self.MAX_TURN = 5

    def get_response(self, input_text):
        self.payload["request"]["dialog"].append(input_text)

        response = requests.post(self.url, json=self.payload, headers=self.header)

        json_data = response.text
        data = json.loads(json_data)
        output = data.get("response").get("replies")[0].get("text")
        output_text = output[:-1]
        flag = output[-1]
        self.payload["request"]["dialog"].append(output_text)

        if len(self.payload["request"]["dialog"]) >= self.MAX_TURN:
            while len(self.payload["request"]["dialog"]) >= self.MAX_TURN:
                self.payload["request"]["dialog"].pop(0)

        return output_text, flag


if __name__ == "__main__":
    chatbot = ChatBot()
    print("대화를 시작합니다.('q'입력 시 종료됩니다.)")

    while True:
        input_text = input("나: ")
        
        if input_text == 'q':
            print("대화를 종료합니다.")
            break

        output_text, flag = chatbot.get_response(input_text)
        print("ARoMI: {0}".format(output_text))
        # print("ARoMI: {0}".format(flag))