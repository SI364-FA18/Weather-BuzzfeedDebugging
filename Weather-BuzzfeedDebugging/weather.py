from flask import Flask, request, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp
import json, requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug=True

API_KEY = "2e05204953a15ff2c1b7bc7f798349a9" #enter API key from Open Weather Maps here

####################
###### FORMS #######
####################


class WeatherForm(FlaskForm):
    zipcode = IntegerField("Enter a US zipcode", validators=[Required()]) #An alternate solution is to use the built-in length validator instead of the custom validator "validate_zipcode"
    submit = SubmitField("Submit")


    def validate_zipcode(self, field):
        if len(str(field.data)) != 5:
            raise ValidationError("Please enter a 5 digit zipcode")

####################
###### ROUTES ######
####################

@app.route('/zipcode', methods = ["POST", "GET"])
def zipcode():
    form = WeatherForm()
    if form.validate_on_submit():
        zipcode = str(form.zipcode.data)
        params = {}
        params["zip"] = zipcode + ",us"
        params["appid"] = API_KEY
        baseurl = "http://api.openweathermap.org/data/2.5/weather?"
        response = requests.get(baseurl, params = params)
        response_dict = json.loads(response.text)

        description = response_dict["weather"][0]["description"]
        city = response_dict["name"]
        temperature_kelvin = response_dict["main"]["temp"]
        temperature = temperature_kelvin * 1.8 - 459.67 #convert temperature from Kelvin to Fahrenheit

        return render_template('results.html',city=city,description=description,temperature=temperature)
    
    flash(form.errors)
    return render_template('weather_form.html', form=form)

if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)
