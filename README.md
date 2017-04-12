# Api.ai - multiple webhook simulation implementation in Python

This python code takes the input json from the api.ai agent and processes the query based on the action specified in the json file,
It uses wikipedia api for basic information retrieval and wolfram alpha api for general facts and questions

#pre-requisites
1. API.AI account and a functional agent
2. wolfram alpha account to get the app id [watch online tutorials on how to get wolfram alpha app id]
3. Heroku account to host the app.py file

NOTE
Substitute the app_id variable in the app.py file with your app_id from wolframalpha page and intents for api calls should contain the action "wiki" for wikipedia search and "wolf" for wolfram alpha search and YahooWeatherForecast for weather report.


More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a weather information fulfillment service that uses [Yahoo! Weather API](https://developer.yahoo.com/weather/) and basic web search 
using mediawiki api or wolfram alpha api.
The services takes the `geo-city` parameter from the action, performs geolocation for the city and requests weather information from Yahoo! Weather public API and takes par1 parameter for the wikipedia search.
Change the parameter you pass from the intents in api.ai and keep the same parameters name while you retrieve the parameters ex:
param = req.get("result").get("parameters").get("Your_parameter_name")

The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.
