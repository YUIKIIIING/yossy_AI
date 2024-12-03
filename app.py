from flask import Flask, request, render_template, send_file, redirect, url_for
from lyrics import process_youtube_audio
from reading import generate_audio_from_transcription
from translation import translate_text_with_gas, correct_grammar
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

# 音声読み上げ
@app.route("/read-aloud")
def read_aloud():
    try:
        # reading.py の関数を呼び出して音声ファイルを生成
        output_file = generate_audio_from_transcription()
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        return f"エラーが発生しました: {e}"

# 翻訳ページ
@app.route("/translate", methods=["GET", "POST"])
def translate():
    # transcription.txt が存在するかチェック
    transcription_file = "transcription.txt"
    if not os.path.exists(transcription_file):
        return render_template("translation.html", error="文字起こしファイルが見つかりません。まず文字起こしを実行してください。")

    try:
        # transcription.txt を読み込む
        with open(transcription_file, "r", encoding="utf-8") as f:
            text = f.read()

        source_lang = "en"  # ソース言語をデフォルトで英語に設定
        target_lang = "ja"  # ターゲット言語をデフォルトで日本語に設定

        # 翻訳の実行
        translated_text = translate_text_with_gas(text, source_lang=source_lang, target_lang=target_lang)
        if translated_text:
            # 文法修正
            corrected_text = correct_grammar(translated_text)
            return render_template("translation.html", translated_text=corrected_text)
        else:
            return render_template("translation.html", error="翻訳に失敗しました。GAS APIを確認してください。")

    except Exception as e:
        return render_template("translation.html", error=f"エラーが発生しました: {e}")

if __name__ == "__main__":
    app.run(debug=True)
