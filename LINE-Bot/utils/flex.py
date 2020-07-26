from utils.db import find_user_site


def create_county_flex(line_id, county, site, status, update_time):
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
                                    "text": "狀態",
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
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
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
                "label": "查詢其他區域",
                "text": "所有區域"
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
            "type": "spacer",
            "size": "sm"
        }]
    else:
        return [{
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
                "type": "message",
                "label": "查詢其他區域",
                "text": "所有區域"
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
            "type": "spacer",
            "size": "sm"
        }]


def counties_template(counties):
    contents, total = [], []
    counties_len = len(counties)
    for index in range(counties_len):
        if (index+1) == counties_len:
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