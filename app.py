from typing import Tuple
from flask import Flask
from flask_caching import Cache
import werkzeug
import random

app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'DEBUG': True,
    'CACHE_DEFAULT_TIMEOUT': 3600  # 1 hour
})


@app.route('/greetings/<greeting>', methods=['POST'])
def put_greeting(greeting: str = '') -> str:
    greeting = greeting.strip()
    if len(greeting) == 0 or len(greeting) > 140:
        raise werkzeug.exceptions.BadRequest
    cache.set(greeting, greeting)
    return greeting


@app.route('/all_greetings/', methods=['GET'])
def get_all_greeting() -> dict:
    dump_cache = []
    for k in cache.cache._cache:
        item = cache.get(k)
        if item:
            dump_cache.append(cache.get(k))
    return {'greetings': dump_cache}


@app.route('/greetings', methods=['GET'])
def get_greeting() -> str:
    dump_cache = []
    for k in cache.cache._cache:
        item = cache.get(k)
        if item:
            dump_cache.append(cache.get(k))

    if len(dump_cache) == 0:
        raise werkzeug.exceptions.NotFound
    r = random.randint(0, len(dump_cache) - 1)
    return dump_cache[r]


@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_greeting_too_long(e) -> Tuple[str, int]:
    return 'Invalid greeting', 400


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_no_greeting_found(e) -> Tuple[str, int]:
    return 'No greetings were found', 404
