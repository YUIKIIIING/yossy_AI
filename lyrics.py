#conda activate youtube-mp3
from faster_whisper import WhisperModel
from youtubemp3 import download_youtube_audio_as_mp3
from punctuation import add_punctuation
import os


# MP3ファイルを文字起こしする関数
def transcribe_audio(mp3_path, model):
    if not os.path.exists(mp3_path):
        raise FileNotFoundError(f"{mp3_path} が見つかりません。")

    segments, info = model.transcribe(mp3_path, beam_size=1)  # beam_sizeを小さくして高速化
    transcription = " ".join(segment.text for segment in segments)
    return transcription

# メインの関数(高速化)
def process_youtube_audio(youtube_url, model):
    try:
        mp3_path = download_youtube_audio_as_mp3(youtube_url)
        print('歌詞起こし中です...')
        if not os.path.exists(mp3_path):
            print(f"エラー: {mp3_path} が見つかりません。")
            return

        # 文字起こしを実行
        transcription = transcribe_audio(mp3_path, model)

        if os.path.exists(mp3_path):
            os.remove(mp3_path)
            print(f"MP3ファイルが削除されました: {mp3_path}")
        punctuated_text = add_punctuation(transcription)

        # 句読点付きテキストを保存
        transcription_file = "transcription.txt"
        with open(transcription_file, "w", encoding="utf-8") as f:
            f.write(punctuated_text)
        print(f"文字起こし結果が保存されました: {transcription_file}")

        return punctuated_text
    
    except Exception as e:
        print(f"エラー: {e}")
        return
    #エラーハンドリング(2024/11/26)

# 実行
if __name__ == "__main__":
    youtube_links = [input("YouTubeのリンクを入力してください: ")]
    model = WhisperModel("small", device="cpu", compute_type="int8")
    for url in youtube_links:
        result = process_youtube_audio(url, model)
        print('歌詞起こし結果')
        print(result)
