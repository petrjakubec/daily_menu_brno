from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    botanic = botanic_menu()
    mediteran = mediteran_menu()

    return render_template('home.html', botanic=botanic, mediteran=mediteran)


def botanic_menu():
    url = 'https://www.botanicbar.cz/#menu'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    menu_items = soup.find_all('h4', class_='menu-item-heading')
    menu_text = [item.text for item in menu_items[-9:-6]]

    return menu_text


def mediteran_menu():
    url = 'https://www.mediteranbistro.cz/cs/poledni-menu'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    weekday = datetime.datetime.today().weekday()
    days = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek']

    if weekday < 5:
        menu_header = soup.find('h3', string=days[weekday])
        menu_list = menu_header.find_next('div', {'role': 'list', 'class': 'w-dyn-items'})
        menu_items = menu_list.find_all('div', {'role': 'listitem'})
        menu_text = [item.text.strip() for item in menu_items]

        return menu_text


if __name__ == '__main__':
    app.run(debug=True)