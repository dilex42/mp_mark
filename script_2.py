import requests
import json
import asyncio


def check_rate(response):
    cur_timestamp = response["timestamp"]
    cur_rate = response["rates"]["UAH"]
    print(f"Current rate is {cur_rate}")
    with open("storage_kinda.txt", "r+") as json_file:
        try:
            data = json.load(json_file)
        except json.decoder.JSONDecodeError:
            json_file.seek(0)
            json.dump({"rate": 0, "timestamp": 0}, json_file)
            json_file.truncate()
            check_rate(response)
        else:
            past_timestamp = data["timestamp"]
            if cur_timestamp > past_timestamp:
                past_rate = data["rate"]
                if cur_rate > past_rate:
                    telegram_bot_sendtext(
                        f"New exchange rate !!! {cur_rate} instead of {past_rate}"
                    )
                    json_file.seek(0)
                    json.dump(
                        {"rate": cur_rate, "timestamp": cur_timestamp},
                        json_file,
                    )
                    json_file.truncate()


def pool_rate():
    print("Pooling rate...")
    URL = "http://data.fixer.io/api/latest"
    access_key = "9d04dbafbd54014c011cceee92fd5af7"

    response = requests.get(
        f"{URL}?access_key={access_key}&symbols=UAH"
    ).json()
    if response["success"]:
        check_rate(response)
    else:
        print(f"Something went wrong {response}")


def telegram_bot_sendtext(bot_message):

    bot_token = "1879542866:AAGtwaTfbkt5PgeiNMJLqbdfpPbSloC1GHI"
    # find @mp_mark_dilex_bot and send /start
    # find @userinfobot and send /start to get your chatID
    bot_chatID = "YOUR CHAT ID"
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}"

    response = requests.get(send_text)

    return response.json()


async def periodic():
    sleep_min = 0.1
    while True:
        try:
            pool_rate()
            print(f"Going to sleep for {sleep_min} minute(s)")
        except Exception as err:
            print(err)
            print(
                f"!!! Something went wrong !!! Retrying in {sleep_min} minute(s)"
            )
        await asyncio.sleep(sleep_min * 60)


loop = asyncio.get_event_loop()
task = loop.create_task(periodic())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
