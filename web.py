"""
import json

with open('Study Plan.md', 'r') as f:
    data = f.read()
lines = data.split('\n')
days = []
current_day = None
topics = []
for line in lines:
    if line.startswith('#'):
        if current_day:
            days.append({'date': current_day, 'topics': topics})
        current_day = line[2:]
        topics = []
    elif line.startswith('- '):
        topics.append(line[2:])
days.append({'date': current_day, 'topics': topics})

data_string = json.dumps(days)
"""

"""Me"""
from flask import Flask, render_template, request, make_response, flash, redirect, url_for
app = Flask(__name__)

"""Chat"""
@app.route('/')
def index():
    with open('Study Plan.md', 'r') as f:
        data = f.read()
    lines = data.split('\n')
    days = []
    current_day = None
    topics = []
    for line in lines:
        if line.startswith('#'):
            if current_day:
                days.append({'date': current_day, 'topics': topics})
            current_day = line[2:]
            topics = []
        elif line.startswith('- '):
            topics.append(line[2:])
    days.append({'date': current_day, 'topics': topics})
    return render_template('index.html', days=days)

"""Me"""
if __name__ == "__main__":
    print("GameSetMatch")
    app.run(debug=True)