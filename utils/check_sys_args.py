import sys  # コマンドライン引数を扱う


# URLパスをチェックするプライベートメソッド
def _check_url_path(target_url):
    # print(target_url[0])
    has_http = "http" in target_url[0]
    has_https = "https" in target_url[0]
    has_slash = "/" in target_url[0]
    if has_http or has_https or has_slash:
        return target_url[0]

    sys.exit("URLを指定してください")


# 1. はじめに、モジュールの主要な処理を関数にまとめる
def check_sys_args():
    if len(sys.argv) != 2:
        # （コマンドライン引数が1つでない場合は）引数に指定した文字列を表示して処理終了
        this_filename = sys.argv[0]  # 先頭（1つ目）はファイル名
        sys.exit(
            f"'{this_filename}'に必要な引数は「1つ」ですが、指定された引数は「{len(sys.argv) - 1 if len(sys.argv) == 1 else len(sys.argv)}つ」です"
        )

    # コマンドライン引数が1つの場合（正常処理パターン）
    except_filename_args = sys.argv[1:]  # 先頭以外の全ての引数

    target_site = _check_url_path(except_filename_args)

    return target_site


# 2. モジュールを単独で（Pythonコマンドで）実行したときに関数を呼び出す処理を追加
if __name__ == "__main__":
    check_sys_args()
