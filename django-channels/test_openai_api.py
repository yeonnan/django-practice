import openai
from djangoChannels import config

openai.api_key = config.OPENAI_API_KEY

# 첫 번째 작업 : 문법 수정
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant that corrects grammar.'},
        {'role': 'user', 'content': '''
Fix grammar errors:
    - I is a boy
    - You is a girl
        '''.strip()}
    ]
)

# 결과 출력
print(response)
print(response['choices'][0]['message']['content'])

# 두 번째 작업 : 질문
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'system', 'content': '당신은 지식이 풍부한 도우미입니다.'},
        {'role': 'user', 'content': '세계에서 가장 큰 도시는 어디인가요?'}
    ]
)

# 결과 출력
print(response)
print(response['choices'][0]['message']['content'])