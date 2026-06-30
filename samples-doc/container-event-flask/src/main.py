import json

from flask import Flask, request, jsonify, g

from loggingmiddleware import register_logging_middleware

# Create a Flask application instance.
app = Flask(__name__)
register_logging_middleware(app)

# Define the function initializer
@app.route('/init', methods=['POST'])
def init_post():
    # Print the request path for debugging.
    g.logger.info("***" + request.path + "***")
    
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


# Define the function handler.
@app.route('/invoke', methods=['POST'])
def invoke_post():
    
    requestId = g.cff_request_id
    ak = request.headers.get("x-cff-security-access-key")
    sk = request.headers.get("x-cff-security-secret-key")
    st = request.headers.get("x-cff-security-token")
    
    token = request.headers.get("x-cff-auth-token")

    
    # Print the request path for debugging.
    g.logger.info("***" + request.path + "***")
    g.logger.info("***requestId: " + requestId + "***")
    
    # Log all incoming headers for debugging purposes.
    for header_name, header_value in request.headers.items():
        g.logger.debug(f"***header[{header_name}]: {header_value}***")
        
    if ak and ak != "null":
        g.logger.info("***ak: " + ak + "***")
    else:
        g.logger.error("***NO AGENCY SPECIFIED OR KEYS NOT INCLUDED ***")

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
    #app.run(host="0.0.0.0", port=8000)
    
    # production server using waitress:
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)