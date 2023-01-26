from flask import Flask
import os

from google.cloud import bigquery
client = bigquery.Client()

app = Flask(__name__)

query = """
    SELECT corpus AS title, COUNT(word) AS unique_words
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY title
    ORDER BY unique_words
    DESC LIMIT 10
"""

@app.route('/')
def hello():
    results = client.query(query)

    for row in results:
        title = row['title']
        unique_words = row['unique_words']
        print(f'{title:<20} | {unique_words}')

    return "Check the log for results"

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
