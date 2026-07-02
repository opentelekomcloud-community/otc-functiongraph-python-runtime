import json

from flask import Flask, request, jsonify

# Create a Flask application instance.
app = Flask(__name__)


# Define a route /index that handles GET requests.
@app.route('/index', methods=['GET'])
def index_get():
    # Print the request path for debugging.
    print("***" + request.path + "***", flush=True)
    
    return jsonify(message="Hello from scratch-http sample!")
    
# Define a route /index that handles POST requests.
@app.route('/index', methods=['POST'])
def index():
    # Print the request path for debugging.
    print("***" + request.path + "***", flush=True)

    # Build response data.
    data = {
        "statusCode": 200,
        "isBase64Encoded": False,
        "body": json.dumps(request.path + " success"),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    return jsonify(data)

# Main program entry
if __name__ == '__main__':
    # dev server:
    # app.run(host="0.0.0.0", port=8000)
    
    # production server using waitress:
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)