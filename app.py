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
from PyDictionary import PyDictionary

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
        john = client.query(req.get("result").get("resolvedQuery"))
        answer = next(john.results).text
        return {
        "speech": answer,
        "displayText": answer,
        "source": "From wolfram_alpha"
        }
    
    #translator
    #uses microsoft translator api USE your key here
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
    #takes news randomly from different sources use newsapi docs for more info
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
    
    #for dictionary
    else:
        dictionary = PyDictionary()
        ch = req.get('result').get('parameters').get('word')
        test = req.get('result').get('parameters').get('dictionary')
        if test == 'antonym':
            res = dictionary.antonym(ch)
            try:
                try:
                    answer = "Antonym for the word " + ch +" are: {0}, {1}, {2}, {3}, {4}.".format(res[0],res[1],res[2],res[3],res[4])            
                except:
                    try:
                        answer = "Antonym for the word " + ch + " are: {0}, {1}, {2}, {3}.".format(res[0], res[1], res[2], res[3])
                    except:
                        try:
                            answer = "Antonym for the word " + ch + " are: {0}, {1}, {2}.".format(res[0], res[1], res[2])

                        except:
                            answer= "Antonym for the word " + ch + " are: {0}, {1}.".format(res[0], res[1])

            except:
                answer = "There is no antonym for this word"
            return makeWebhookResult(answer)

        elif test=='definition':
            re1s = dictionary.meaning(ch)
            try:
                answer = "The word {0} is a verb and its meaning is {1}".format(ch,re1s['Verb'])
            except:
                answer = "The word {0} is a noun and its meaning is {1}".format(ch, re1s['Noun'])
            return makeWebhookResult(answer)    

        elif test=='synonym':
            res = dictionary.synonym(ch)
            try:
                try:
                    answer = "Synonym for the word " + ch + " are: {0}, {1}, {2}, {3}, {4}.".format(res[0], res[1], res[2],
                                                                                            res[3], res[4])
                except:
                    try:
                        answer = "Synonym for the word " + ch + " are: {0}, {1}, {2}, {3}.".format(res[0], res[1], res[2],
                                                                                           res[3])
                    except:
                        try:
                            answer = "Synonym for the word " + ch + " are: {0}, {1}, {2}.".format(res[0], res[1], res[2])
                        except:
                            answer = "Synonym for the word " + ch + " are: {0}, {1}.".format(res[0], res[1])
                return makeWebhookResult(answer)
            except:
                answer = "There is no Synonym for this word"
                return makeWebhookResult(answer)        

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
        "source": "from jkthaha webhook"
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
        "source": "apiai webhook jkthaha"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    

    app.run(debug=False, port=port, host='0.0.0.0')
