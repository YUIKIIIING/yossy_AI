import requests
from lyrics import process_youtube_audio

def translate_text_with_gas(text, source_lang='en', target_lang='ja'):
    # Google Apps ScriptのデプロイURL
    GAS_API_URL = "https://script.google.com/macros/s/AKfycby4pLoT16FMfFwkHQAzrhQnwxzdCUQT9sf4aTVTlah-U__eCithqzwsSDTQPf0rnJlQJg/exec"
    
    # パラメータを設定
    params = {
        'text': text,
        'source': source_lang,
        'target': target_lang
    }
    
    try:
        # APIにリクエストを送信
        response = requests.get(GAS_API_URL, params=params)
        
        # ステータスコードが200の場合、翻訳結果を取得
        if response.status_code == 200:
            result = response.json()
            return result['text']
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

# テスト用
if __name__ == "__main__":
    # 英語から日本語に翻訳
    translated_text = translate_text_with_gas(process_youtube_audio, source_lang='en', target_lang='ja')
    print("翻訳結果:")
    print(translated_text)