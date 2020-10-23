# Subscribe open data with LINE Bot/Notify/LIFF

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-%3E%3D%203.5-blue.svg)](https://badge.fury.io/py/lotify)

The bot provides subscribing and notifying [open data - air pollution](http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json).

Using `所有縣市` trigger and start bot.

It builds by:

- flask/Python 3.8
- LINE v10.12
- LINE Notify
- LINE Login/LIFF v2.3
- PostgreSQL

> You need Github, LINE, Heroku accounts to deploy this bot.

# Developer Side

## Environment property

These properties are need to export in environment.

```
LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
LINE_NOTIFY_CLIENT_ID=
LINE_NOTIFY_CLIENT_SECRET=
LINE_NOTIFY_REDIRECT_URI=
LIFF_BIND_ID=
LIFF_CONFIRM_ID=
LIFF_SHARE_ID=
DATABASE_URL=postgres://USER:PASSWORD@127.0.0.1:5432/postgres
```

## LINE account (LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET)

- Got A LINE Bot API developer account
  Make sure you already registered, if you need use LINE Bot.

* Go to LINE Developer Console
  - Close auto-reply setting on "Messaging API" Tab.
  - Setup your basic account information. Here is some info you will need to know.
    - Callback URL: `https://{YOUR_URL}/webhooks/line`
    - Verify your webhook.
* You will get following info, need fill back to `.env` file.
  - Channel Secret
  - Channel Access Token (You need to issue one here)

## LIFF (LIFF_BIND_ID & LIFF_CONFIRM_ID)

- Input `https://{YOUR_URL}/notify` into binding LIFF app.
- Input `https://{YOUR_URL}/notify/callback` into callback LIFF app.

![](https://i.imgur.com/yvldqPA.png)

## LINE notify

- Input your key into `LINE_NOTIFY_CLIENT_ID` and `LINE_NOTIFY_CLIENT_SECRET`

![](https://i.imgur.com/SZG7Re6.png)

- Copy `callback LIFF app` url to NOTIFY callback url column.

![](https://i.imgur.com/VGaKILZ.png)

## Local testing

1. first terminal window

```
cp .env.example .env
pip install -r requirements.txt --user
python api.py
```

2. Create a provisional Https:

```
ngrok http 5000
```

or maybe you have npm environment:

```
npx ngrok http 5000
```

![](https://i.imgur.com/azVdG8j.png)

3. Copy url to LINE Developer Console

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Click `Configure Add-ons` and input `Heroku Scheduler` to install scheduler.

![](https://i.imgur.com/cval2jv.png)

- Add two jobs on `Heroku Schedular`:

  - `python scripts/sync_to_sql.py`
  - `python scripts/notify_me.py`

- Add `Heroku Postgres` and it would create `DATABASE_URL` environment variable automatically.

![](https://i.imgur.com/wCFeUlu.png)

If you are not sure where are files in, use following up commands:

```
heroku run bash
heroku logs --tail
```

# Generator

You need to install `openapi-generator`, and use the following command to generate the SDK.(example is JavaScript)

```
openapi-generator generate -i https://{YOUR_URL}.herokuapp.com/api/swagger.json -g javascript -o lotifySampleApi
cd lotifySampleApi
npm install
npm run build
```

Push to your Repository Center(e.g. GitHub, GitLab).

Then you can install it by git.

# License

MIT License
