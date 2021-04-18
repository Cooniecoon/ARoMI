import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
from tf_pose.common import CocoPart

from classifier.model import import_classifier


import chatbot.chatbot_dialog as chatbot
import speech_recognition as sr
import socket

def ChatBot(header, url, payload):
    '''
    # 주변 환경 노이즈 측정 후, 음성 인식 threshold값 조절
    # with m as source: r.adjust_for_ambient_noise(source)
    # print("Set minimum energy threshold to {}".format(r.energy_threshold))
    '''

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


cam = cv2.VideoCapture(0)
ret_val, image = cam.read()

BODY_PARTS={
    'Nose' : 0,
    'REye' : 14, 'LEye' : 15,
    'REar' : 16, 'LEar' : 17,
    'Neck' : 1,
    'RShoulder' : 2, 'RElbow' : 3, 'RWrist' : 4,
    'LShoulder' : 5, 'LElbow' : 6, 'LWrist' : 7,
    'RHip' : 8, 'RKnee' : 9, 'RAnkle' : 10,
    'LHip' : 11, 'LKnee' : 12, 'LAnkle' : 13,
    'Background' : 18
}
    
classifier_path = "C:\\Users\\jeongseokoon\\capstone\\tf-pose-estimation\\classifier\\model\\pose_classification.weight"

if __name__ == "__main__":
    # Request 설정
    header, url, payload = chatbot.set_header()

    r = sr.Recognizer()
    m = sr.Microphone()

    classifier = import_classifier(output_shape=1)
    classifier.load_weights(classifier_path)
    
    w, h = model_wh("432x368") # default=0x0, Recommends : 432x368 or 656x368 or 1312x736 "
    e = TfPoseEstimator(
        get_graph_path("mobilenet_thin"), # "mobilenet_thin", "mobilenet_v2_large", "mobilenet_v2_small"
        target_size=(w, h),
        trt_bool=False,
    )
       

    while True:
        ret_val, image = cam.read()
        original_img=image.copy()

        humans = e.inference(
            image,
            resize_to_default=(w > 0 and h > 0),
            upsample_size=4.0,
        )
        
        if len(humans)>0:

            Body_Parts=humans[0].body_parts
            x_data = np.zeros((18, 2), dtype=np.float16)

            for i in range(CocoPart.Background.value):
                if i in humans[0].body_parts.keys():
                    body_part = humans[0].body_parts[i]
                    x_data[i] = np.array([body_part.x, body_part.y], dtype=np.float16)

            # print(x_data.reshape(1,x_data.shape[0], x_data.shape[1],1))
            preds = classifier.predict(
                        x_data.reshape(1,x_data.shape[0], x_data.shape[1],1)
                    ) #! pose classification

            if preds > 0.9:
                result = 'standing'
            else:
                result = 'sitting'
            print('pose : ',result)


            L_EAR_CHECK=BODY_PARTS['LEar'] in Body_Parts.keys()
            R_EAR_CHECK=BODY_PARTS['REar'] in Body_Parts.keys()
            NOSE_CHECK=BODY_PARTS['Nose'] in Body_Parts.keys()

            if (L_EAR_CHECK and R_EAR_CHECK and NOSE_CHECK):
                L_EAR_coordinate=Body_Parts[BODY_PARTS['LEar']]
                R_EAR_coordinate=Body_Parts[BODY_PARTS['REar']]

                face_box_x=min(L_EAR_coordinate.x, R_EAR_coordinate.x)
                face_box_w=abs(L_EAR_coordinate.x-R_EAR_coordinate.x)
                face_box_y=min(L_EAR_coordinate.y, R_EAR_coordinate.y)

                x1=int(face_box_x*original_img.shape[1])
                w=int(face_box_w*original_img.shape[1])
                x2=x1+w
                y1=int(face_box_y*original_img.shape[0])

                x_padding=15
                y_padding=10

                face_crop=original_img[max(0,y1-int(w)-y_padding):y1+int(w)+y_padding, x1-x_padding:x2+x_padding]
                face_crop_gray=cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
                face_box=cv2.resize(face_crop_gray, dsize=(48, 48), interpolation=cv2.INTER_AREA)

                cv2.imshow("_", face_box) #! face_box : input of FER

                # print('Eye Contact') #! Chatbot Litsening
                ChatBot(header, url, payload)
                

            elif ((not L_EAR_CHECK or not R_EAR_CHECK) and NOSE_CHECK):
                pass
                # print('Look Elsewhere')

        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        cv2.imshow("tf-pose-estimation result", image)


        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()