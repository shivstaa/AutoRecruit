from typing import List, Dict

import openai


def chat(messages: List[Dict[str, str]], model: str, **kwargs):
    return openai.ChatCompletion.create(
        messages=messages,
        model=model,
        **kwargs
    )['choices'][0]['message']['content']


def call_openai(prompt: str):
    for _ in range(3):  # Attempt up to 3 times
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a seasoned recruiter."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print("An error occurred:", str(e))
            time.sleep(20)
    return None
