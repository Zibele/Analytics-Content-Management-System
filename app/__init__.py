import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# Create application instance
app = Flask(__name__)
app.config.from_object(Config)

# Create database instance
db = SQLAlchemy(app)

# Create database migration instance
migrate = Migrate(app, db)

# Create login manager instance
login = LoginManager(app)
login.login_view = "login"

# Flask Bootstrap instance
bootstrap = Bootstrap(app)

# Flask Mail instance
mail = Mail(app)

# Avoid circular dependancies
from app import routes, models, errors

# Logging Errors
if not app.debug:
    # Email Based Logging
    if app.config["MAIL_SERVER"]:
        auth = None

        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])

        secure = None

        if app.config["MAIL_USE_TLS"]:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost = (app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr = "no-reply@" + app.config["MAIL_SERVER"],
            toaddrs = app.config["ADMINS"], 
            subject = "Microblog Failure",
            credentials = auth,
            secure = secure)
        
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    # File Based Logging
    if not os.path.exists("logs"):
        os.mkdir("logs")

    file_handler = RotatingFileHandler("logs/microblog.py", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    
    app.logger.addHandler(file_handler)

    # Create an info-based log
    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog startup")
