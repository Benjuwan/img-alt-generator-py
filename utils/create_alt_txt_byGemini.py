import google.generativeai as genai  # Google Gemini API用ライブラリ
from urllib.parse import urljoin  # URLの結合・正規化
from urllib.parse import urlparse  # URLの解析
from tqdm import tqdm  # プログレスバーを表示するための非標準ライブラリ
import requests  # Webページからコンテンツ（情報）を取得
from PIL import Image  # 画像処理用ライブラリ（Pillow）
from io import BytesIO  # バイナリデータをファイルのように扱う
from dotenv import load_dotenv  # .envファイルから環境変数を読み込む
import os  # OSの環境変数操作用


# Gemini APIの設定
load_dotenv()  # ローカルの .env ファイルから環境変数（秘匿情報など）を読み込んで、os.environ で参照できるようにする関数
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


# Gemini への処理要求
def _request_Gemini(img: str, img_url: str, results: list[dict]) -> None:
    try:
        response = requests.get(img_url)

        # レスポンス判定
        if response.status_code != 200:
            print(f"レスポンスエラー：status-[{response.status_code}]\n{img}")
            return

        # 画像形式の検証
        if not response.headers.get("content-type", "").startswith("image/"):
            print(f"画像ファイルではありません: {img_url}")
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

        # strip() で文字列・文章前後の空白をトリミングし、改行を。に置換する
        suggested_alt = response.text.strip().replace("\n", "。")
        # dict 形式でリストに格納
        results.append({"original_img": img, "suggested_alt": suggested_alt})

    except Exception as e:
        print(f"Gemini の解析時にエラーが発生 | _request_Gemini : {e}")
        return


# 1. はじめに、モジュールの主要な処理を関数にまとめる
# 実引数は呼び出し元で指定するので、仮引数としてオプショナルな指定（None）に留めておく
def create_alt_txt_byGemini(
    img_list: list | None = None, target_site: str | None = None
):
    results: list[dict] = []

    if img_list is None or target_site is None:
        return

    for img in tqdm(img_list, desc="画像を処理中"):
        try:
            # 画像URLを取得して正規化
            img_url: str = img.get("src")

            if img_url is None:
                continue

            # URLスキーム（http:// や https:// など）の有無をチェック
            # `urlparse(img_url).scheme`はスキーム（プロトコル）がある場合はそのスキーム名を、無い場合は空文字を返す
            if not urlparse(img_url).scheme:
                # スキームが無い（適切なURL記述でない）場合は空文字が返ってくるので`img_url`は相対パスとなり、
                # それを`urljoin`で`target_site`を基準とした絶対パスに変換する
                img_url = urljoin(target_site, img_url)

            # Gemini への処理要求
            _request_Gemini(img, img_url, results)

        # Exception：大部分の例外の基底クラス
        except Exception as e:
            print(f"{img} 画像を処理中にエラーが発生 | create_alt_txt_byGemini : {e}")
            continue

    return results


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    create_alt_txt_byGemini()
