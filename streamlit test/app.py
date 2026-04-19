import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
import os

# 1. 페이지 설정
st.set_page_config(page_title="OpenCV x AI 분류기", layout="centered")
st.title("📸 OpenCV AI 이미지 판독기")
st.write("OpenCV를 이용해 이미지를 처리하고 AI로 분류해봅시다.")

# 2. 모델 로드 함수
@st.cache_resource
def load_ai_model():
    model_path = "model_unquant.tflite"
    label_path = "labels.txt"
    
    if not os.path.exists(model_path):
        return None, None
    
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    with open(label_path, "r", encoding="utf-8") as f:
        labels = [line.strip() for line in f.readlines()]
        
    return interpreter, labels

interpreter, labels = load_ai_model()

# 3. 이미지 입력 (카메라 또는 파일 선택)
option = st.radio("입력 방식 선택", ("카메라로 찍기", "파일 업로드하기"))

if option == "카메라로 찍기":
    img_file = st.camera_input("카메라 앞에 물체를 두세요")
else:
    img_file = st.file_uploader("이미지를 업로드하세요", type=['jpg', 'png', 'jpeg'])

if img_file is not None:
    # --- OpenCV 처리 시작 ---
    # 4. 파일을 바이트 배열로 읽어서 OpenCV 이미지 객체로 변환
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1) # BGR 컬러 이미지로 읽기
    
    # 5. OpenCV 전처리 (BFP -> RGB 변환 및 크기 조절)
    # 티쳐블 머신은 RGB를 사용하지만 OpenCV는 BGR로 읽으므로 변환이 필요합니다.
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(opencv_image, (224, 224), interpolation=cv2.INTER_AREA)
    
    # 결과 화면 출력
    st.image(opencv_image, caption="OpenCV로 처리된 이미지", use_container_width=True)

    # 6. AI 모델용 데이터 정규화
    input_data = np.asarray(resized_image).astype(np.float32)
    input_data = (input_data / 127.5) - 1 # -1 ~ 1 사이로 정규화
    input_data = np.expand_dims(input_data, axis=0)

    # 7. 추론 실행
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])[0]
    
    # 8. 결과 표시
    idx = np.argmax(prediction)
    score = prediction[idx]

    st.subheader(f"판독 결과: {labels[idx]}")
    st.write(f"신뢰도: {score*100:.2f}%")
    st.progress(float(score))