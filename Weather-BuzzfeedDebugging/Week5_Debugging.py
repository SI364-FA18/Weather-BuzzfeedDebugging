##Debug this code to get articles from Buzzfeed
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
import json, requests

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/')
def hello_to_you():
    return 'Hello!'

class buzzForm(FlaskForm):
    feed = StringField('Enter a feed name(news or lol or life)', validators=[Required()])
    submit = SubmitField("Submit")

@app.route("/buzzfeed")
def buzzfeed():
    form = buzzForm()
    return render_template('buzzfeed.html', form=form)


@app.route("/buzzfeed_articles", methods = ["POST", "GET"])
def buzzfeed_articles():
    if request.method == "POST":
        form = buzzForm()

        baseurl = "https://www.buzzfeed.com/api/v2/feeds/"
        feed_name = form.feed.data
        params = {}
        response = requests.get(baseurl + feed_name)
        response_dict = json.loads(response.text)

        return render_template('article_links.html', results = response_dict["buzzes"])

    return redirect(url_for("buzzfeed"))

if __name__ == '__main__':
    app.run()