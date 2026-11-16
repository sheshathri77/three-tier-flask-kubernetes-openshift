
import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import requests

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:4000")


@app.route('/')
def index():
    todos = {}

    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        response.raise_for_status()
        todos = response.json()

    except requests.RequestException as ex:
        print(f"Backend connection error: {ex}")

    return render_template('index.html', todos=todos)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
