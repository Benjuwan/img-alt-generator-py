import requests  # 指定したWebページからコンテンツ（情報）を取得
from bs4 import BeautifulSoup  # 取得したwebページの各コンテンツをHTML解析

# 独自モジュール（コマンドライン引数をチェック）
from check_sys_args import check_sys_args

# 独自モジュール（Gemini による画像チェック及び altテキストの生成）
from create_alt_txt_byGemini import create_alt_txt_byGemini

# 独自モジュール（画像パスと、Gemini が生成した altテキストをエクセルファイルに保存）
from create_xlsx_file import create_xlsx_file

target_site = check_sys_args()

# 指定したWebページからコンテンツ（情報）を取得
res = requests.get(target_site)
res.encoding = res.apparent_encoding

# 取得したwebページの各コンテンツをHTML解析
soup = BeautifulSoup(res.text, "html.parser")


# check_img_alt： 指定したWebページ内における alt属性が指定されていない画像に適切な altテキストを生成する関数
def check_img_alt():
    images = []

    for imgs in soup.find_all("img"):
        # 指定したwebページ内の img 要素の alt属性をチェック
        # .get()：引数に指定した属性名の有無を取得（無い場合はNone）
        img_alt = imgs.get("alt")

        # 対象画像が alt属性を持っていて、1文字以上指定されている場合は処理スキップ
        if img_alt is not None and len(img_alt) > 0:
            continue

        images.append(imgs)

    if len(images) > 0:
        results = create_alt_txt_byGemini(images, target_site)
        create_xlsx_file(results=results)
        print("すべての処理が完了しました")

    else:
        print(f"{target_site}内の画像データの alt属性は全て記入されています")


check_img_alt()
