
import json
from datetime import datetime
from urllib import request as http_client
from flask import Flask, render_template, abort, request, jsonify

app = Flask(__name__)

@app.route('/')
def weather():  # put application's code here
    results = http_client.urlopen('https://raw.githubusercontent.com/eesur/country-codes-lat-long/master/country-codes-lat-long-alpha3.json').read()
    _results = json.loads(results)
    countries = _results["ref_country_codes"]
    country_list = list()
    for country in countries:
        _tmp = dict()
        _tmp[country['country']] = "lat="+str(country["latitude"])+"&lon="+str(country["longitude"])
        country_list.append(_tmp)

    return render_template("index.html", countries=country_list)

@app.route("/forecast", methods=['POST'])
def forecast():
    params = request.get_json()
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?{params['country']}&units=metric&appid=1f88cf5ad23f2d0ec9f6613c4508ef8c"
    forecast_weather_url = f"http://api.openweathermap.org/data/2.5/forecast?{params['country']}&units=metric&appid=1f88cf5ad23f2d0ec9f6613c4508ef8c"
    try:
        data = dict()
        current_source = http_client.urlopen(current_weather_url).read()
        _curr_data = json.loads(current_source)
        _current = dict()
        _current["description"] = _curr_data['weather'][0]['description']
        _current["icon"] = "https://www.weatherbit.io/static/img/icons/t"+_curr_data['weather'][0]['icon']+".png"
        _current["temp"] = _curr_data['main']['temp']
        data['current_weather'] = _current

        forecast_source = http_client.urlopen(forecast_weather_url).read()
        _forecast_data = json.loads(forecast_source)
        forecast_list = _forecast_data['list'] if _forecast_data['cnt'] < 24 else _forecast_data['list'][:24]
        forecast_weather = list()
        for weather in forecast_list:
            _tmp = dict()
            _tmp["description"] = weather['weather'][0]['description']
            _tmp["icon"] = "https://www.weatherbit.io/static/img/icons/t"+weather['weather'][0]['icon']+".png"
            _tmp["temp"] = weather['main']['temp']
            _tmp["date_time"] = datetime.fromtimestamp(weather['dt'])
            forecast_weather.append(_tmp)

        data["forecast_weather"] = forecast_weather
        return jsonify(data)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
