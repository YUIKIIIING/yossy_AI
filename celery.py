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

# celery.pyの中での遅延インポートの例
def create_celery_app():
    from celery import Celery
    app = Celery('your_app')
    app.config_from_object('your_config_module')
    return app
