#!/usr/bin/env python
import urllib
import json
import os
import wikipedia
import wolframalpha
import sys
from microsofttranslator import Translator
import requests
import random

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
    #for wolfram alpha
    if req.get("result").get("action") == "fact":
        client = wolframalpha.Client("4393W5-W6E838H957")
        john = client.query("what is the capital of china")
        answer = next(john.results).text
        return {
        "speech": answer,
        "displayText": answer,
        "source": "From wolfram_alpha"
        }
    
    #translator
    elif req.get("result").get("action") == "tran":
        translator = Translator('''jkthaha''', '''syosNIlEOJnlLByQGcMS+AIin0iaNERaQVltQvJS6Jg=''')
        try:
            s = translator.translate(req.get("result").get("parameters").get("question"),req.get("result").get("parameters").get("language"))
            res = makeWebhookResult(s)
            return res
        except:
            res = makeWebhookResult("Server busy, please try again later")
            return res
    
    #for news
    elif req.get("result").get("action") == "news":
        y = random.randint(1,6)
        if y == 1:
            r = requests.get('https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res
        
        elif y==2:
            r = requests.get('https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res       
        
        elif y==3:
            r = requests.get('https://newsapi.org/v1/articles?source=independent&sortBy=top&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res
        
        elif y==4:
            r = requests.get('https://newsapi.org/v1/articles?source=bbc-sport&sortBy=top&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines from bbc sports: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res
        
        elif y==5: 
            r = requests.get('https://newsapi.org/v1/articles?source=ars-technica&sortBy=latest&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res
        
        elif y==6:
            r = requests.get('https://newsapi.org/v1/articles?source=the-hindu&sortBy=latest&apiKey=1412588264c447da83a7c75f1749d6e8')
            j = r.json()
            x = j.get('articles')
            newp = "The headlines are: "+"1. "+x[0]["title"]+"." +" 2. "+x[1]["title"]+"."+" 3. "+x[2]["title"]+"."+" 4. "+x[3]["title"]+"."+" 5. "+x[4]["title"]+"." 
            res = makeWebhookResult(newp)
            return res
        
    #for wikipedia
    elif req.get("result").get("action") == "wiki":    
        param = req.get("result").get("parameters").get("any")    
        fin = wikipedia.summary(param,sentences=2)    
        res = makeWebhookResult(fin)
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

    cels = (int(condition.get('temp'))-32)*0.566
    cels = int(cels)
    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + str(cels) + " " + "Degree Celsius"
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    

    app.run(debug=False, port=port, host='0.0.0.0')
