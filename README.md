# しそら

「しそら」は、入力された語句に関連した語句を AI が教えてくれる Web アプリです。

関連語句から関連語句へと、ネットサーフィンのように遷移していけるのが特徴です。

## 使用法

ターミナルにて`pip install -r requirements.txt`で、必要なライブラリをインストールしてください。

OPENAI の API キーを取得し、環境変数に設定してください。`export OPENAI_API_KEY=sk-xxxxxxxxxxx`

ターミナルにて、作業フォルダ内で`uvicorn main:app --reload`を実行してください。

**http://127.0.0.1:8000** にアクセスしてください。
