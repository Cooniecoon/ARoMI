import requests    # conda install -c anaconda requests
from selenium import webdriver    # conda install -c conda-forge selenium
from selenium.webdriver.common.keys import Keys

class TTS:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()

        # self.driver.implicitly_wait(1)

        self.url = 'http://localhost:5000/tts-server/text-inference'
        
    def text_to_sound(self, intput_text):
        self.driver.get(self.url)

        text_place = self.driver.find_element_by_id("text")
        play_button = self.driver.find_element_by_id("infer")

        text_place.send_keys(Keys.CONTROL + "a")
        text_place.send_keys(intput_text)

        play_button.click()


if __name__ == "__main__":
    tts = TTS()
    tts.text_to_sound("로딩이 완료되었습니다.")

    while True:
        intput_text = input("Input Text: ")
        
        if intput_text == 'q':
            break

        tts.text_to_sound(intput_text)

    tts.driver.quit()