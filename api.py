from sanic import Sanic
from sanic.response import json

from libraries.Config import config
from libraries.Rabbit import Rabbit

rabbitMq = Rabbit()

app = Sanic()


@app.route('/')
async def test(request):
    return json({'message': 'Welcome to Wuxiaworld chapters to pdf api'})


@app.route('/crawl')
async def trigger(request):
    data = request.raw_args
    print(data)
    if not data or 'email' not in data or 'start_chapter' not in data or 'end_chapter' not in data:
        return json({"response": "Please provide 'email', 'start_chapter' and 'end_chapter'"})
    print('Pushing data to queue')
    rabbitMq.push_to_queue(data)
    return json(
        {'status': True, 'message': 'Your work has been queued. The pdf will be sent to your e-mail'},
        headers={'Content-Type': 'application/json'},
        status=200
    )


if __name__ == '__main__':
    app.run(host=config['app']['host'], port=config['app']['port'])
