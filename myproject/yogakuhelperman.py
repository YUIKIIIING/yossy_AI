from celery import Celery

app = Celery('yogakuhelperman', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task
def example_task(x, y):
    return x + y
