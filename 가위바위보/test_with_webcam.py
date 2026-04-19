import cv2
import numpy as np
from keras.models import load_model
import os
from PIL import Image, ImageOps


# (중요)소스 파일이 있는 폴더로 작업 디렉토리 자동 변경 (경로 에러 방지)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. 모델과 라벨 읽어오기
model = load_model('keras_model.h5', compile=False)
class_names = open('labels.txt', 'r', encoding='utf-8').readlines()

# 2. 웹캠 연결 (0번은 기본 카메라)
cap = cv2.VideoCapture(0)

while True:
    # 카메라 프레임 읽기
    ret, frame = cap.read()
    if not ret: break

    # 3. 이미지 전처리 (모델 입력 크기에 맞게 224x224로 조절)
    input_img = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    input_img = np.asarray(input_img, dtype=np.float32).reshape(1, 224, 224, 3)
    
    # 데이터 정규화 (티처블 머신 기본 설정: -1 ~ 1 사이 값)
    input_img = (input_img / 127.5) - 1

    # 4. 모델 예측
    prediction = model.predict(input_img, verbose=0)
    index = np.argmax(prediction) # 가장 높은 확률의 인덱스
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # 5. 화면에 결과 출력
    text = f"{class_name}: {round(confidence_score * 100, 2)}%"
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('AI Webcam Test', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()