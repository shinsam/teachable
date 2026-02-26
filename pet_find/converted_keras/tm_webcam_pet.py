import tensorflow as tf
from keras.models import load_model
import cv2
import numpy as np

# 1. 모델 불러오기 (keras_model.h5 파일이 같은 폴더에 있어야 함)
model = load_model("keras_model.h5", compile=False)

# 2. 라벨 불러오기 (labels.txt 파일이 같은 폴더에 있어야 함)
try:
    class_names = open("labels.txt", "r", encoding="utf-8").readlines()
except:
    class_names = ["Class 0", "Class 1"] # 파일이 없을 경우 기본값

# 3. 카메라 설정 (0번 기본 웹캠)
camera = cv2.VideoCapture(0)

print("프로그램이 실행되었습니다. 종료하려면 'q'를 누르세요.")

while True:
    print("..")
    ret, image = camera.read()
    if not ret: break

    display_image = image.copy()

    # 이미지 전처리 (224x224 크기 조정 및 정규화)
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    # 인공지능 예측
    prediction = model.predict(image, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # 화면에 결과 출력
    text = f"{class_name}: {round(confidence_score * 100, 2)}%"
    cv2.putText(display_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Teachable Machine Test", display_image)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

camera.release()
cv2.destroyAllWindows()