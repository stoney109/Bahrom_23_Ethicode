import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# 데이터 불러오기
df = pd.read_csv("processed_responses.csv", encoding="utf-8")

# 총 정답 수 컬럼 추가
df['total_correct'] = df[[f'Q{i+1}' for i in range(15)]].sum(axis=1)

### (1) 문항별 수치 ###
print("\n📌 (1) 문항별 정답률 (%)")
question_means = df[[f'Q{i+1}' for i in range(15)]].mean().round(4) * 100
print(question_means)

print("\n📌 (1) 문항별 정답 수 기준 평균/중앙값/표준편차")
question_stats = df[[f'Q{i+1}' for i in range(15)]].agg(['mean', 'median', 'std']).T.round(4)
question_stats['mean'] *= 100  # 백분율로 보기 좋게
print(question_stats)

### (2) 연령대별 수치 ###
# age_group 컬럼이 없을 경우, age로 구간 나눔 (예: 10대, 20대, ...)
if 'age_group' not in df.columns and 'age' in df.columns:
    bins = [0, 19, 29, 39, 49, 59, 100]
    labels = ['10대 이하', '20대', '30대', '40대', '50대', '60대 이상']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)

print("\n📌 (2) 연령대별 평균 정답 수")
age_correct = df.groupby('age_group', observed=True)['total_correct'].mean().round(2)
print(age_correct)

print("\n📌 (2) 연령대별 문항별 정답률 (%)")
age_q_means = df.groupby('age_group', observed=True)[[f'Q{i+1}' for i in range(15)]].mean().round(4) * 100
print(age_q_means)

### (3) 성별 수치 ###
print("\n📌 (3) 성별 평균 정답 수")
gender_correct = df.groupby('gender', observed=True)['total_correct'].mean().round(2)
print(gender_correct)

print("\n📌 (3) 성별 문항별 정답률 (%)")
gender_q_means = df.groupby('gender', observed=True)[[f'Q{i+1}' for i in range(15)]].mean().round(4) * 100
print(gender_q_means)

# 총점 컬럼이 없다면 생성
if 'total_correct' not in df.columns:
    df['total_correct'] = df[[f'Q{i+1}' for i in range(15)]].sum(axis=1)

# 정답 수 분포 출력
score_distribution = df['total_correct'].value_counts().sort_index()
print("📊 총점 분포 (정답 수별 인원 수):")
print(score_distribution)