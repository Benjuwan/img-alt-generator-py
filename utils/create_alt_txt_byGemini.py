import google.generativeai as genai  # Google Gemini API用ライブラリ
from urllib.parse import urljoin  # URLの結合・正規化
import requests  # Webページからコンテンツ（情報）を取得
from PIL import Image  # 画像処理用ライブラリ（Pillow）
from io import BytesIO  # バイナリデータをファイルのように扱う
from dotenv import load_dotenv  # .envファイルから環境変数を読み込む
import os  # OSの環境変数操作用


# Gemini APIの設定
load_dotenv()  # ローカルの .env ファイルから環境変数（秘匿情報など）を読み込んで、os.environ で参照できるようにする関数
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")  # より詳細な画像認識を重視する場合
# model = genai.GenerativeModel("gemini-1.5-flash")  # 処理速度を重視する場合


# Gemini への処理要求
def _request_Gemini(img: str, img_url: str, results: list):
    response = requests.get(img_url)

    if response.status_code != 200:
        print(f"レスポンスエラー：status-[{response.status_code}]\n{img}")
        return

    # レスポンス内容をバイナリデータ化して画像データとして出力（開く）
    image = Image.open(BytesIO(response.content))

    # Geminiに画像を解析してもらう
    response = model.generate_content(
        [
            """
            ## タスク
            あなたはSEOの知見が豊富なエージェントです。この画像の内容を alt属性として最適な文章となるよう日本語で生成してください

            ## 条件
            装飾系やパターン、テクスチャなどデザイン要素としての画像である場合は空文字（""）を返してください
            """,
            image,
        ]
    )

    suggested_alt = response.text
    # dict 形式でリストに格納
    results.append({"original_img": img, "suggested_alt": suggested_alt})


# 1. はじめに、モジュールの主要な処理を関数にまとめる
# 実引数は呼び出し元で指定するので、仮引数としてオプショナルな指定（None）に留めておく
def create_alt_txt_byGemini(
    img_list: list | None = None, target_site: str | None = None
):
    results: list[str] = []

    if img_list is None or target_site is None:
        return

    for img in img_list:
        try:
            # 画像URLを取得して正規化
            img_url: str = img.get("src")

            if img_url is None:
                return

            # 相対パス判定フラグ
            is_not_absolute_pass = img_url.count("../") > 0
            # 文字列が"/"開始かどうかの判定フラグ
            is_not_startWith_scheme = img_url.startswith("/") is False

            if is_not_absolute_pass or is_not_startWith_scheme:
                # urljoinを使用して相対パス（'../'）を解決
                img_url = urljoin(target_site, img_url)
                # print(f"true : {img_url}")  # デバック用

            # print(f"false: {img_url}")  # デバック用

            # Gemini への処理要求
            _request_Gemini(img, img_url, results)

        # Exception：大部分の例外の基底クラス
        except Exception as e:
            print(f"エラーが発生しました | create_alt_txt_byGemini.py : {e}")
            continue

    return results


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    create_alt_txt_byGemini()
