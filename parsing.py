import asyncio
import requests
import sqlite3 as sq
import os
from dotenv import load_dotenv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
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
    sql_start()


class FSMAdmin(StatesGroup):
    name = State()
    symbol_mask = State()
    tariff = State()
    mask = State()
    reserv = State()
    stop = State()

def sql_start():
    global base, cur
    base = sq.connect('filter.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS fil(num TEXT, symbol_mask TEXT, tariff TEXT, mask TEXT, reserv TEXT)')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    global r, session, flag
    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'. format(message.from_user), reply_markup=kb_client)

    url = 'https://store-old.bezlimit.ru/app/login'
    session = requests.Session()
    session.headers.update(headers)
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', {'name': '_csrf-auth'})['value']
    data_authorization = {
        '_csrf-auth': csrf_token,
        'LoginForm[login]': '519891',  #666666 thay1and
        'LoginForm[password]': '4qt'
    }
    r = session.post(url, data=data_authorization)
    flag = True
    await bot.send_message(message.from_user.id, 'Бот авторизовался на сайте!')


@dp.message_handler(text=['Фильтр'])
async def filter(message: types.Message, state=FSMContext):

    await bot.send_message(message.from_user.id, 'Введите номер телефона или комбинацию цифр\n'
                                                 'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=kb_mask)
    await FSMAdmin.name.set()



@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    global flag
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    flag = False
    await message.reply('OK')
    await bot.send_message(message.from_user.id, '🛑Перезагрузите бота🛑', reply_markup=kb_client)


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
    global flag
    async with state.proxy() as data:
        data['reserv'] = message.text.upper()

    async with state.proxy() as data:
        cur.execute('INSERT INTO fil VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()

    for ret in cur.execute('SELECT * FROM fil').fetchall():
        num = ret[0]
        sym_mask = ret[1]
        trf = ret[2]
        msk = ret[3]
        rev = ret[4]

    list_num = []
    page = 1

    if rev == 'YES':
        await message.reply('Бот набирает базу номеров...')
        url_work = "https://store-old.bezlimit.ru/promo"
        soup_filter = BeautifulSoup(r.content, 'lxml')
        csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
        data_filter = {
            '_csrf-auth': csrf_token_filter,
            'PhonePromoSearch[page]': str(page),
            'PhonePromoSearch[phoneCombs][1]': num,
            'PhonePromoSearch[phoneCombs][2]': '',
            'PhonePromoSearch[phoneCombs][3]': '',
            'PhonePromoSearch[phonePattern][1]': sym_mask[0].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][2]': sym_mask[1].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][3]': sym_mask[2].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][4]': sym_mask[3].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][5]': sym_mask[4].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][6]': sym_mask[5].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][7]': sym_mask[6].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][8]': sym_mask[7].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][9]': sym_mask[8].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][10]': sym_mask[9].replace(' ', '').upper(),
            'PhonePromoSearch[tariffList]': '',
            'PhonePromoSearch[tariffList][]': trf,
            'PhonePromoSearch[categoryList]': '',
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.post(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')
        numbers_base = soup_filter.find_all('div', class_='phone-container')
        for i in numbers_base:
            num_base = i.find('h2').text
            list_num.append(num_base)
        await message.reply(f'Бот собрал {len(list_num)} номер')
    if rev == 'NO':
        url_work = "https://store-old.bezlimit.ru/promo"
        soup_filter = BeautifulSoup(r.content, 'lxml')
        csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
        data_filter = {
            '_csrf-auth': csrf_token_filter,
            'PhonePromoSearch[page]': str(page),
            'PhonePromoSearch[phoneCombs][1]': num,
            'PhonePromoSearch[phoneCombs][2]': '',
            'PhonePromoSearch[phoneCombs][3]': '',
            'PhonePromoSearch[phonePattern][1]': sym_mask[0].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][2]': sym_mask[1].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][3]': sym_mask[2].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][4]': sym_mask[3].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][5]': sym_mask[4].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][6]': sym_mask[5].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][7]': sym_mask[6].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][8]': sym_mask[7].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][9]': sym_mask[8].replace(' ', '').upper(),
            'PhonePromoSearch[phonePattern][10]': sym_mask[9].replace(' ', '').upper(),
            'PhonePromoSearch[tariffList]': '',
            'PhonePromoSearch[tariffList][]': trf,
            'PhonePromoSearch[categoryList]': '',
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.post(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')


    while flag != False:
        await asyncio.sleep(5)

        if len(soup_filter.find_all('div')) <= 82:
            continue

        if len(soup_filter.find_all('div')) <= 3583:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': '',
                'PhonePromoSearch[phoneCombs][1]': num,
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': sym_mask[0].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][2]': sym_mask[1].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][3]': sym_mask[2].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][4]': sym_mask[3].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][5]': sym_mask[4].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][6]': sym_mask[5].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][7]': sym_mask[6].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][8]': sym_mask[7].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][9]': sym_mask[8].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][10]': sym_mask[9].replace(' ', '').upper(),
                'PhonePromoSearch[tariffList]': '',
                'PhonePromoSearch[tariffList][]': trf,
                'PhonePromoSearch[categoryList]': '',
                'PhonePromoSearch[regionList]': '',
                'PhonePromoSearch[maskPattern]': msk
            }
            r_filter = session.post(url_work, data=data_filter, headers=headers)
            soup_filter = BeautifulSoup(r_filter.content, 'lxml')
            number_phone = soup_filter.find_all('div', class_='phone-container')
            for j in number_phone:
                new_phone = j.find('h2').text
                if new_phone not in list_num:
                    await asyncio.sleep(1)
                    await bot.send_message(message.from_user.id, new_phone, reply_markup=kb_s)
                    if rev == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    continue

        elif len(soup_filter.find_all('div')) >= 3584:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': str(page),
                'PhonePromoSearch[phoneCombs][1]': num,
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': sym_mask[0].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][2]': sym_mask[1].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][3]': sym_mask[2].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][4]': sym_mask[3].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][5]': sym_mask[4].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][6]': sym_mask[5].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][7]': sym_mask[6].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][8]': sym_mask[7].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][9]': sym_mask[8].replace(' ', '').upper(),
                'PhonePromoSearch[phonePattern][10]': sym_mask[9].replace(' ', '').upper(),
                'PhonePromoSearch[tariffList]': '',
                'PhonePromoSearch[tariffList][]': trf,
                'PhonePromoSearch[categoryList]': '',
                'PhonePromoSearch[regionList]': '',
                'PhonePromoSearch[maskPattern]': msk
            }
            r_filter = session.post(url_work, data=data_filter, headers=headers)
            soup_filter = BeautifulSoup(r_filter.content, 'lxml')
            number_phone = soup_filter.find_all('div', class_='phone-container')
            for j in number_phone:
                new_phone = j.find('h2').text
                if new_phone not in list_num:
                    await asyncio.sleep(1)
                    await bot.send_message(message.from_user.id, new_phone, reply_markup=kb_s)
                    if rev == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    continue
            page += 1

        elif page >= 20:
            page = 1

        elif flag == False:
            break


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)