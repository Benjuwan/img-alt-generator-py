import os
import openpyxl


# 1. はじめに、モジュールの主要な処理を関数にまとめる
def create_xlsx_file(results=None):
    # 保存先ディレクトリとファイルパス
    save_dir = "../dist"
    save_path = os.path.join(save_dir, "img_lists.xlsx")

    # 当該ディレクトリがなければ作成
    # exist_ok=True とすると既に存在しているディレクトリを指定してもエラーにならない
    os.makedirs(save_dir, exist_ok=True)

    # ワークブックはExcelのブックに相当し、自動的にシートも生成される。
    img_lists_workbook = openpyxl.Workbook()

    # 操作対象ブック（オブジェクト）をアクティブにすることでセルの編集が行える
    img_lists_worksheet = img_lists_workbook.active

    # 読み込み：ワークシート[セル位置].value
    img_lists_worksheet["A1"] = "画像要素（img タグ）"
    img_lists_worksheet["B1"] = "Gemini が生成した alt文"

    if results is not None:
        for i, result in enumerate(results, 2):
            # 書き込み：ワークシート[セル位置] = 値
            img_lists_worksheet[f"A{i}"] = str(result["original_img"])
            img_lists_worksheet[f"B{i}"] = str(result["suggested_alt"])

        # 同名ファイルが存在する場合は上書き保存され、無い場合は新規作成となる。
        img_lists_workbook.save(save_path)

    else:
        print("エラー：引数 results が渡ってきていません")
        return


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    create_xlsx_file()
