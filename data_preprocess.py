import pandas as pd
import ast
import re

# CSV 파일 불러오기
df = pd.read_csv("responses.csv", encoding="utf-8")

# 분석에 불필요한 컬럼 드랍
drop_cols = ['phone', 'feedback', 'timestamp', 'doc_id', 'username']
df = df.drop(columns=drop_cols, errors='ignore')

# 문자열로 저장된 리스트를 실제 리스트로 변환
df['answers'] = df['answers'].apply(ast.literal_eval)

# answers 컬럼을 Q1~Q15로 분리
answers_df = pd.DataFrame(df['answers'].tolist(), columns=[f'Q{i+1}' for i in range(15)])

# 기존 df에서 answers 컬럼 제거 후 병합
df = df.drop(columns=['answers']).reset_index(drop=True)
df = pd.concat([df, answers_df], axis=1)

# age 컬럼에서 숫자만 추출
df['age'] = df['age'].apply(lambda x: int(re.search(r'\d+', x).group()))

print(df.info())

# 새로운 CSV로 저장
df.to_csv("processed_responses.csv", encoding="utf-8-sig",index=False)

print("'processed_responses.csv' 파일로 저장 완료")
