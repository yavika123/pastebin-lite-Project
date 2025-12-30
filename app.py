# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta
# import string, random
#
# # 1️⃣ Create Flask app
# app = Flask(__name__)
#
# # 2️⃣ SQLite configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastes.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# # 3️⃣ Initialize DB
# db = SQLAlchemy(app)
#
# # 4️⃣ Paste model
# class Paste(db.Model):
#     id = db.Column(db.String(10), primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     ttl_seconds = db.Column(db.Integer, nullable=True)
#     max_views = db.Column(db.Integer, nullable=True)
#     views = db.Column(db.Integer, default=0)
#
# # 5️⃣ Health check route
# @app.route("/api/healthz", methods=["GET"])
# def health_check():
#     return jsonify({"ok": True}), 200
#
# # 6️⃣ Helper to generate random ID
# def generate_id(length=6):
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
#
# # 7️⃣ Create paste route
# @app.route("/api/pastes", methods=["POST"])
# def create_paste():
#     data = request.get_json()
#     content = data.get("content")
#     ttl_seconds = data.get("ttl_seconds")
#     max_views = data.get("max_views")
#
#     # Validation
#     if not content or not content.strip():
#         return jsonify({"error": "Content is required"}), 400
#
#     if ttl_seconds is not None:
#         try:
#             ttl_seconds = int(ttl_seconds)
#             if ttl_seconds < 1:
#                 raise ValueError
#         except:
#             return jsonify({"error": "ttl_seconds must be an integer ≥ 1"}), 400
#
#     if max_views is not None:
#         try:
#             max_views = int(max_views)
#             if max_views < 1:
#                 raise ValueError
#         except:
#             return jsonify({"error": "max_views must be an integer ≥ 1"}), 400
#
#     # Generate unique ID
#     paste_id = generate_id()
#
#     # Save paste to DB
#     new_paste = Paste(
#         id=paste_id,
#         content=content,
#         ttl_seconds=ttl_seconds,
#         max_views=max_views
#     )
#     db.session.add(new_paste)
#     db.session.commit()
#
#     return jsonify({
#         "id": paste_id,
#         "url": f"http://127.0.0.1:5000/p/{paste_id}"
#     }), 201
#
# # 8️⃣ Fetch paste API
# @app.route("/api/pastes/<paste_id>", methods=["GET"])
# def get_paste(paste_id):
#     paste = Paste.query.get(paste_id)
#     if not paste:
#         return jsonify({"error": "Paste not found"}), 404
#
#     # Check TTL
#     if paste.ttl_seconds:
#         expire_time = paste.created_at + timedelta(seconds=paste.ttl_seconds)
#         if datetime.utcnow() > expire_time:
#             return jsonify({"error": "Paste expired"}), 404
#
#     # Check max views
#     if paste.max_views and paste.views >= paste.max_views:
#         return jsonify({"error": "View limit exceeded"}), 404
#
#     # Increment views
#     paste.views += 1
#     db.session.commit()
#
#     return jsonify({
#         "content": paste.content,
#         "remaining_views": paste.max_views - paste.views if paste.max_views else None,
#         "expires_at": (paste.created_at + timedelta(seconds=paste.ttl_seconds)).isoformat() if paste.ttl_seconds else None
#     })
#
# # 9️⃣ View paste HTML
# @app.route("/p/<paste_id>", methods=["GET"])
# def view_paste(paste_id):
#     paste = Paste.query.get(paste_id)
#     if not paste:
#         return "Paste not found", 404
#
#     # TTL and max views check
#     if paste.ttl_seconds:
#         expire_time = paste.created_at + timedelta(seconds=paste.ttl_seconds)
#         if datetime.utcnow() > expire_time:
#             return "Paste expired", 404
#     if paste.max_views and paste.views >= paste.max_views:
#         return "View limit exceeded", 404
#
#     paste.views += 1
#     db.session.commit()
#     return render_template("view_paste.html", content=paste.content)
#
# # 1️⃣0️⃣ Run the app
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import string, random

