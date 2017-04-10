#!/usr/bin/env python

import urllib
import json
import os
import wikipedia
import wolframalpha


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)




@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
   
def processRequest(req):    
    #for wikipedia search
    if req.get("result").get("action") == "wiki":        
        param = req.get("result").get("parameters").get("any")    
        fin = wikipedia.summary(param,sentences=2)    
        res = makeWebhookResult(fin)
        return res
    
    #for wolframalpha
    elif req.get("result").get("action") == "wolf":
        
        try:
            pars = req.get("result").get("resolvedQuery")
            app_id = "4393W5-W6E838H957"
            client = wolframalpha.Client(app_id)
            john = client.query(pars)
            answer = next(john.results).text
            res = makeWebhookResult(answer)
            return res
        except:
            req2 = req.get("result").get("parameters").get("any")
            fin1 = wikipedia.summary(req2,sentences=2)    
            res = makeWebhookResult(fin1)
            return res
            
    #for local time
    elif req.get("result").get("action") == "time":
        app_id = "4393W5-W6E838H957"
        client = wolframalpha.Client(app_id)
        john = client.query("time in bangalore")
        answer = next(john.results).text
        res = makeWebhookResult(answer)
        return res
                   
    #for weather (yahoo api)
    elif req.get("result").get("action") == "yahooWeatherForecast":
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = makeYqlQuery(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib.urlopen(yql_url).read()
        data = json.loads(result)
        res = makeWebhookResult1(data)
        return res

def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    global fl
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"    

def makeWebhookResult(fin):
    speech = fin
    return {
        "speech": speech,
        "displayText": speech,
        
        # "contextOut": [],
        "source": "from my example"
    }

def makeWebhookResult1(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    
    location = channel.get('location')
    
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}


    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + (condition.get('temp')-32)*0.566 + " " + "Fahrenheit"
    
    return {
        "speech": speech,
        "displayText": speech,
        
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
