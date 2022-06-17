
import json
import urllib.request
from flask import Flask, render_template, abort, request, jsonify

app = Flask(__name__)

@app.route('/')
def weather():  # put application's code here
    results = urllib.request.urlopen('https://raw.githubusercontent.com/eesur/country-codes-lat-long/master/country-codes-lat-long-alpha3.json').read()
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
    api_key = '1f88cf5ad23f2d0ec9f6613c4508ef8c'
    params = request.json()
    print(params)

    try:
        # source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid='+api_key).read()
        pass
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
