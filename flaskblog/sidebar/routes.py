import os

from flask import render_template, Blueprint, url_for, current_app, send_from_directory, flash
from werkzeug.utils import redirect

from flaskblog import db
from flaskblog.models import ContactMessage
from flaskblog.sidebar.forms import ContactForm
from flaskblog.utils import create_sentiment_index_plot, create_msgs_vols_mkt_caps_plot

sidebar = Blueprint('sidebar', __name__)


@sidebar.route('/files_dir/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # --- append app root path to data' folder
    files_dir = os.path.join(current_app.root_path,
                             current_app.config['FILES_FOLDER'])
    # --- return file from the full path
    return send_from_directory(directory=files_dir, filename=filename)


@sidebar.route("/crypto_sentiment")
def crypto_sentiment():
    plot_0, sent_idx_filenames, crypto_names = create_msgs_vols_mkt_caps_plot()
    plot_1, ticker_1 = create_sentiment_index_plot(filename=sent_idx_filenames[0])
    plot_2, ticker_2 = create_sentiment_index_plot(filename=sent_idx_filenames[1])
    plot_3, ticker_3 = create_sentiment_index_plot(filename=sent_idx_filenames[2])
    plot_4, ticker_4 = create_sentiment_index_plot(filename=sent_idx_filenames[3])
    plot_5, ticker_5 = create_sentiment_index_plot(filename=sent_idx_filenames[4])
    # return render_template("graphics.html", title='Graphics')
    return render_template("crypto_sentiment.html", plot_0=plot_0,
                           plot_1=plot_1, plot_2=plot_2, plot_3=plot_3, plot_4=plot_4, plot_5=plot_5,
                           ticker_1=ticker_1, ticker_2=ticker_2, ticker_3=ticker_3, ticker_4=ticker_4,
                           ticker_5=ticker_5, filename_1=sent_idx_filenames[0], filename_2=sent_idx_filenames[1],
                           filename_3=sent_idx_filenames[2], filename_4=sent_idx_filenames[3],
                           filename_5=sent_idx_filenames[4], cryptoname_1=crypto_names[0],
                           cryptoname_2=crypto_names[1], cryptoname_3=crypto_names[2],
                           cryptoname_4=crypto_names[3], cryptoname_5=crypto_names[4])


@sidebar.route("/roboadvisor_fundamental")
def roboadvisor_fundamental():
    return render_template("roboadvisor_fundamental.html", title='RoboAdvisor - Fundamental')


@sidebar.route("/roboadvisor_technical")
def roboadvisor_technical():
    return render_template("roboadvisor_technical.html", title='RoboAdvisor - Technical')


@sidebar.route("/forecasts")
def forecasts():
    return render_template("forecasts.html", title='Forecasts')


@sidebar.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(name=form.name.data,
                             email=form.email.data, message=form.body.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your information has been sent', 'success')
        return redirect(url_for("sidebar.success_contact"))
    return render_template("contact.html", title='Contact', form=form)


@sidebar.route("/success_contact", methods=["GET", "POST"])
def success_contact():
    """Generic success page upon form submission."""
    return render_template(
        "success_contact.html"
    )
