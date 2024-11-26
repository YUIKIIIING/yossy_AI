from google.cloud import texttospeech
import playsound  # 再生用にインストール: pip install playsound
import os
import re

# Google Cloudの認証情報を設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\YUIKIIIING\\Downloads\\geeksalon-441211-4622fab85300.json"

# 短縮形のリストを定義（これにより、分割せずにそのまま読む）
CONTRACTIONS = [
    "I'm", "I've", "I'd", "I'll", "I'am", "we're", "we've", "we'll", "you're", "you've", "you'll", "he's", "he've", "he'll",
    "she's", "she've", "she'll", "it's", "it've", "it'll", "they're", "they've", "they'll", "that's", "who's", "what's",
    "where's", "how's", "don't", "doesn't", "didn't", "can't", "couldn't", "won't", "wouldn't", "isn't", "aren't", "wasn't",
    "weren't", "haven't", "hasn't", "hadn't", "shouldn't", "mustn't", "needn't", "mightn't", "couldn't", "wouldn't"
]

# 短縮形をそのまま読み上げるようにする処理
def preserve_contractions(text):
    # 短縮形をそのまま扱う（単語ごとにリスト化して、短縮形はそのまま保持）
    for contraction in CONTRACTIONS:
        text = text.replace(contraction, f" {contraction} ")  # 短縮形の前後にスペースを追加して調整
    return text

# Google Cloud Text-to-Speechを使用してテキストを音声に変換する関数
def text_to_speech(text, output_file="output.mp3"):
    print('音声ファイルを生成しています...')
    
    # 短縮形をそのままにしたテキストに変換
    text = preserve_contractions(text)

    # Google CloudのText-to-Speechクライアントを初期化
    client = texttospeech.TextToSpeechClient()

    # 音声変換するテキストと音声設定
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # 言語設定 (例: 英語)
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # 声の性別
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.7  # MP3形式で出力,スピードを設定
    )

    # テキストを音声に変換
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # 生成した音声をMP3ファイルに保存
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"音声ファイルが保存されました: {output_file}")

    # 音声ファイルを再生
    playsound.playsound(output_file)

# transcription.txtからテキストを読み上げる
if __name__ == "__main__":
    if os.path.exists("transcription.txt"):
        with open("transcription.txt", "r", encoding="utf-8") as f:
            text = f.read()
        text_to_speech(text)
    else:
        print("文字起こしファイルが見つかりません。lyrics.pyを実行して文字起こしを行ってください。")
