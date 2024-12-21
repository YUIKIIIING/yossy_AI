from flask import Flask, request, render_template, send_file, jsonify
from lyrics import process_youtube_audio
from reading import generate_audio_from_transcription
from translation import process_translation_async, correct_grammar
import os
import asyncio

app = Flask(__name__)

# トップページ（フォームの表示）
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return {"error": "YouTubeリンクを入力してください。"}, 400

        try:
            # 文字起こし処理
            transcription = process_youtube_audio(youtube_url)
            return {"transcription": transcription}  # JSONで結果を返す
        except Exception as e:
            return {"error": str(e)}, 500

    return render_template("index.html")

# 文字起こし結果のダウンロード
@app.route("/download")
def download():
    if os.path.exists("transcription.txt"):
        return send_file("transcription.txt", as_attachment=True)
    return "ファイルが見つかりません。"

# 音声読み上げ
@app.route("/read-aloud")
def read_aloud():
    try:
        output_file = generate_audio_from_transcription()
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"エラーが発生しました: {e}"

# 翻訳ページ
@app.route("/translate", methods=["GET", "POST"])
def translate():
    transcription_file = "transcription.txt"
    if not os.path.exists(transcription_file):
        return render_template("translation.html", error="文字起こしファイルが見つかりません。まず文字起こしを実行してください。")

    try:
        # transcription.txt を読み込む
        with open(transcription_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()  # 行ごとに分割

        source_lang = "en"
        target_lang = "ja"

        # 非同期翻訳処理を実行
        print("翻訳処理をバックエンドで実行中...")
        translated_texts = asyncio.run(process_translation_async(lines, target_lang))

        # 文法修正
        corrected_texts = [correct_grammar(text) for text in translated_texts]

        # 結果をHTMLに渡す
        final_result = "\n".join(corrected_texts)
        return render_template("translation.html", translated_text=final_result)

    except Exception as e:
        return render_template("translation.html", error=f"エラーが発生しました: {e}")

#アプリ起動
if __name__ == "__main__":
    app.run(debug=True)