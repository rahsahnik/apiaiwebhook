#!/usr/bin/env python

import urllib
import json
import os
import wikipedia


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
    if req.get("result").get("action") != "wiki":        
        return {}
    
    param = req.get("result").get("parameters").get("par1")
    
    fin = wikipedia.summary(param,sentences=1)
    
    res = makeWebhookResult(fin)
    return res


def makeWebhookResult(fin):
    speech = fin
    return {
        "speech": speech,
        "displayText": speech,
        
        # "contextOut": [],
        "source": "from my example"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
