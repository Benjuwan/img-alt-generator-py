import google.generativeai as genai
from urllib.parse import urljoin
import requests
from PIL import Image
from io import BytesIO


# Gemini APIの設定
GOOGLE_API_KEY = 'Your Gemini API-KEY'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


# 1. はじめに、モジュールの主要な処理を関数にまとめる
# 実引数は呼び出し元で指定するので、仮引数としてオプショナルな指定（None）に留めておく
def create_alt_txt_byGemini(img_list = None, target_site = None):
    results = []
    
    for img in img_list:
        try:
        # 画像URLを取得して正規化
            img_url = img.get('src')

            if img_url:
                # urljoinを使用して相対パス（'../'）を解決
                img_url = urljoin(target_site, img_url)

            response = requests.get(img_url)
            # レスポンス内容をバイナリデータ化して画像データとして出力（開く）
            image = Image.open(BytesIO(response.content))
            
            # Geminiに画像を解析してもらう
            response = model.generate_content([
                """
                ## タスク
                この画像の内容を alt属性として適切な文章となるよう日本語で生成してください。

                ## 条件
                装飾系やパターン、テクスチャなどデザイン要素としての画像である場合は空文字（""）を返してください
                """,
                image
            ])
            
            suggested_alt = response.text
            # dictd 形式でリストに格納
            results.append({
                'original_img': img,
                'suggested_alt': suggested_alt
            })
            
        # Exception：大部分の例外の基底クラス
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            continue
    
    return results


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    create_alt_txt_byGemini()
