from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup

# CONTRIBUTORS: Antigravity - Full Backend Restoration

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Supabase Client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = None
try:
    if url and key:
        supabase = create_client(url, key)
    else:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not set.")
except Exception as e:
    print(f"Failed to initialize Supabase client: {e}")

def crawl_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        # Limit text length to avoid token limits (e.g., 3000 chars)
        return text[:3000]
    except Exception as e:
        print(f"Crawling failed: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        topic = data.get('topic')
        tone = data.get('tone', 'professional') 
        ref_url = data.get('url') # Get optional URL
        include_storyboard = data.get('storyboard', False) # Get optional Storyboard flag
        
        if not topic:
            return jsonify({'error': '토픽을 입력해주세요.'}), 400
            
        # Tone mapping
        tone_prompts = {
            'professional': '전문적이고 객관적인 어조로, 신뢰감 있게',
            'friendly': '친근하고 부드러운 대화체로(해요체 사용), 이해하기 쉽게',
            'witty': '유머러스하고 재치있는 표현을 섞어서, 흥미롭게',
            'emotional': '감성적이고 호소력 짙은 문체로, 독자의 공감을 이끌어내며'
        }
        
        selected_tone_prompt = tone_prompts.get(tone, tone_prompts['professional'])

        # Context from URL
        crawled_content = ""
        if ref_url:
            crawled_text = crawl_url(ref_url)
            if crawled_text:
                crawled_content = f"\n\n[참고 자료]\n{crawled_text}\n(위 참고 자료의 내용을 바탕으로 기사를 작성해주세요.)\n"

        # Storyboard Prompt Addition
        storyboard_prompt = ""
        if include_storyboard:
            storyboard_prompt = """
6. **영상/카드뉴스 스토리보드** (기사 작성 후 마지막에 추가)
   - 반드시 **HTML Table** 형식으로 작성해주세요.
   - 컬럼 구성: [순서 (No.)] | [장면 설명 (Visual)] | [대본/내레이션 (Script)]
   - 최소 5개 장면 이상 구성해주세요.
   - 테이블 스타일: `<table class="table table-bordered table-striped mt-4">...</table>`
            """

        # Simplified Prompt
        prompt = f"""다음 주제에 대한 기사 초안을 작성해주세요.
주제: {topic}
작성 스타일: {selected_tone_prompt}{crawled_content}

형식:
- 반드시 **HTML5 태그**를 사용하여 작성해주세요 (예: <h1>, <h2>, <p>, <ul>, <li>, <strong> 등).
- <html>, <head>, <body> 태그는 제외하고, 본문에 들어갈 내용만 작성해주세요.
- 마크다운 코드 블록(```html)으로 감싸지 말고 순수 HTML 코드만 반환하세요.

구성:
1. 제목 (<h1> 태그)
2. 도입부 (<p> 태그)
3. 본문 (최소 3개 문단, 각 소제목은 <h2> 사용)
4. 결론 (<p> 태그)
5. 요약 (<ul> 사용){storyboard_prompt}"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"당신은 {selected_tone_prompt} 글을 HTML 형식으로 작성하는 전문 콘텐츠 에디터입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Remove potential markdown wrapping just in case
        if content.startswith("```html"):
            content = content.replace("```html", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        # Save to Supabase
        if supabase:
            try:
                data = {
                    "topic": topic,
                    "tone": tone,
                    "content": content
                }
                supabase.table("generated_content").insert(data).execute()
            except Exception as db_error:
                print(f"Failed to save to Supabase: {db_error}")
                # We don't stop the response if saving fails, just log it.

        return jsonify({'result': content})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        if not supabase:
            return jsonify({'error': 'Supabase not connected'}), 503
            
        # Fetch articles sorted by creation time (newest first)
        response = supabase.table("generated_content").select("*").order("created_at", desc=True).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
