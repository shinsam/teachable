from keras.models import load_model
from PIL import Image, ImageOps
import glob # 폴더 내 파일 검색을 위한 라이브러리
import numpy as np
import os  # 폴더 내 파일 목록을 가져오기 위해 필요
import cv2 # 이미지를 화면에 보여주고 키보드 입력을 받기 위해 필요

# 1. 출력 및 환경 설정
np.set_printoptions(suppress=True)

# (중요)소스 파일이 있는 폴더로 작업 디렉토리 자동 변경 (경로 에러 방지)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 2. 모델 및 라벨 로드
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r", encoding="utf-8").readlines()

# 3. 입력 데이터 저장소(4차원 배열) 미리 준비
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 4. 이미지 폴더 탐색
# 현재 폴더(.) 내의 파일 중 이미지 확장자만 골라냅니다.
valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp') #튜플형태로 확장자 정의할 경우
#image_files = [f for f in glob.glob('imgs\\*') if f.lower().endswith(valid_extensions)]
# imgs 폴더 내의 파일 중에서 지정된 확장자로 끝나는 파일만 리스트에 저장

image_files = []
for f in glob.glob("imgs/*"):
    if f.lower().endswith(valid_extensions):    
        image_files.append(f)

if not image_files:
    print("폴더에 이미지 파일이 없습니다. 확장자 확인", valid_extensions )
    exit()

print(f"총 {len(image_files)}개의 이미지를 찾았습니다.")
print("▶ 아무 키나 누르면 다음 이미지로 넘어갑니다. (종료: Esc 또는 q)")

# 5. 폴더 내 모든 이미지 반복 처리
for file_name in image_files:
    # 이미지 불러오기
    image = Image.open(f'{file_name}').convert("RGB")
    
    # 전처리: Center Crop (224x224)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    
    # 정규화 (-1 ~ 1 사이 값으로 변환)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # 예측 실행
    prediction = model.predict(data, verbose=0)   #모델에게 물어보기
    index = np.argmax(prediction)           #가장 높은 확률의 인덱스
    class_name = class_names[index].strip() #인덱스에 해당하는 클래스 이름을 가져와서 공백 제거
    confidence_score = prediction[0][index] #인덱스에 해당하는 신뢰도 점수 가져오기``

    # ----------- 결과 시각화 (OpenCV 활용) ------------------
    # PIL 이미지를 OpenCV에서 보여줄 수 있도록 변환 (RGB -> BGR)
    display_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # 이미지 위에 텍스트 쓰기 (결과와 신뢰도 표시)
    result_text = f"Result: {class_name[2:]} ({confidence_score:.2%})"
    cv2.putText(display_img, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(display_img, "Quit:q", (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #디버깅 정보
    print(f"파일명: {file_name} 예측 결과: {class_name[2:]} 신뢰도: {confidence_score:.2%})") #파일명과 예측 결과를 줄바꿈으로 구분하여 출력
    
    # 화면에 표시
    cv2.imshow("AI Prediction Test", display_img)

    # 사용자의 키 입력 대기 (0은 아무 키나 누를 때까지 무한 대기)
    key = cv2.waitKey(0)
    if key == ord('q') or key == 27: # 'q' 또는 Esc 누르면 중단
        break

cv2.destroyAllWindows()
print("모든 이미지 검증이 완료되었습니다.")