
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API 키 설정 (환경변수 사용)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/gpt", methods=["POST"])
def gpt_response():
    user_input = request.json.get("userRequest", {}).get("utterance", "")

    prompt = f"""당신은 초보 러너를 위한 따뜻하고 친절한 러닝 코치입니다.
    사용자의 질문에 대해 너무 길지 않게, 현실적인 조언을 주고,
    필요하다면 부상 예방이나 보강 운동 정보를 함께 주세요.

    사용자: {user_input}
    러닝 코치:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    answer = response.choices[0].message['content'].strip()

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": answer
                }
            }]
        }
    })

@app.route("/", methods=["GET"])
def root():
    return "RunMate Flask 서버 작동 중입니다! /gpt 경로로 POST 요청을 보내주세요."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
