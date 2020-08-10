from utils.db import find_user_site


def county_flex_template(county, site, status, update_time):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": county,
                    "weight": "bold",
                    "size": "xl",
                    "decoration": "underline",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "區域",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": site,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "空氣",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": status,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "時間",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": update_time,
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 5
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }


def create_county_flex(line_id, county, site, status, update_time):
    return {
        **county_flex_template(county, site, status, update_time),
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "flex": 0,
            "contents": check_user_subscribe_site(line_id=line_id, site=site)
        }
    }


def check_user_subscribe_site(line_id, site):
    sub_site = False
    row = find_user_site(line_id, site)
    if row:
        sub_site = True
    if sub_site:
        return [{
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "查詢",
                "text": "所有縣市"
            }
        }, {
            "type": "button",
            "style": "secondary",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "取消訂閱",
                "text": f"取消訂閱 {site}"
            }
        }, {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": "分享",
                "uri": f"https://liff.line.me/1622939248-JYQqZerE?site={site}"
            }
        }]
    else:
        return [{
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "查詢",
                "text": "所有縣市"
            }
        }, {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "訂閱",
                "text": f"訂閱 {site}"
            }
        }, {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "uri",
                "label": "分享",
                "uri": f"https://liff.line.me/1622939248-JYQqZerE?site={site}"
            }
        }]


def counties_template(counties):
    contents, total = [], []
    counties_len = len(counties)
    for index in range(counties_len):
        if (index + 1) == counties_len:
            contents.append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": counties[index]['county'],
                    "text": counties[index]['county']
                }
            })
            total.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents
                }
            })
        elif (index + 1) % 6 != 0:
            contents.append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": counties[index]['county'],
                    "text": counties[index]['county']
                }
            })
        else:
            contents.append({
                "type": "button",
                "action": {
                    "type": "message",
                    "label": counties[index]['county'],
                    "text": counties[index]['county']
                }
            })
            total.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents
                }
            })
            contents = []

    return total


def bind_notify_content(url):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "🔔 您尚未綁定 LINE Notify\n綁定後即可收到推播訊息 ⬇️",
                    "size": "xl",
                    "align": "center",
                    "wrap": True
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "點我綁定",
                        "uri": url
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
            ],
            "flex": 0
        }
    }
