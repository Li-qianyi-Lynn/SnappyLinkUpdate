import base64
import io
import time
import logging
import shortuuid
import qrcode
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists,  create_database
from datetime import datetime

from sqlalchemy import create_engine

# Set up logging
logging.basicConfig(filename='snappy_link.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:@/snappy_link'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Create the database if it does not exist
if not database_exists(engine.url):
    create_database(engine.url)
    logging.info("Database created successfully.")
else:
    logging.info("Database already exist.")

# Database model, storing long urls, short codes and create time
class Link2(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    short_code = db.Column(db.String(500), nullable=False)
    original_url = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    visit_count = db.Column(db.Integer, nullable=False, default=1)


# Build database
with app.app_context():
    db.create_all()

# generate short codes with length of 6
def generate_short_code(length=6):
    short_code = shortuuid.ShortUUID().random(length=length)
    logging.info(f"Generated short code: {short_code}")
    return short_code

    # Another logic for generating short urls, and we don't use that way:
    # characters = string.ascii_letters + string.digits  # involve ascii + digits
    # short_code = ''.join(random.choice(characters) for _ in range(length))
    # # Ensure that the generated short url is unique and regenerate if duplicated
    # link = Link.query.filter_by(short_code=short_code).first()
    # if link:
    #     return generate_short_code(length)
    # return short_code

# URL validation
def validate_url(long_url):
    """
    URL validation logic to check for proper lengths.

    :param long_url: The original long URL
    :return: A tuple containing validation result (True/False) and an error message if invalid
    """

    # Check if long_url exceeds the length limit
    if len(long_url) > 2000:
        logging.warning("URL is too long")
        return False, "URL is too long"

    # URL is valid, return True and URL
    return True, long_url


@app.route("/", methods=['GET','POST'])
def store_short_url():

    if request.method == "POST":  # request long urls and generate short urls
        long_url = request.form['url']
        logging.info(f"Received long URL: {long_url}")
        is_valid, result = validate_url(long_url)

        # If URL is valid, generate short code and store in the database, else return error message
        if is_valid:
            short_code = generate_short_code()

            # Store long urls and short urls in the database
            new_link = Link2(original_url=long_url, short_code=short_code)
            db.session.add(new_link)
            db.session.commit()
            logging.info(f"Stored new link with short code: {short_code}")


            start_time = time.time()
            logging.info("Starting QR code generation...")

            # design and generate qr code.
            # The qrcode library is used to generate QR codes for the short links.
            # We can design the version and border.
            
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=1,
            )

            qr.add_data("http://i16k.com/r/" + new_link.short_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # save qr code
            img_io = io.BytesIO()
            img.save(img_io,'PNG')
            img_io.seek(0)
            qr_image = base64.b64encode(img_io.getvalue()).decode('utf-8')

            custom_domain = "http://i16k.com"
            #custom_domain = "http://127.0.0.1:5000/" test
            short_code = custom_domain + "/r/" + short_code

            # Another logic for generating qr code, and we don't use that way:
            # img = qrcode.make(short_code)
            # qr_code_filename = "static/qr_code.png"
            # img.save(qr_code_filename)
            #
            # qr_code_url = url_for("static", filename="qr_code.png")

            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.info(f"QR code generated in {elapsed_time:.2f} seconds")



        else:
            logging.error(f"Invalid URL: {result}")
            return f"Invalid URL: {result}", 400


        return render_template('generate.html', short_code=short_code, qr_image=qr_image, long_url=long_url)


    return render_template('generate.html')


# Redirect to original URL
@app.route('/r/<short_code>', methods=['GET'])
def short_link_redirect(short_code):
    logging.info(f"Handling redirect request for short code: {short_code}")
    link = Link2.query.filter_by(short_code=short_code).first()
    if link:
        # visit_count + 1 each redirect
        link.visit_count += 1
        db.session.commit()
        logging.info(f"Redirecting to original URL: {link.original_url}")
        return redirect(link.original_url)
    else:
        logging.error(f"Short URL not found: {short_code}")
        return "Short URL not found", 404


# Run the Flask application
if __name__ == '__main__':
    logging.info("Starting the Flask application...")
    app.run(host='0.0.0.0', port=80, debug=True)
    with app.app_context():
        db.create_all()