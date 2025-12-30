Project description

Example: “Pastebin-Lite is a simple web app to create, share, and view text pastes with TTL and view limits.”

How to run locally

pip install -r requirements.txt
python app.py


Persistence used

Example: SQLite database (pastes.db)

Notable design decisions

TTL and max_views constraints

Flask + SQLAlchemy for simplicity