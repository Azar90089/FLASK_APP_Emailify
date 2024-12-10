from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session security

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example for Gmail
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'azar.jain9080@gmail.com'
app.config['MAIL_PASSWORD'] = 'rzwi ndzc miqi qfdd'


mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emails = request.form.get("emails").split(",")
        message = request.form.get("message")
        subject = request.form.get("subject")

        # Validate email list and message
        if not emails or not message:
            flash("Please provide both email addresses and a message.", "danger")
            return redirect(url_for("index"))

        try:
            # Send email to each recipient
            for email in emails:
                msg = Message(subject, sender="your_email@gmail.com", recipients=[email.strip()])
                msg.body = message
                mail.send(msg)
            flash("Emails sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending emails: {e}", "danger")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
