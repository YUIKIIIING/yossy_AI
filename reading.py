from google.cloud import texttospeech
import playsound  # 再生用にインストール: pip install playsound

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\YUIKIIIING\\Downloads\\geeksalon-441211-4622fab85300.json"

# Google Cloud Text-to-Speechを使用してテキストを音声に変換する関数
def text_to_speech(text, output_file="output.mp3"):
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
        speaking_rate=0.65  # MP3形式で出力,スピードを設定
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