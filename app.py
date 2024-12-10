import csv
import os
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
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to store the uploaded file
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

mail = Mail(app)

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        emails = request.form.get("emails")
        subject = request.form.get("subject")
        message = request.form.get("message")
        file = request.files.get("file")

        # Check if file was uploaded and is a CSV
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Parse the CSV to extract emails
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                emails = [row[0].strip() for row in reader if row]  # Assuming emails are in the first column

        # Validate the inputs
        if not emails or not subject or not message:
            flash("Please provide email addresses, a subject, and a message.", "danger")
            return redirect(url_for("index"))

        try:
            # Send email to each recipient
            for email in emails:
                msg = Message(subject, sender="your_email@gmail.com", recipients=[email])
                msg.body = message
                mail.send(msg)
            flash("Emails sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending emails: {e}", "danger")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
