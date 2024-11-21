import os
import requests

#ファイルの内容を読み取ってテキストデータを返す
def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {file_path} が見つかりません。")
        return None

def get_gas_api_url():
    return os.getenv("GAS_API_URL", "https://script.google.com/macros/s/AKfycby4pLoT16FMfFwkHQAzrhQnwxzdCUQT9sf4aTVTlah-U__eCithqzwsSDTQPf0rnJlQJg/exec")
#GASのグーグル翻訳APIのURLを環境変数または外部設定ファイルに保存し、そこから読み取るようにする


def translate_text_with_gas(text, source_lang='en', target_lang='ja'):
    GAS_API_URL = get_gas_api_url()
    
    params = {
        'text': text,
        'source': source_lang,
        'target': target_lang
    }
    
    try:
        response = requests.get(GAS_API_URL, params=params)
        if response.status_code == 200:
            result = response.json()
            if 'text' in result:
                return result['text']
            else:
                print("Unexpected response format:", result)
                return None
        else:
            print(f"Error: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None
    #エラーハンドリング

if __name__ == "__main__":
    file_content = read_file("transcription.txt")
    if file_content:
        translated_text = translate_text_with_gas(file_content, source_lang='en', target_lang='ja')
        print("翻訳結果:")
        print(translated_text)
    else:
        print("文字起こしファイルが見つかりません。lyrics.pyを実行して文字起こしを行ってください。")
#エラーメッセージをif __name__ == "__main__"のelse文ではなくファイル読み取り部分に統合する