# 1️⃣ Create Flask app
app = Flask(__name__)

# 2️⃣ SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pastes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3️⃣ Initialize DB
db = SQLAlchemy(app)

# 4️⃣ Paste model
class Paste(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ttl_seconds = db.Column(db.Integer, nullable=True)
    max_views = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, default=0)

# 5️⃣ Homepage route
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Welcome to Pastebin-Lite!</h1>
    <p>Use the API to create and view pastes:</p>
    <ul>
        <li>Health check: /api/healthz</li>
        <li>Create paste: POST /api/pastes</li>
        <li>Fetch paste JSON: /api/pastes/&lt;id&gt;</li>
        <li>View paste HTML: /p/&lt;id&gt;</li>
    </ul>
    """, 200

# 6️⃣ Health check route
@app.route("/api/healthz", methods=["GET"])
def health_check():
    return jsonify({"ok": True}), 200

# 7️⃣ Helper to generate random ID
def generate_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 8️⃣ Create paste route
@app.route("/api/pastes", methods=["POST"])
def create_paste():
    data = request.get_json()
    content = data.get("content")
    ttl_seconds = data.get("ttl_seconds")
    max_views = data.get("max_views")

    # Validation
    if not content or not content.strip():
        return jsonify({"error": "Content is required"}), 400

    if ttl_seconds is not None:
        try:
            ttl_seconds = int(ttl_seconds)
            if ttl_seconds < 1:
                raise ValueError
        except:
            return jsonify({"error": "ttl_seconds must be an integer ≥ 1"}), 400

    if max_views is not None:
        try:
            max_views = int(max_views)
            if max_views < 1:
                raise ValueError
        except:
            return jsonify({"error": "max_views must be an integer ≥ 1"}), 400

    # Generate unique ID
    paste_id = generate_id()

    # Save paste to DB
    new_paste = Paste(
        id=paste_id,
        content=content,
        ttl_seconds=ttl_seconds,
        max_views=max_views
    )
    db.session.add(new_paste)
    db.session.commit()

    return jsonify({
        "id": paste_id,
        "url": f"http://127.0.0.1:5000/p/{paste_id}"
    }), 201

# 9️⃣ Fetch paste API
@app.route("/api/pastes/<paste_id>", methods=["GET"])
def get_paste(paste_id):
    paste = Paste.query.get(paste_id)
    if not paste:
        return jsonify({"error": "Paste not found"}), 404

    # Check TTL
    if paste.ttl_seconds:
        expire_time = paste.created_at + timedelta(seconds=paste.ttl_seconds)
        if datetime.utcnow() > expire_time:
            return jsonify({"error": "Paste expired"}), 404

    # Check max views
    if paste.max_views and paste.views >= paste.max_views:
        return jsonify({"error": "View limit exceeded"}), 404

    # Increment views
    paste.views += 1
    db.session.commit()

    return jsonify({
        "content": paste.content,
        "remaining_views": paste.max_views - paste.views if paste.max_views else None,
        "expires_at": (paste.created_at + timedelta(seconds=paste.ttl_seconds)).isoformat() if paste.ttl_seconds else None
    })

# 🔟 View paste HTML
@app.route("/p/<paste_id>", methods=["GET"])
def view_paste(paste_id):
    paste = Paste.query.get(paste_id)
    if not paste:
        return "Paste not found", 404

    # TTL and max views check
    if paste.ttl_seconds:
        expire_time = paste.created_at + timedelta(seconds=paste.ttl_seconds)
        if datetime.utcnow() > expire_time:
            return "Paste expired", 404
    if paste.max_views and paste.views >= paste.max_views:
        return "View limit exceeded", 404

    paste.views += 1
    db.session.commit()
    return render_template("view_paste.html", content=paste.content)

import os
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port=int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

