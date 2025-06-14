# img-alt-generator-py

## 概要
コマンドライン引数に指定したページ内の全画像データの`alt`記述漏れをチェックします。<br>
`alt`指定漏れの画像を`pillow`ライブラリで生成して、それらをLLM（`Gemini`）に読み込ませて適切な`alt`文を自動生成してもらう機能です。<br>
最終結果として`openpyxl`ライブラリで「当該DOM要素（`img`）の文字列」と「AIが生成した`alt`文」をまとめたエクセルファイルを出力します。

## 使い方
1. ルートに`.env`ファイルを用意
2. 仮想環境を構築（初回のみ）または仮想環境を立ち上げる（初回以降）
    - 仮想環境をアクティベートすると以下のようなコマンド画面になります
```bash
# WindowsOS の場合
(仮想環境名) C:\~~~~\img-alt-generator-py\仮想環境ディレクトリ名>

# MacOS の場合
(仮想環境名) user-PC-name 仮想環境ディレクトリ名
```
3. `utils`ディレクトリへ移動して`check_img_alt.py`を実行

> [!NOTE]
> 本機能はWebスクレイピングします<br>
> 必ず自身が管理するサイトや関係するサイトでのみ行ってください<br>
> webスクレイピングは犯罪に該当するかもしれない迷惑行為なので対象サイト／ページは慎重に選んでください

### ルートに`.env`ファイルを用意
- `.env`
```bash
GOOGLE_API_KEY="発行した Geminiの APIキーを記述"
```

### 仮想環境を構築（初回のみ）
ターミナル／コマンドプロンプトを開いてルート（ファイルの最上階層）にいる状態で以下フローを実行
```bash
mkdir venv # venv ディレクトリ（仮想環境ディレクトリ）を作成
cd venv    # 作成した仮想環境ディレクトリ（`venv`）へ移動

# 新しい仮想環境を作成してアクティベート
# WindowsOS の場合: python -m venv env
python3 -m venv env # env{は仮想環境名}

# WindowsOS の場合: env\Scripts\activate
source env/bin/activate

# 仮想環境をアクティベートした状態で、パス指定して`requirements.txt`から各種ライブラリをインストール
# `../requirements.txt`なのは`requirements.txt`がルート直下にあるため
pip install -r ../requirements.txt 
```

### 仮想環境を立ち上げる（初回以降）
```bash
# 1. 仮想環境を格納しているディレクトリへ移動（存在しない場合は上記を参照に新規作成）
cd venv

# 2. 仮想環境をアクティベート
# WindowsOS の場合: env\Scripts\activate
source env/bin/activate
```

### `utils`ディレクトリへ移動して`check_img_alt.py`を実行
必ず**仮想環境をアクティベートした状態**で以下フローを実行
```bash
# ※必要に応じて以下コマンドを実行
# 仮想環境をアクティベートした直後だと`venv`ディレクトリへいるためルートに移動する
# cd ../

# `utils`ディレクトリへ移動
cd utils

# 解析したいWebページURLを`コマンドライン引数`に指定してファイルを実行
# WindowsOS の場合:
# python check_img_alt.py https://example.com/archive/items/index.html
python3 check_img_alt.py https://example.com/archive/items/index.html
```

## 技術構成
```bash
annotated-types              0.7.0
beautifulsoup4               4.13.4
cachetools                   5.5.2
certifi                      2025.4.26
charset-normalizer           3.4.2
colorama                     0.4.6
et_xmlfile                   2.0.0
google-ai-generativelanguage 0.6.15
google-api-core              2.25.0
google-api-python-client     2.170.0
google-auth                  2.40.2
google-auth-httplib2         0.2.0
google-generativeai          0.8.5
googleapis-common-protos     1.70.0
grpcio                       1.72.1
grpcio-status                1.71.0
httplib2                     0.22.0
idna                         3.10
openpyxl                     3.1.5
pillow                       11.2.1
pip                          25.1.1
proto-plus                   1.26.1
protobuf                     5.29.5
pyasn1                       0.6.1
pyasn1_modules               0.4.2
pydantic                     2.11.5
pydantic_core                2.33.2
pyparsing                    3.2.3
python-dotenv                1.1.0
requests                     2.32.3
rsa                          4.9.1
soupsieve                    2.7
tqdm                         4.67.1
typing_extensions            4.13.2
typing-inspection            0.4.1
uritemplate                  4.2.0
urllib3                      2.4.0
```

- `google-generativeai`<br>
Googleの公式Generative AIライブラリ
```bash
pip install google-generativeai
```

- [Gemini各モデルについて](https://ai.google.dev/gemini-api/docs/models?hl=ja&_gl=1*cf3ayb*_up*MQ..*_ga*MTAzMDk0MDk5OC4xNzQ5NTEyODU2*_ga_P1DBVKWT6V*czE3NDk1MTI4NTUkbzEkZzAkdDE3NDk1MTI5NTYkajYwJGwwJGg3MDY1NjM3MTE.)
- [レート制限について](https://ai.google.dev/gemini-api/docs/rate-limits?hl=ja&_gl=1*139atk2*_up*MQ..*_ga*MTAzMDk0MDk5OC4xNzQ5NTEyODU2*_ga_P1DBVKWT6V*czE3NDk1MTI4NTUkbzEkZzAkdDE3NDk1MTI4NTUkajYwJGwwJGg3MDY1NjM3MTE.#free-tier)

- `python-dotenv`<br>
秘匿情報ファイルを扱うための非標準ライブラリ
```bash
pip install python-dotenv
```

## `JavaScript`での`alt`記述漏れチェックコード

```js
const allImg = document.querySelectorAll('img');
for(const img of allImg){
    if(!img.getAttribute('alt') && img.getAttribute('alt').length === 0){
        console.log(img);
    }
}

/* img（DOM要素）の各種プロパティまでも把握するには以下 */
const allImg = document.querySelectorAll('img');
noAltImgs = Array.from(allImg).filter(img => img.alt.length === 0);
console.log(noAltImgs);
```
