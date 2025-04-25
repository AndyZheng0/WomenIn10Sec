from flask import Flask, render_template, request, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "respect_women"

@app.route("/", methods=["GET", "POST"])
def index():
    session.permanent = True  # persist data during session

    # Init session variables if needed
    if "start_time" not in session:
        session["start_time"] = None
        session["women"] = []

    now = datetime.now()
    message, color = "", ""

    # Handle form submission
    if request.method == "POST":
        if "start" in request.form:
            session["start_time"] = now.timestamp()
            session["women"] = []
        elif "name" in request.form and session["start_time"]:
            if now.timestamp() - session["start_time"] < 10:
                session["women"].append(request.form["name"])
            else:
                session["start_time"] = None

    # Final message logic
    women = session.get("women", [])
    count = len(women)
    if session["start_time"] and now.timestamp() - session["start_time"] >= 10:
        if count >= 5:
            message, color = "Wow, you really respect women!", "green"
        elif count == 4:
            message, color = "You like girls", "lightblue"
        elif count == 3:
            message, color = "You like girls", "white"
        elif count == 2:
            message, color = "Only 2? Whatever", "orange"
        elif count <= 1:
            message, color = "So you hate women", "red"
        session["start_time"] = None

    return render_template(
        "index.html",
        women=women,
        message=message,
        color=color,
        start_time=session.get("start_time"),
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
