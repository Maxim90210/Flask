from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

app.config.update(
    CELERY_BROKER_URL='amqp://guest:guest@rabbitmq:5672//',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = make_celery(app)

@celery.task
def example_task(x, y):
    return x + y
