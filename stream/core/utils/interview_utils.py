import time
from typing import List, Dict

import openai

from .chat_utils import chat


def interview_reply(
    role: str, job_description: str, company: str,
    resume: str, name: str,
    interview_so_far: List[Dict[str, str]], 
    n: int, 
    model: str
):
    messages = [
        {"role": "system", "content": f"""You are an interviewer, conducting behavioral interviews to select the most skilled and well-rounded candidates for the role of {role} at {company}. You generate interview questions given a job description, the resume of an interviewee to that job, and the interview so far. Read carefully the job description and associated resume, as well as the instructions that follow. However, note that you are the expert of the interview process, so the following should be taken as guidelines, not as strict rules.

        Job Description:
        \"\"\"
        {job_description}
        \"\"\"

        {name}'s Resume:
        \"\"\"
        {resume}
        \"\"\"

        This interview will last ~{n} minutes.

        A few notes to help you find avenues of discussion:
        - You may compare the resume to the job description to see if the interviewee has the necessary skills. If they do not, you may ask them about it, and about what they wish to do to remedy the situation.
        - You should visit these 4 major areas of discussion: experience, skills, values, and personality.
        """},
    ]
    messages += interview_so_far

    return chat(
        messages=messages,
        model=model,
    )
