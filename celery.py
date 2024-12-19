from celery import Celery

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# Celeryアプリケーションの設定
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

# Celeryを作成
celery = make_celery(app)
