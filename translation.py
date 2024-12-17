import os
import requests
import asyncio
import language_tool_python
from concurrent.futures import ThreadPoolExecutor

# GASの公開URL
GAS_API_URL = "https://script.google.com/macros/s/AKfycbzV_jDirFRmldR9VAaQDLBmTsnpLLiSnV9bb3zPqxnYoak2sn4FgXF_EaetwpOafTsCJw/exec"

def call_translation_api(text, target_lang="ja"):
    params = {"text": text, "targetLanguage": target_lang}  # targetLang -> targetLanguage
    response = requests.get(GAS_API_URL, params=params)
    print("APIレスポンス内容:", response.text)  # レスポンス内容を表示

    if response.status_code == 200:
        if response.text.strip():  # 空のレスポンスを確認
            try:
                response_data = response.json()  # JSONに変換
                translated_text = response_data.get("translated")
                return translated_text
            except ValueError:
                return "JSON解析エラー: レスポンスが正しいJSONではありません"
        else:
            return "APIが空のレスポンスを返しました"
    else:
        return f"APIエラー {response.status_code}: {response.text}"



# 非同期に翻訳タスクを実行する関数
async def process_translation_async(texts, target_lang="ja"):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as executor:
        # 非同期で複数の翻訳タスクを並行実行
        tasks = [loop.run_in_executor(executor, call_translation_api, text, target_lang) for text in texts]
        results = await asyncio.gather(*tasks)
    return results

# ファイルの内容を読み取ってテキストデータを返す
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()  # 複数行をリストとして返す
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: {file_path} が見つかりません。文字起こしファイルを準備してください。")

# 文法修正
def correct_grammar(text):
    tool = language_tool_python.LanguageTool('ja')
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# メイン処理
if __name__ == "__main__":
    transcription_file = "transcription.txt"
    try:
        # ファイルを読み取り
        file_content = read_file(transcription_file)

        if file_content:
            print("翻訳中...")
            # 非同期翻訳タスクの実行
            translated_texts = asyncio.run(process_translation_async(file_content, target_lang="ja"))
            
            # 文法修正
            print("文法修正中...")
            corrected_texts = [correct_grammar(text) for text in translated_texts]
            
            # 結果表示
            print("\n翻訳結果:")
            for corrected_text in corrected_texts:
                print(corrected_text)
        else:
            print("ファイルが空です。")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
