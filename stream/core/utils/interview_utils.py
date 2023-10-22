import os
import time
from typing import List, Dict, Generator
from dotenv import load_dotenv
from threading import Thread
import queue

import openai
from elevenlabs import set_api_key, generate, stream

from chat_utils import chat_stream

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
set_api_key(os.getenv('ELEVENLABS_API_KEY'))


class AudioBuffer:
    def __init__(self):
        self.buffer = queue.Queue(maxsize=3)  # Adjust the buffer size as needed

    def add_audio(self, audio):
        self.buffer.put(audio, block=True)

    def get_audio(self):
        return self.buffer.get(block=True)


class InterviewerVoice:
    def __init__(self, tts_engine):
        self.tts_engine = tts_engine
        self.audio_buffer = AudioBuffer()

    def pre_fetch_audio(self, text_stream: Generator[str, None, None]):
        for text_chunk in text_stream:
            self.tts_engine.pre_fetch(text_chunk, self.audio_buffer)

    def speak_stream(self, text_stream: Generator[str, None, None]):
        start_time = time.time()
        pre_fetch_thread = Thread(target=self.pre_fetch_audio, args=(text_stream,))
        pre_fetch_thread.start()
        
        while pre_fetch_thread.is_alive() or not self.audio_buffer.buffer.empty():
            audio = self.audio_buffer.get_audio()
            stream(audio)
        end_time = time.time()
        print(f"Total Time for Speaking: {end_time - start_time:.4f} seconds")


class ElevenLabsTTS:
    def __init__(self, voice_id: str, model: str = "eleven_monolingual_v1"):
        self.voice_id = voice_id
        self.model = model
        self.partial_sentence = ""

    def pre_fetch(self, text_chunk: str, audio_buffer: AudioBuffer, voice_id: str = None):
        self.partial_sentence += text_chunk
        if self.partial_sentence.endswith('.'):
            start_time = time.time()
            audio = generate(
                text=self.partial_sentence.strip(),
                voice=voice_id or self.voice_id,
                model=self.model,
                stream=True,
            )
            end_time = time.time()
            print(f"Time for Audio Generation: {end_time - start_time:.4f} seconds")
            audio_buffer.add_audio(audio)
            print(f"Speaking: {self.partial_sentence}")
            self.partial_sentence = ""


