import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler

def get_weather_info():
    # 这里编写获取天气信息的代码，比如调用天气 API
    # 返回包含天气相关信息的字典，例如 {'weather': '晴', 'temp': '25℃'}
    return weather_data

def send_wechat_message(weather_info, appid, secret, template_id, openid):
    access_token = get_access_token(appid, secret)
    data = {
        "touser": openid,
        "template_id": template_id,
        "data": {
            # 根据你的模板内容，填充相应的参数值
            "date": {"value": "今天的日期"},
            "region": {"value": "所在地区"},
            "weather": {"value": weather_info['weather']},
            "temp": {"value": weather_info['temp']}
        }
    }
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=" + access_token
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("消息推送成功")
    else:
        print("消息推送失败：", response.text)

def get_access_token(appid, secret):
    token_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret
    response = requests.get(token_url)
    if response.status_code == 200:
        result = response.json()
        if "access_token" in result:
            return result["access_token"]
    return None

def main():
    # 你的微信测试号的 appid、secret、模板 ID 和接收消息的用户 OpenID
    appid = "wx30afd0b702ac0971"
    secret = "541b2c5093cc822ec0e5746f5792002b"
    template_id = "ibHTxtRJdrPDSTmdTk7NWPvFo84W5SLHrsQbqpI2L8k"
    openid = "o3m8S6wC_BzGi2xQj72FuFKFegAg"
    weather_info = get_weather_info()
    send_wechat_message(weather_info, appid, secret, template_id, openid)

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 每天早上 8 点执行一次消息推送
    scheduler.add_job(main, 'cron', hour=8)
    scheduler.start()
