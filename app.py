from flask import Flask, request, render_template, send_file
from lyrics import process_youtube_audio
import os

app = Flask(__name__)

# トップページ（フォームの表示）
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return render_template("index.html", error="YouTubeリンクを入力してください。")

        try:
            # 文字起こし処理
            transcription = process_youtube_audio(youtube_url)
            return render_template("index.html", transcription=transcription)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

# 文字起こし結果のダウンロード
@app.route("/download")
def download():
    if os.path.exists("transcription.txt"):
        return send_file("transcription.txt", as_attachment=True)
    return "ファイルが見つかりません。"

if __name__ == "__main__":
    app.run(debug=True)
