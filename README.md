# img-alt-generator-py
指定したページの全画像データにおける`alt`タグの記述漏れをチェックします。<br>`alt`指定漏れの画像をPythonライブラリ（`pillow`）で生成して、それらをLLM（`Gemini`）に読み込ませて適切な`alt`タグを自動生成してもらう機能です。

## 技術構成
```bash
annotated-types              0.7.0
beautifulsoup4               4.13.4
cachetools                   5.5.2
certifi                      2025.4.26
charset-normalizer           3.4.2
colorama                     0.4.6
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
pillow                       11.2.1
pip                          25.1.1
proto-plus                   1.26.1
protobuf                     5.29.5
pyasn1                       0.6.1
pyasn1_modules               0.4.2
pydantic                     2.11.5
pydantic_core                2.33.2
pyparsing                    3.2.3
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

## `JavaScript`での`alt`タグ記述漏れチェックコード

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
"# img-alt-generator-py" 
