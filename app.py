from flask import Flask, request, render_template, send_file, jsonify
from celery_config import Celery
from celery_config import current_app
from celery_config import make_celery
from lyrics import process_youtube_audio
from reading import generate_audio_from_transcription
from translation import process_translation_async, correct_grammar
import os
import asyncio

# Flaskアプリケーションの設定
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',  # Redisがインストールされていることが前提
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

# Celeryのインスタンスを作成
celery = make_celery(app)

# トップページ（フォームの表示）
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        if not youtube_url:
            return {"error": "YouTubeリンクを入力してください。"}, 400

        # 文字起こしを非同期で実行
        task = transcribe_youtube_audio.apply_async(args=[youtube_url])
        return jsonify({"task_id": task.id}), 202

    return render_template("index.html")


# 文字起こし処理を非同期で行う
@celery.task
def transcribe_youtube_audio(youtube_url):
    try:
        transcription = process_youtube_audio(youtube_url)
        # 文字起こし結果をファイルに保存
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(transcription)
        return transcription
    except Exception as e:
        raise Exception(f"文字起こしのエラー: {e}")

# 文字起こし結果のダウンロード
@app.route("/download")
def download():
    if os.path.exists("transcription.txt"):
        return send_file("transcription.txt", as_attachment=True)
    return "ファイルが見つかりません。"

# 音声読み上げ処理を非同期で実行
@app.route("/read-aloud")
def read_aloud():
    task = generate_audio_from_transcription_async.apply_async()
    return jsonify({"task_id": task.id}), 202

@celery.task
def generate_audio_from_transcription_async():
    try:
        output_file = generate_audio_from_transcription()
        return output_file
    except Exception as e:
        raise Exception(f"音声生成エラー: {e}")

# 翻訳ページを非同期で処理
@app.route("/translate", methods=["GET", "POST"])
def translate():
    transcription_file = "transcription.txt"
    if not os.path.exists(transcription_file):
        return render_template("translation.html", error="文字起こしファイルが見つかりません。まず文字起こしを実行してください。")

    try:
        # transcription.txt を読み込む
        with open(transcription_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()  # 行ごとに分割

        # 非同期翻訳処理を実行
        task = translate_text_async.apply_async(args=[lines, "ja"])
        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        return render_template("translation.html", error=f"エラーが発生しました: {e}")

# 翻訳処理を非同期で行う
@celery.task
def translate_text_async(lines, target_lang):
    try:
        # 非同期翻訳を処理
        translated_texts = asyncio.run(process_translation_async(lines, target_lang))

        # 文法修正
        corrected_texts = [correct_grammar(text) for text in translated_texts]

        # 結果を返す
        return "\n".join(corrected_texts)
    except Exception as e:
        raise Exception(f"翻訳処理エラー: {e}")

# 結果の取得
@app.route("/task-status/<task_id>")
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"status": "処理中"})
    elif task.state == "SUCCESS":
        return jsonify({"status": "成功", "result": task.result})
    else:
        return jsonify({"status": task.state, "result": str(task.info)})

# アプリ起動
# if __name__ == "__main__":
#     app.run(debug=True)
