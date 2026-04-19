import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="AI 웹캠 분류기", layout="centered")
st.title("📷 실시간 AI 카메라")
st.write("카메라 앞에 사물을 두고 사진을 찍어보세요!")

# --- 2. 모델 로드 (캐싱) ---
@st.cache_resource
def load_resource():
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path,  "model_unquant.tflite")
    label_path = os.path.join(base_path,  "labels.txt")
    
    interpreter = tf.lite.Interpreter(model_path=model_path)# 모델 로드
    interpreter.allocate_tensors()# 모델이 사용할 메모리를 할당하는 과정입니다.
    
    with open(label_path, "r", encoding="utf-8") as f:# 라벨 파일 읽기
        labels = [line.strip() for line in f.readlines()]
    return interpreter, labels

interpreter, labels = load_resource()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# --- 3. 웹캠 입력 섹션 ---
# 학생들에게 가장 신기한 부분입니다!
img_file_buffer = st.camera_input("카메라를 바라봐 주세요")

if img_file_buffer is not None:# 사진이 찍히면 실행되는 부분입니다.`
    # 1) 사진 읽기
    image = Image.open(img_file_buffer).convert("RGB")
    
    # 2) 티쳐블 머신 규격에 맞게 전처리 (224x224)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    img_array = np.asarray(image).astype(np.float32)
    img_array = (img_array / 127.5) - 1  # 정규화
    img_array = np.expand_dims(img_array, axis=0)

    # 3) AI 추론 실행
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    prediction = interpreter.get_tensor(output_details[0]['index'])[0]

    # 4) 결과 분석
    max_idx = np.argmax(prediction)
    confidence = prediction[max_idx]
    label_name = labels[max_idx]

    # --- 4. 시각적 피드백 ---
    st.divider()
    if confidence > 0.7:  # 신뢰도가 높을 때
        st.success(f"이것은 **{label_name}**일 확률이 높습니다! (정확도: {confidence*100:.1f}%)")
        st.balloons()
    else:
        st.warning(f"음.. **{label_name}** 같긴 한데, 좀 더 가까이 보여주세요. (정확도: {confidence*100:.1f}%)")
    
    # 각 클래스별 확률을 막대그래프로 표시
    st.write("### 📊 분석 상세 정보")
    for i, prob in enumerate(prediction):
        st.write(f"{labels[i]}")
        st.progress(float(prob))