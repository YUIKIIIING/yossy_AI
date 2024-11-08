import yt_dlp

def download_youtube_audio_as_mp3(url, output_path="output"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,  # 拡張子を含めずに指定
        'ffmpeg_location': 'C:/Users/YUIKIIIING/anaconda3/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        final_output_path = f"{output_path}.mp3"  # 出力ファイル名に拡張子を追加
        print(f"MP3ファイルが保存されました: {final_output_path}")
    except yt_dlp.utils.DownloadError as e:
        print(f"エラーが発生しました: {str(e)}")
        print("FFmpegのインストールを確認してください。")
    return final_output_path