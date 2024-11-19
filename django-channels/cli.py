import os
from io import BytesIO
from tempfile import NamedTemporaryFile
import openai
import pygame
from gtts import gTTS
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')


# 상황극 설정
language = 'English'
gpt_name = 'Steve'
level_string = f'a beginner in {language}'
level_word = 'simple'
situation_en = 'make new friends'
my_role_en = 'me'
gpt_role_en = 'new friend'

SYSTEM_PROMPT = (
    f'You are helpful assistant supporting people learning {language}.'
    f'Your name is {gpt_name}. Please assume that the user you are assisting'
    f'is {level_string}. And please write only the sentence without'
    f'the character role.'
)

USER_PROMPT = (
    f"Let's have a conversation in {language}. Please answer in {language} only "
    f"without providing a translation. And please don't write down the "
    f"pronunciation either. Let us assume that the situation in '{situation_en}'. "
    f"I am {my_role_en}. The character I want you to act as is {gpt_role_en}. "
    f"Please make sure that "
    f"I'm {level_string}, so please use {level_word} words as much as possible. "
    f"Now, start a conversation with the first sentence!"
)

RECOMMEND_PROMPT = (
    f"Can you please provide me an {level_word} example"
    f"of how to respond to the last sentence"
    f"in this situation, without providing a translation"
    f"and any introductory phrases or sentences."
)


# 대화 내역 누적 리스트
message = [
    {'role' : 'system', 'content' : SYSTEM_PROMPT} 
]


def gpt_query(user_query : str, skip_save : bool = False) -> str:
    '유저 메세지에 대한 응답을 반환합니다.'

    global message

    message.append({
        'role' : 'user',
        'content' : user_query,
    })

    response = openai.ChatCompletion.create(
        model = 'gpt-4o',
        messages = message,     # messages인자에 전역변수 message를 받는다.
    )
    assistant_message = response['choices'][0]['message']['content']

    if skip_save is False:
        message.append({
            'role' : 'assistant',
            'content' : assistant_message,
        })

    return assistant_message


def play_file(file_path : str) -> None:
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.quit()


def say(message : str, lang : str) -> None:
    io = BytesIO()
    gTTS(message, lang=lang).write_to_fp(io)

    with NamedTemporaryFile() as f:
        f.write(io.getvalue())
        play_file(f.name)


def main():
    assistant_message = gpt_query(USER_PROMPT)
    print(f'[assistant] {assistant_message}')

    while line := input('[user] ').strip():
        if line == '!recommend':
            recommend_message = gpt_query(RECOMMEND_PROMPT, skip_save=True)
            print('추천 표현 : ', recommend_message)
        elif line == '!say':
            say(message[-1]['content'], 'en')
        else:
            response = gpt_query(line)
            print(f'[assistant] {response}')


# cli.py 파일을 시작으로 파이썬 프로그램이 구동되면 main 함수가 호출
if __name__ == '__main__':
    main()