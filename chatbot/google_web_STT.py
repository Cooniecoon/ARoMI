import speech_recognition as sr    # pip install SpeechRecognition
# pip install pyaudio
import os

class GoogleWebSTT:
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()

        # 주변 환경 노이즈 측정 후, 음성 인식 threshold값 조절
        # with m as source: r.adjust_for_ambient_noise(source)
        # print("Set minimum energy threshold to {0}".format(r.energy_threshold))

        self.r.dynamic_energy_threshold  = False
        self.r.energy_threshold = 1000

    def sound_to_text(self):
        text='음성을 이해하지 못했음'
        # 사용자 음성 입력
        with self.m as source:
            audio = self.r.listen(source)
            try:
                text = self.r.recognize_google(audio, language="ko-KR")
                # print("나: {0}".format(text))

            except sr.UnknownValueError:
                print("음성을 이해하지 못했습니다.")
                pass

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

        return text


if __name__ == "__main__":
    try:
        stt = GoogleWebSTT()
        print("대화를 시작합니다.")

        while True:
            text = stt.sound_to_text()
            print("나: {0}".format(text))

    except KeyboardInterrupt:
        print("대화를 종료합니다.")
        pass