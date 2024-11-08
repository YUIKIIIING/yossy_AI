from faster_whisper import WhisperModel
from youtubemp3 import download_youtube_audio_as_mp3
import os
import concurrent.futures

# MP3ファイルを文字起こしする関数
def transcribe_audio(mp3_path, model):
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"{mp3_path} が見つかりません。")

    segments, info = model.transcribe(mp3_path)
    transcription = " ".join(segment.text for segment in segments)
    return transcription

# メインの関数
def process_youtube_audio(youtube_url):
    mp3_path = download_youtube_audio_as_mp3(youtube_url)

    # MP3ファイルが存在するか確認
    if not os.path.exists(mp3_path):
        print(f"エラー: {mp3_path} が見つかりません。")
        return
    
    # Whisperモデルのロードを事前に行う
    model = WhisperModel("medium", device="cpu", compute_type="int8")  # 'medium'モデルで処理を高速化
    transcription = transcribe_audio(mp3_path, model)

    # ダウンロードしたMP3ファイルを削除
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
        print(f"MP3ファイルが削除されました: {mp3_path}")

    print("文字起こし結果:", transcription)
    return transcription

# 複数のYouTubeリンクを並列で処理
def process_multiple_youtube_audios(youtube_links):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_youtube_audio, url) for url in youtube_links]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

# 実行例
if __name__ == "__main__":
    youtube_links = [input("YouTubeのリンクを入力してください: ")]
    process_multiple_youtube_audios(youtube_links)
