import os
import telebot
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['usd'])
def send_economy(message):
    def scrape_dollar(url, item_type, item_name):
        # Make a request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the li element with the specified class and data attributes
            li_element = soup.find('li', {'class': 'active', 'data-item-type': item_type, 'data-item-name': item_name})

            # Check if the li element is found
            if li_element:
                # Find the span element with the class 'value'
                value_span = li_element.find('span', {'class': 'value'})

                # Check if the value span is found
                if value_span:
                    # Extract and return the text content of the value span
                    return value_span.text.strip()
                else:
                    return "Value span not found."
            else:
                return "Li element not found."
        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"

    # Replace this URL with the actual URL you want to scrape
    url_to_scrape = "https://www.df.cl/app_df/frontend/modules/index.php?modulo=cd&accion=Inicio"

    # Replace these values with the actual item type and item name you want to scrape
    item_type_to_find = "bolsas"
    item_name_to_find = "Dólar EE.UU."

    # Call the function and print the result
    result = scrape_dollar(url_to_scrape, item_type_to_find, item_name_to_find)
    print(result)

    info = f"The df's dollar to clp price is {result} \n"
    bot.reply_to(message, info)


# Geo location: [-33.3667, -70.5167]
@bot.message_handler(commands=['a'])
def send_weather(message):
    weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={-33.3667}&lon={-70.5167}&units=metric&appid={API_KEY_WEATHER}").json()
    # weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Santiago&units=metric&appid={API_KEY_WEATHER}")
    # weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={-33.3667}&lon={-70.5167}&exclude=current,minutely,hourly&appid={API_KEY_WEATHER}").json()
    print('----------------------------')
    print(weather_data)
    # print(weather_data['weather'][0]['main'])
    # print(weather_data['main']['temp'])
    info = "This is a bot to help you with your economy. \n"
    bot.reply_to(message, info)


bot.infinity_polling()
