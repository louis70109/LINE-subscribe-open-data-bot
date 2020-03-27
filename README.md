
# LINE Icon Switch API sample

LINE new API - [Icon Switch](https://developers.line.biz/zh-hant/reference/messaging-api/#icon-nickname-switch): this API can change icon and display name in same **LINE BOT**

# Trigger text
This bot will catch trigger text to change name and avatar !!🎉
- Sally
- Brown
- Cony

![](https://i.imgur.com/TbtdNFjl.png)

# Developer Side

## LINE account

- Got A LINE Bot API devloper account
Make sure you already registered, if you need use LINE Bot.


- Go to LINE Developer Console
    - Close auto-reply setting on "Messaging API" Tab.
    - Setup your basic account information. Here is some info you will need to know.
        - Callback URL: `https://{NGROK_URL}/webhooks/line`
        - Verify your webhook.
- You will get following info, need fill back to `.env` file.
    - Channel Secret
    - Channel Access Token (You need to issue one here)

## Normal testing

1. first terminal window
```
pip install -r requirements.txt --user
python api.py
```

> [2020/03/28] LINE just not already release tag in SDK, so I use git method to install NEW feature package(icon switch).
2. Create a provisional Https:

```
ngrok http 5000
```

or maybe you have npm enviroment:

```
npx ngrok http 5000
```
![](https://i.imgur.com/azVdG8j.png)

3. Copy url to LINE Developer Console

## If you have AWS account
1. Install serverless via npm:

```bash=
$ npm install -g serverless
```

2. Setup your **AWS** ceritficate

```bash=
export AWS_ACCESS_KEY_ID=<your-key-here>
export AWS_SECRET_ACCESS_KEY=<your-secret-key-here>
```

3. Deploy the example:

```bash=
npm install
pip install -r requirements.txt --user
serverless wsgi serve # local testing
serverless deploy     # deploy to AWS
```

4. If deploy, copy the url to LINE Developer Console
# License

MIT License

