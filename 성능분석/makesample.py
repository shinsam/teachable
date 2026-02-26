# 1. 500건의 샘플 데이터 CSV 생성 (Python Script)
# 실제 이미지가 없더라도 구조를 이해하실 수 있도록, 임의의 파일명과 정답(Label)이 매칭된 500행의 CSV를 만드는 코드입니다.


import pandas as pd
import random

# 클래스 정의 (티쳐블 머신에서 설정한 클래스 이름과 맞춰주세요)
classes = ['Class A', 'Class B', 'Class C']

data = {
    'filename': [f'image_{i:03d}.jpg' for i in range(1, 501)],
    'actual_label': [random.choice(classes) for _ in range(500)]
}

df = pd.DataFrame(data)
df.to_csv('test_data_500.csv', index=False)
print("test_data_500.csv 파일이 생성되었습니다.")