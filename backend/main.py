from flask import Flask, request, jsonify
from flask_cors import CORS

from graphRAG import graphRAG

import uuid
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def receive_message():

    # Parse JSON data from the request
    data = request.json
    
    # Log the incoming data
    print("Received data:", data)
    
    try:
        res = graphRAG(data['role'], data['content'])
        result = str(res)
    except Exception as e:
        print(e)
        result = "I'm sorry, I do not understand the question. Please provide a valid query related to the graph database schema."
    
    # Process the incoming message (example: send back a response)
    response_message = {
        'role': 'assistant',
        'content': result,
        'id': str(uuid.uuid4()),
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    }
    
    # Return the response as JSON
    return jsonify(response_message), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)