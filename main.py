import requests
import json
import time
import const


def answer_user_bot(data, user_id):
    data = {
        'chat_id': user_id,
        'text': data
    }
    url = const.URL.format(
        token=const.TOKEN,
        method=const.SEND_METH
    )
    response = requests.post(url, data=data)


def parse_weather_data(data):
    for elem in data['weather']:
        weather_state = elem['main']
    temp = round(data['main']['temp'] - 273.15, 0)
    feel = round(data['main']['feels_like'] - 273.15, 0)
    city = data['name']
    country = data["sys"]["country"]
    msg = f'The weather in {city}, {country}: Temp is {temp}°C, feels like {feel}°C' \
          f' \nState is {weather_state}'
    return msg


def get_weather(location):
    url = const.WEATHER_URL.format(city=location,
                                   token=const.WEATHER_TOKEN)
    response = requests.get(url)
    if response.status_code != 200:
        return 'City not found, try again.'
    data = json.loads(response.content)
    return parse_weather_data(data)


def get_message(data):
    return data['message']['text'].lower()


def save_update_id(update):
    with open(const.UPDATE_ID_FILE_PATH, 'w') as file:
        file.write(str(update['update_id']))
    const.UPDATE_ID = update['update_id']
    return True


def get_content():
    url = const.URL.format(token=const.TOKEN, method=const.UPDATE_METH)
    content = requests.get(url).text
    data = json.loads(content)
    result = data['result'][::-1]
    return result[0]


def main():
    while True:
        needed_part = get_content()
        user_id = needed_part["message"]["chat"]["id"]
        if const.UPDATE_ID != needed_part['update_id']:
            message = get_message(needed_part)
            if message == "/start":
                answer_user_bot("Hello, i`m the Weather bot. Type the name of the city u want"
                                "to know weather. Example: London", user_id)
                save_update_id(needed_part)
                continue
            msg = get_weather(message)
            answer_user_bot(msg, user_id)
            save_update_id(needed_part)

        time.sleep(1)


if __name__ == '__main__':
    main()
