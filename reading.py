import os
import json
from google.oauth2 import service_account
from google.cloud import texttospeech

# サービスアカウントJSONファイルのパス
SERVICE_ACCOUNT_PATH = "C:/Users/YUIKIIIING/Downloads/geeksalon-441211-4622fab85300.json"

# 環境変数の設定
with open(SERVICE_ACCOUNT_PATH, "r", encoding="utf-8") as f:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = f.read()

def generate_audio_from_transcription(input_file="transcription.txt", output_file="output.mp3"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"{input_file} が見つかりません。")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    if not text.strip():
        raise ValueError(f"{input_file} が空です。")

    credentials_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if not credentials_json:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS_JSON が設定されていません。")

    credentials_dict = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.7
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    print(f"音声ファイルが生成されました: {output_file}")
    return output_file

