from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

# Disable scientific notation for clarity : 
# 과학적 표기법을 끄고, 실수 형태로 출력하도록 설정
np.set_printoptions(suppress=True)

# Load the model : 소스와 같은 폴더에 있는지 확인하세요
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# 이 코드는 딥러닝 모델(Keras)이 데이터를 받아들일 수 있도록 입력 데이터의 '그릇'을 미리 만드는 과정입니다. 텐서플로우나 케라스 모델은 아무 데이터나 받지 않고, 아주 엄격하게 정해진 4차원 배열(4D Tensor) 형식을 요구합니다.
# 작성하신 shape=(1, 224, 224, 3)의 숫자들이 각각 무엇을 의미하는지 쉽게 풀어드릴게요.
# 1. 4차원 형태(Shape)의 비밀: (1, 224, 224, 3)
# 1 (Batch Size): 한 번에 모델에 넣을 이미지의 개수입니다. 지금은 '한 장'씩 테스트하므로 1입니다. 만약 10장을 동시에 예측한다면 이 숫자가 10이 됩니다.
# 224 (Height): 이미지의 세로 픽셀 수입니다. 티처블 머신 표준 모델은 224픽셀을 사용합니다.
# 224 (Width): 이미지의 가로 픽셀 수입니다.
# 3 (Channels): 색상 정보입니다. R, G, B 3가지 색상 채널을 의미합니다. (만약 흑백 이미지라면 1이 됩니다.)
# 2. dtype=np.float32는 왜 쓰나요?
# 이미지 파일(JPG, PNG 등)의 픽셀 값은 보통 0~255 사이의 정수(Integer)입니다. 하지만 딥러닝 모델 내부의 복잡한 수학 연산(가중치 곱셈 등)을 수행하려면 소수점 연산이 필요합니다.
# 따라서 데이터를 정수가 아닌 실수(Floating Point) 형태로 미리 정의해 두는 것입니다.

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# 이미지 이름을 씁니다. 소스와 같은 폴더에 있는지 확인하세요
image = Image.open("imgs\\4.jpg").convert("RGB")

# 이미지를 모델에 넣기 전, 단순히 구겨서 크기를 맞추는 게 아니라 비율을 유지하면서 가운데를 자르는(Center Crop) 과정은 딥러닝에서 매우 중요합니다. 사물이 찌그러지면 인공지능이 인식하기 어려워지기 때문이죠.

# 티처블 머신 코드에서 ImageOps.fit 함수가 바로 이 역할을 수행합니다.

# 1. 왜 그냥 리사이징(Resizing)을 안 하나요?
# 일반적인 리사이징을 하면 이미지의 가로세로 비율이 무시되어 사물이 길쭉해지거나 넙적해집니다. 반면, Center Crop 방식은 다음 단계를 거칩니다.
#인공지능 모델은 224x224 크기의 정사각형 창문으로 세상을 봐. 그런데 우리가 찍은 사진은 보통 직사각형이지? 이걸 억지로 창문에 구겨 넣으면 얼굴이 홀쭉해져서 AI가 못 알아볼 수 있어. 그래서 가장 중요한 가운데 부분만 예쁘게 오려서 보여주는 것이란다."
# 확대/축소: 이미지의 짧은 쪽을 224픽셀에 맞춥니다. (비율 유지)

# 중앙 정렬: 긴 쪽의 남는 부분을 양옆(또는 위아래)에서 똑같이 잘라냅니다.

# 결과: 사물의 특징이 왜곡되지 않은 정사각형 이미지가 생성됩니다.
size = (224, 224) # 224x224 크기에 딱 맞게 비율 유지하며 중앙 자르기
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array :이 한 줄의 코드는 '이미지 데이터'라는 시각적 정보를 '숫자 데이터'라는 행렬(Matrix)로 변환하는 결정적인 단계입니다.
image_array = np.asarray(image)

# Normalize the image : 정규화(Normalization)는 딥러닝 모델이 더 빠르고 안정적으로 학습할 수 있도록 입력 데이터를 일정한 범위로 조정하는 과정입니다. 대부분의 딥러닝 모델은 입력값이 0과 1 사이 또는 -1과 1 사이에 있기를 기대합니다. 이 경우, 픽셀 값이 0~255 범위에 있기 때문에 이를 -1~1 범위로 변환하는 것이 필요합니다.    
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data) #모델에게 물어보기"
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Print prediction and confidence score
print("Class:", class_name[2:], end="")
print("Confidence Score:", confidence_score)