def interview_reply(
    role: str, job_description: str, company: str,
    resume: str, name: str,
    interview_so_far: List[Dict[str, str]], 
    n: int, 
    model: str,
    tts_engine: ElevenLabsTTS
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
        - You should visit these 4 major areas of discussion:
            - experience
            - skills
            - values
            - personality
        """},
    ]
    messages += interview_so_far

    start_time = time.time()
    text_stream = chat_stream(
        messages=messages,
        model=model,
    )
    end_time = time.time()
    print(f"Time for Text Generation: {end_time - start_time:.4f} seconds")
    
    voice = InterviewerVoice(tts_engine)
    voice.speak_stream(text_stream)


if __name__ == "__main__":
    role = "Software Engineer"

    job_description = """
    The Automated Workflows are the core platform feature that helps customers to automate their mundane tasks. Smartsheet supports workflows to notify when a change occurs in a sheet, auto-assign, setup dates, update/clear data and generate documents (PDF/Docusign). Our customers created millions of workflows and we execute tens of millions of workflows every day. We observed around 2x increase in workflow executions every year with improved performance. Come join us to strengthen the platform to support the exponential growth and adding new features to the workflows.

    In 2005, Smartsheet was founded on the idea that teams and millions of people worldwide deserve a better way to deliver their very best work. Today, we deliver a leading cloud-based platform for work execution, empowering organizations to plan, capture, track, automate, and report on work at scale, resulting in more efficient processes and better business outcomes.

    This position will report to our Senior Engineering Manager and can be based remotely from anywhere within the United States where Smartsheet is a registered employer.

    Our team focuses on distributed decision making that rewards ownership, transparency, and collaboration. Learn more about our platform here: Smartsheet Overview Video

    You Will:

        Build scalable back-end services for the next generation of applications at Smartsheet (Kotlin, Java)
        Solve challenging distributed systems problems and work with modern cloud infrastructure (AWS, Kubernetes)
        Take part in code reviews and architectural discussions as you work with other software engineers and product managers
        Mentor junior engineers on code quality and other industry best practices
        Forge a strong partnership with product management and other key areas of the business

    You Have:

        2+ years software development experience building highly scalable, highly available applications
        2+ years of programming experience with full stack technologies such Java, Kotlin or TypeScript
        2+ years Infrastructure management (Terraform, Terragrunt or Pulumi)
        2+ years of experience with cloud technologies (AWS, Azure, etc.)
        Experience developing, documenting, and supporting REST APIs
        Front-end development experience is plus (React, JavaScript, VueJS or Angular)
        A degree in Computer Science, Engineering, or a related field or equivalent practical experience
        Legally eligible to work in the U.S. on an ongoing basis

    Perks & Benefits:

        HSA, 100% employer-paid premiums, or buy-up medical/vision and dental coverage options for full-time employees
        Equity - Restricted Stock Units (RSUs) with all offers
        Lucrative Employee Stock Purchase Program (15% discount)
        401k Match to help you save for your future (50% of your contribution up to the first 6% of your eligible pay)
        Monthly stipend to support your work and productivity
        Flexible Time Away Program, plus Incidental Sick Leave
        Up to 24 weeks of Parental Leave
        Personal paid Volunteer Day to support our community
        Opportunities for professional growth and development including access to LinkedIn Learning online courses
        Company Funded Perks, including a counseling membership, local retail discounts, and your own personal Smartsheet account
        Teleworking options from any registered location in the U.S. (role specific) 
        US employees are automatically covered under Smartsheet-sponsored life insurance, short-term, and long-term disability plans
        US employees receive 12 paid holidays per year

    Smartsheet provides a competitive range of compensation for roles that may be hired in different geographic areas we are licensed to operate our business from. Actual compensation is determined by several factors including, but not limited to, level of professional, educational experience, skills, and specific candidate location. In addition, this role will be eligible for a market competitive bonus and RSU stock grant upon accepted offer. California & New York: $124,200 to $180,900 | All other US States: $115,000 to $167,500

    Equal Opportunity Employer:

    Smartsheet is an Equal Opportunity Employer committed to fostering an inclusive environment with the best employees. We provide employment opportunities without regard to any legally protected status in accordance with applicable laws in the US, UK, Germany, Costa Rica, Japan and Australia. If there are preparations we can make to help ensure you have a comfortable and positive interview experience, please let us know.

    At Smartsheet, we strive to build an inclusive environment that encourages, supports, and celebrates the diverse voices of our team members who also represent the diverse needs of our customers. We’re looking for people who are driven, authentic, supportive, effective, and honest. You’re encouraged to apply even if your experience doesn’t precisely match our job description—if your career path has been nontraditional, that will set you apart. At Smartsheet, we welcome diverse perspectives and people who aren’t afraid to be innovative—join us! 
    """

    company = "Google"

    resume = """
    Shubh Khandelwal
    Full-Stack Software Engineer | Python, JS, Java | ML/AI/NLP Enthusiast
    shubhvk10@gmail.com ·(602) 380-5667 ·linkedin.com/in/shubhk7 ·github.com/caffeinelover1012
    Education
    Arizona State University, Tempe, AZ Aug 2020 - May 2024
    BS in Computer Science (Dean’s List Recipient) GPA: 4.00
    Relevant Coursework: Data Structures and Algorithms, Object Oriented Programming, Operating Systems,
    Database Management, Principles of Programming, Advanced Physics (UGTA), Advanced Machine Learning
    Professional Experience
    Full-Stack Software Engineering Intern Bellevue, WA
    Smartsheet Inc. ·Licensing and Payments team May 2023 - Aug 2023
    •Developed 30+ REST API SaaS architecture services using Java, Javascript, Spring Boot, MySQL,
    DynamoDB, Maven, ReactJS, NodeJS, Docker and Ansible to support multi-line item subscriptions.
    •Engineered a serverless architecture using AWS Cloudwatch, ECS, Lambda, SQS and SES to automate email
    notifications for Seamless Trial Evaluations, resulting in a scalable and cost-efficient solution.
    •Provisioned AWS instances using Terraform, Terragrunt and Docker. Wrote JUnit tests and integration tests
    to improve library automated test coverage by 87%. Configured the Lingoport Globalyzer and CI/CD
    pipelines in 8 Git repositories to promote internationalization and generate i18n reports.
    Software Developer Intern Tempe, AZ
    School of Earth and Space Exploration ·ASU Apr 2022 - Jan 2023
    •Developed and maintained software applications for the MARS-2020 MastCam-Z NASA space mission
    operations using Python automation scripting, Django, Linux MakeFiles, jQuery, PostgreSQL.
    •Implemented a new search portal to display the sequences, images, and observations data captured by the
    Mars Rover and a caching mechanism resulting in a 90%reduction in search time.
    CTO and Co-founder MP, India
    Infocard Apr 2022 - Present
    •Co-founded Infocard, an NFC digital business card startup, which elevates the networking capabilities of
    professionals. Led the design and development of the platform using technologies like MongoDB, Express.js,
    React, Node.js, Redux and Bootstrap. Serving over 700+infocard users worldwide.
    Machine Learning Research Assistant Mesa, AZ
    W.P. Carey Morrison School of Agribusiness ·ASU Jan 2023 - Present
    •Working with Prof. Lauren Chenarides to create DIFA, a comprehensive data catalog tool that provides
    dataset-specific information, elevating the research capabilities of agricultural and applied economists.
    •Leveraging Machine Learning, Named Entity Recognition, NLP using Spacy and TensorFlow for dataset
    detection and Neo4j Graph DB for computation of linkage metrics using a knowledge graph.
    •Created Python web scrapers for 200+datasets using Selenium and a Full-Stack Web App and REST APIs
    using Django to display the knowledge graphs. Deployed with auto-scaling on AWS EC2.
    Projects
    Sentiment Analysis as a Service ·NLP, NLTK, Django, Heroku GitHub
    •Leveraged Natural Language Processing to analyze text, tokenize words and compute the sentiment score.
    •Developed REST APIs and a web application using Django to provide access to the analysis results.
    Worksheet Wizard ·Flask, React, SQLite, Cohere LLM Devpost
    •An innovative AI-powered educational platform, for UCLA Hackathon; the platform automatically generates
    custom worksheets from diverse multimedia content, utilizing Python, Flask, Cohere API, and NLP.
    Zuckbook ·Flask, MySQL, Bootstrap
    •A comprehensive Instagram clone, leveraging Flask and MySQL for the management and storage of user data,
    photo data, and other essential platform information.
    Certifications and Leadership Involvement
    Technical Officer ·Software Developer Association of ASU Jan 2023 - Present
    •Managing an organization with 2200+ members as a Technical Officer, leading technical presentations on
    Python Automation, Machine Learning, Git and Modern Tech Stacks within the industry.
    AWS Certified Cloud Practitioner Aug 2022
    Technical Skills
    Languages: Python, Java, JavaScript, HTML, CSS, C/C++, C#, SQL, Dart
    Tools/Frameworks: Django, Flask, Node.js, React, Spring, Linux, MVC, Bootstrap, jQuery, AJAX
    DB: PostgreSQL, MySQL, SQLite, ORMs, Redis, MongoDB, DynamoDB
    DevOps: JUnit, Agile, Scrum, Maven, Git, REST APIs, Ansible, Jira, Docker
    """

    name = "Shubh"

    interview_so_far = []

    n = 10

    model = "gpt-3.5-turbo"

    tts_engine = ElevenLabsTTS("21m00Tcm4TlvDq8ikWAM")
    interview_reply(
        role=role,
        job_description=job_description,
        company=company,
        resume=resume,
        name=name,
        interview_so_far=interview_so_far,
        n=n,
        model=model,
        tts_engine=tts_engine,
    )
