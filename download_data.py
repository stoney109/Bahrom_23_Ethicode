import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# 서비스 계정 키로 초기화
cred = credentials.Certificate("ethicode-quiz-firebase-adminsdk-fbsvc-b8b4a91728.json")
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 생성
db = firestore.client()

# 'responses' 컬렉션 불러오기
docs = db.collection('responses').stream()

# 데이터 정리
data = []
for doc in docs:
    entry = doc.to_dict()
    entry['doc_id'] = doc.id
    data.append(entry)

# 데이터프레임으로 변환 후 저장
df = pd.DataFrame(data)
df.to_csv("responses.csv", index=False, encoding='utf-8-sig')

print("응답 데이터가 responses.csv로 저장되었습니다.")
