#conda activate youtube-mp3
from faster_whisper import WhisperModel
from youtubemp3 import download_youtube_audio_as_mp3
from punctuation import add_punctuation
import os

# Whisperモデルの初期化（グローバル変数として定義）
model = WhisperModel("medium", device="cpu", compute_type="int8")


# MP3ファイルを文字起こしする関数
def transcribe_audio(mp3_path):
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"{mp3_path} が見つかりません。")
    # グローバル変数のmodelを使用
    segments, info = model.transcribe(mp3_path)
    transcription = " ".join(segment.text for segment in segments)
    return transcription

# メインの関数
def process_youtube_audio(youtube_url):
    mp3_path = download_youtube_audio_as_mp3(youtube_url)
    print("歌詞起こし中です...")
     # MP3ファイルが存在するか確認
    if not os.path.exists(mp3_path):
        print(f"エラー: {mp3_path} が見つかりません。")
        return
    try:
        transcription = transcribe_audio(mp3_path)

    # ダウンロードしたMP3ファイルを削除
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        print(f"MP3ファイルが削除されました: {mp3_path}")

    # 句読点を追加
    punctuated_text = add_punctuation(transcription)

    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(punctuated_text)

    print("文字起こし結果:")
    print(punctuated_text)
    return punctuated_text
