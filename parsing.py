import requests
import os
from dotenv import load_dotenv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keybord import kb_client, keyboard_tariff, kb_skip, kb_reserv, kb_mask, kb_s


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
ua = UserAgent()
headers = {'User-agent': ua.random}


async def on_startup(_):
    print('Бот вышел в онлайн')


class FSMAdmin(StatesGroup):
    name = State()
    symbol_mask = State()
    tariff = State()
    mask = State()
    reserv = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    global r, session
    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'. format(message.from_user), reply_markup=kb_client)

    url = 'https://store-old.bezlimit.ru/app/login'
    session = requests.Session()
    session.headers.update(headers)
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf-auth'})['value']
    data_authorization = {
        '_csrf-auth': csrf_token,
        'LoginForm[login]': '666666',
        'LoginForm[password]': 'thay1and'
    }
    r = session.post(url, data=data_authorization)

    await bot.send_message(message.from_user.id, 'Бот авторизовался на сайте!')


@dp.message_handler(text=['Фильтр'])
async def filter(message: types.Message, state=FSMContext):

    await bot.send_message(message.from_user.id, 'Введите номер телефона или комбинацию цифр\n'
                                                 'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=kb_mask)
    await FSMAdmin.name.set()


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')
    await bot.send_message(message.from_user.id, '🛑ПЕРЕЗАГРУЗИТЕ БОТА!🛑', reply_markup=kb_client)


@dp.message_handler(state=FSMAdmin.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        if message.text == 'Дальше':
            data['name'] = data['name'].replace('Дальше', '')

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Для ввода используйте A,B,C,N или цифры\n'
                        'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=kb_skip)


@dp.message_handler(state=FSMAdmin.symbol_mask)
async def symbol_mask(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['symbol_mask'] = message.text
        if message.text == 'Пропустить':
            data['symbol_mask'] = data['symbol_mask'].replace('П', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('р', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('о', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('п', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('у', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('с', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('т', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('и', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('т', ' ')
            data['symbol_mask'] = data['symbol_mask'].replace('ь', ' ')

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Введите тариф\n'
                        'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=keyboard_tariff)


@dp.message_handler(state=FSMAdmin.tariff)
async def tariff(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['tariff'] = message.text
        if message.text == 'Без тарифа':
            data['tariff'] = data['tariff'].replace('Без тарифа', '')

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Введите нужную маску, через запятую без пробела!\n'
                        'Например - AAABCBC,NAAABBB\n', reply_markup=kb_mask)

@dp.message_handler(state=FSMAdmin.mask)
async def mask(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['mask'] = message.text
        if message.text == 'Дальше':
            data['mask'] = data['mask'].replace('Дальше', '')

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Бронировать номера?', reply_markup=kb_reserv)


@dp.message_handler(state=FSMAdmin.reserv)
async def reserv(message: types.Message, state: FSMContext):
    global r, session, Flag

    async with state.proxy() as data:
        data['reserv'] = message.text.upper()
        if message.text == 'Yes':
            reserv_num = 'YES'
        else:
            reserv_num = 'NO'

    list_num = []
    page = 1

    url_work = "https://store-old.bezlimit.ru/promo"
    soup_filter = BeautifulSoup(r.content, 'lxml')
    csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
    data_filter = {
        '_csrf-auth': csrf_token_filter,
        'PhonePromoSearch[page]': str(page),
        'PhonePromoSearch[phoneCombs][1]': data['name'],
        'PhonePromoSearch[phoneCombs][2]': '',
        'PhonePromoSearch[phoneCombs][3]': '',
        'PhonePromoSearch[phonePattern][1]': data['symbol_mask'][0].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][2]': data['symbol_mask'][1].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][3]': data['symbol_mask'][2].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][4]': data['symbol_mask'][3].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][5]': data['symbol_mask'][4].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][6]': data['symbol_mask'][5].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][7]': data['symbol_mask'][6].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][8]': data['symbol_mask'][7].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][9]': data['symbol_mask'][8].replace(' ', '').upper(),
        'PhonePromoSearch[phonePattern][10]': data['symbol_mask'][9].replace(' ', '').upper(),
        'PhonePromoSearch[tariffList]': '',
        'PhonePromoSearch[tariffList][]': data['tariff'],
        'PhonePromoSearch[categoryList]': '',
        'PhonePromoSearch[regionList]': '',
        'PhonePromoSearch[maskPattern]': data['mask']
    }
    r_filter = session.post(url_work, data=data_filter)
    soup_filter = BeautifulSoup(r_filter.content, 'lxml')

    while True:
        if len(soup_filter.find_all('div')) < 500:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': '',
                'PhonePromoSearch[phoneCombs][1]': data['name'],
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': data['symbol_mask'][0].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][2]': data['symbol_mask'][1].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][3]': data['symbol_mask'][2].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][4]': data['symbol_mask'][3].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][5]': data['symbol_mask'][4].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][6]': data['symbol_mask'][5].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][7]': data['symbol_mask'][6].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][8]': data['symbol_mask'][7].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][9]': data['symbol_mask'][8].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][10]': data['symbol_mask'][9].replace(' ', '').upper(),
                'PhonePromoSearch[tariffList]': '',
                'PhonePromoSearch[tariffList][]': data['tariff'],
                'PhonePromoSearch[categoryList]': '',
                'PhonePromoSearch[regionList]': '',
                'PhonePromoSearch[maskPattern]': data['mask']
            }
            r_filter = session.post(url_work, data=data_filter)
            soup_filter = BeautifulSoup(r_filter.content, 'lxml')
            number_phone = soup_filter.find_all('div', class_='phone-container')
            for j in number_phone:
                new_phone = j.find('h2').text
                if new_phone not in list_num:
                    sleep(1)
                    await bot.send_message(message.from_user.id, new_phone, parse_mode="Markdown", reply_markup=kb_s)
                    if reserv_num == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    bot_answer = await bot.send_message(message.from_user.id, 'ничего нету', parse_mode="Markdown", reply_markup=kb_s)
                    sleep(3)
                    await bot_answer.delete()
                    break

        if len(soup_filter.find_all('div')) > 500:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': str(page),
                'PhonePromoSearch[phoneCombs][1]': data['name'],
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': data['symbol_mask'][0].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][2]': data['symbol_mask'][1].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][3]': data['symbol_mask'][2].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][4]': data['symbol_mask'][3].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][5]': data['symbol_mask'][4].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][6]': data['symbol_mask'][5].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][7]': data['symbol_mask'][6].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][8]': data['symbol_mask'][7].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][9]': data['symbol_mask'][8].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][10]': data['symbol_mask'][9].replace(' ', '').upper(),
                'PhonePromoSearch[tariffList]': '',
                'PhonePromoSearch[tariffList][]': data['tariff'],
                'PhonePromoSearch[categoryList]': '',
                'PhonePromoSearch[regionList]': '',
                'PhonePromoSearch[maskPattern]': data['mask']
            }
            r_filter = session.post(url_work, data=data_filter)
            soup_filter = BeautifulSoup(r_filter.content, 'lxml')
            number_phone = soup_filter.find_all('div', class_='phone-container')
            for j in number_phone:
                new_phone = j.find('h2').text
                if new_phone not in list_num:
                    sleep(1)
                    await bot.send_message(message.from_user.id, new_phone, parse_mode="Markdown", reply_markup=kb_s)
                    if reserv_num == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    bot_answer = await bot.send_message(message.from_user.id, 'ничего нету', parse_mode="Markdown", reply_markup=kb_s)
                    sleep(3)
                    await bot_answer.delete()
                    break
            page += 1

        if len(soup_filter.find_all('div')) <= 82:
            bot_answer = await bot.send_message(message.from_user.id, 'ничего нету', parse_mode="Markdown", reply_markup=kb_s)
            sleep(3)
            await bot_answer.delete()

        if page >= 20:
            page = 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)