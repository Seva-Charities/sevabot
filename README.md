# Seva Slack Bot

The Seva Slack Bot is a slackbot written in python with the Slack Bolt SDK for the UT Seva Charities Team.

## Setting up your dev environment

> Note: Dev Testing is done through ngrok

Use a virtual environment to install necessary dependencies.

```bash
mkdir sevabot
cd sevabot
python3 -m venv venv
source venv/bin/activate
```

Clone the repository into your `sevabot` directory and install dependencies.
```bash
git clone https://github.com/neil-sriv/sevabot.git
pip3 install -r requirements.txt
touch .env
```

Fill your `.env` file with the following information:
```text
SLACK_SIGNING_SECRET='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SLACK_BOT_TOKEN='xoxb-xxxxxxxxxxxxxx-xxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx'
ENV='development'
```

### ngrok installation
Use homebrew to install ngrok

```bash
brew install ngrok
```

### ngrok usage
ngrok can be used to spin up public urls for testing

```bash
ngrok http 3000
```


## Dev Testing
- Make sure that the `ENV` variable in your `.env` file is set to `'development'`
- Spin up an `ngrok` instance on port `3000`
- run your `app.py` function
```bash
python3 app.py
```
- make your changes to endpoints and listeners as desired
- change the the url for any commands or event listeners you change on https://api.slack.com/apps/A01CTPM0ZUZ to `<ngrok-url>/slack/testing`
- make sure to change event subscriptions link back to heroku https://seva-slack-bot.herokuapp.com/slack/events

## Deploying to Heroku


```bash
heroku login
git remote add heroku https://git.heroku.com/seva-slack-bot.git

heroku config:set SLACK_BOT_TOKEN=<SLACK_BOT_TOKEN>
heroku config:set SLACK_SIGNING_SECRET=<SLACK_SIGNING_SECRET>

git add .
git commit -m 'Initial commit for my awesome Slack app'
git push heroku master
```