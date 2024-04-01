import json
from typing import Union
from fastapi import FastAPI, Request
from openai import OpenAI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")


client = OpenAI()


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root(request: Request, word: Union[str, None] = None):

    if word:

        response = client.chat.completions.create(
            temperature=0.66,
            max_tokens=4096,
            model="gpt-4-turbo-preview",
            # model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {
                    "role": "system",
                    "content": "あなたはユーザーが与えてきた単語・熟語に、関連する単語・熟語を返します。",
                },
                {
                    "role": "system",
                    "content": "返答の形式はJSONで、配列の中に「関連する単語・熟語(英訳)」、「どのように関連しているか」、「その語の説明(100字程度)」を入れ込みます。個数は12〜14個程度が望ましいです。配列の先頭には、もとの単語の情報を入れてください。",
                },
                {"role": "user", "content": "明るい"},
                {
                    "role": "assistant",
                    "content": """{'data':[
                        {'word': '明るい(Bright)', 'reason': '元の単語', 'description': '光量の多い状態を指す'},
                        {'word': '暗い(Dark)', 'reason': '反対語', 'description': '光量の少ない状態を指す'}, 
                        {'word': '明るさ(Brightness)', 'reason': '関連語', 'description': '明るい状態であること'}, 
                    ]}""",
                },
                {"role": "user", "content": word},
            ],
        )

        resp = response.choices[0].message.content
        j_resp = json.loads(resp)
        print(word, j_resp["data"])

    # j_respがdictかどうかチェックする
    if "j_resp" in locals() and isinstance(j_resp, dict):
        print("dictです")
        return templates.TemplateResponse(
            "root.html", {"request": request, "response": j_resp["data"]}
        )
    else:
        return templates.TemplateResponse(
            "root.html", {"request": request, "response": []}
        )


@app.get("/ads.txt")
def read_ads():
    with open("static/ads.txt", "r") as f:
        return f.read()
