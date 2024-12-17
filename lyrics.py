# conda activate youtube-mp3
from faster_whisper import WhisperModel
from youtubemp3 import download_youtube_audio_as_mp3
from punctuation import add_punctuation, process_text
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
    # YouTubeの音声をダウンロードしてMP3パスを取得
    mp3_path = download_youtube_audio_as_mp3(youtube_url)
    print("歌詞起こし中です...")
    
    # MP3ファイルが存在するか確認
    if not os.path.exists(mp3_path):
        print(f"エラー: {mp3_path} が見つかりません。")
        return

    transcription = None  # 初期化
    try:
        # MP3を文字起こし
        transcription = transcribe_audio(mp3_path)
    except Exception as e:
        print(f"文字起こし中にエラーが発生しました: {e}")
    finally:
        # ダウンロードしたMP3ファイルを削除
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        print(f"MP3ファイルが削除されました: {mp3_path}")

    if transcription is None:
        print("文字起こしに失敗しました。")
        return

    # 句読点を追加
    try:
        doc = process_text(transcription)  # spaCyを使用して解析
        punctuated_text = add_punctuation(doc)  # 句読点を追加
    except Exception as e:
        print(f"句読点の追加中にエラーが発生しました: {e}")
        return

    # 結果をファイルに保存
    output_path = "transcription.txt"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(punctuated_text)
        print(f"文字起こし結果が保存されました: {output_path}")
    except Exception as e:
        print(f"文字起こし結果の保存中にエラーが発生しました: {e}")

    print("文字起こし結果:")
    print(punctuated_text)
    return punctuated_text
