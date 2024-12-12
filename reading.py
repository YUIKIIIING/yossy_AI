from google.cloud import texttospeech
from google.oauth2 import service_account
import os
import json

def generate_audio_from_transcription(input_file="transcription.txt", output_file="output.mp3"):
    # transcription.txt を確認
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} が見つかりません。")

    # transcription.txt を読み込む
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        raise ValueError(f"{input_file} が空です。")

    # 環境変数からサービスアカウントキーを取得
    credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not credentials_json:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS_JSON が設定されていません。")

    # JSON文字列をPythonオブジェクトに変換
    credentials_dict = json.loads(credentials_json)

    # サービスアカウント資格情報オブジェクトを生成
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    # Google Text-to-Speechクライアントを初期化
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    # リクエスト構築
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.7
    )

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
