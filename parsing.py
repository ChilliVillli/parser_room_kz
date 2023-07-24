import requests
from bs4 import BeautifulSoup
from time import sleep
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token='5601906129:AAH1k-asnKub2yCS36TUmjHMUlr9UtcarW4')
dp = Dispatcher(bot)

async def on_startup(_):
    print('Бот вышел в онлайн')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'. format(message.from_user))


@dp.message_handler(text=['go'])
async def parsing_room(message: types.Message):
    list_url = []
    url = "https://krisha.kz/prodazha/kvartiry/almaty/"
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # page = soup.find("nav", class_="paginator").text.split()
    # page = int(page[-2])

    for count in range(1):  # int(page)+1  ## page + 1

        while True:
            sleep(3)
            if count == 1:
                url = "https://krisha.kz/prodazha/kvartiry/almaty/"
            # else:
            #     url = f'https://krisha.kz/prodazha/kvartiry/almaty/?page={count}'

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            for i in soup.find_all("div", class_="a-card__inc"):
                sleep(3)
                try:
                    card_url = "https://krisha.kz" + i.find("a", class_="a-card__image tm-click-checked-hot-adv").get("href")
                    if card_url not in list_url:
                        response_hot = requests.get(card_url, headers=headers)
                        soup_hot = BeautifulSoup(response_hot.text, 'lxml')
                        data_hot = soup_hot.find("div", class_="layout__container main-col a-item")
                        try:
                            img = data_hot.find("picture").find("img").get("src")
                            name = data_hot.find("picture").find("img").get("alt")
                        except AttributeError:
                            img = 'No foto'
                            name = data_hot.find("h1").text
                        # print(img, name, card_url, sep='\n')
                        await bot.send_message(message.from_user.id, f"[.]({img})\n{name}\n{card_url}", parse_mode="Markdown")
                        list_url.append(card_url)
                    else:
                        continue
                except AttributeError:
                    card_url = "https://krisha.kz" + i.find("a", class_="a-card__image").get("href")
                    if card_url not in list_url:
                        response_ordinary = requests.get(card_url, headers=headers)
                        soup = BeautifulSoup(response_ordinary.text, 'lxml')
                        data_ordinary = soup.find("div", class_="layout__container main-col a-item")
                        try:
                            img = data_ordinary.find("picture").find("img").get("src")
                            name = data_ordinary.find("picture").find("img").get("alt")
                        except AttributeError:
                            img = 'No foto'
                            name = data_hot.find("h1").text
                        # print(img, name, card_url, sep='\n')
                        await bot.send_message(message.from_user.id, f"[.]({img})\n{name}\n{card_url}", parse_mode="Markdown")
                        list_url.append(card_url)
                    else:
                        continue
                if len(list_url) > 70:
                    del list_url[-1]

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)