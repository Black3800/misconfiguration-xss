import secrets
from flask import Flask, request, render_template, make_response, send_from_directory, g

app = Flask(__name__, static_folder="public", static_url_path="/public")

@app.after_request
def set_security_headers(response):
    # Retrieve nonce from g (if generated)
    nonce = getattr(g, 'nonce', None)
    if request.args.get("enable_csp"):
        csp_value = request.args.get("csp_value").split(";")
        if not csp_value:
            csp_value = [
                "default-src 'self'"
                "style-src 'self' https://cdn.jsdelivr.net"
                "img-src data:"
                "script-src 'self' https://cdn.jsdelivr.net"
            ]
        # Append nonce to the script-src directive if the nonce checkbox is checked
        if request.args.get("enable_nonce") and nonce:
            csp_value[-1] += " 'nonce-{}'".format(nonce)
        response.headers["Content-Security-Policy"] = ";".join(csp_value)
    if request.args.get("enable_xcto"):
        response.headers["X-Content-Type-Options"] = "nosniff"
    if request.args.get("enable_xss"):
        response.headers["X-XSS-Protection"] = "1; mode=block"
    if request.args.get("enable_cors"):
        cors_value = request.args.get("cors_value")
        if not cors_value:
            cors_value = "*"
        response.headers["Access-Control-Allow-Origin"] = cors_value
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Serve static files from the 'upload' directory with a fixed MIME type.
@app.route('/upload/<path:filename>')
def upload_file(filename):
    return send_from_directory('upload', filename, mimetype="")

@app.route("/", methods=["GET"])
def index():
    # Retrieve unsanitized user input.
    user_input = request.args.get("msg", "")
    
    # If nonce is enabled, generate a random nonce and store it in g.
    nonce = None
    if request.args.get("enable_nonce"):
        nonce = secrets.token_urlsafe(16)
        g.nonce = nonce

    # Render the template with the user input and nonce.
    resp = make_response(render_template("index.html", user_input=user_input, nonce=nonce))
    
    # Always reset the same "secret" cookie based on the secure cookie checkbox.
    if request.args.get("enable_cookie_secure"):
        resp.set_cookie("secret", "secret_cookie", httponly=True, secure=True, samesite="Strict")
    else:
        resp.set_cookie("secret", "secret_cookie")
    
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    