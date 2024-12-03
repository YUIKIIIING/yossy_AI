from google.cloud import texttospeech
import os

# Google Cloud認証設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\YUIKIIIING\\Downloads\\geeksalon-441211-4622fab85300.json"

def generate_audio_from_transcription(input_file="transcription.txt", output_file="output.mp3"):
    # transcription.txt を確認
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} が見つかりません。")

    # transcription.txt を読み込む
    text = ""
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        raise ValueError(f"{input_file} が空です。")

    # Google Text-to-Speechを初期化
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3,
                                            speaking_rate=0.7)  # MP3形式で出力,スピードを設定)

    # 音声生成リクエスト
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # MP3ファイルとして保存
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    print(f"音声ファイルが生成されました: {output_file}")
    return output_file

if __name__ == "__main__":
    try:
        generate_audio_from_transcription()
    except FileNotFoundError as e:
        print(f"エラー: {e}")
    except ValueError as e:
        print(f"エラー: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
