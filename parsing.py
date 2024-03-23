import asyncio
import sqlite3
import requests
import sqlite3 as sq
import os
from dotenv import load_dotenv
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keybord import kb_client, keyboard_tariff, kb_skip, kb_reserv, kb_mask, kb_s, keyboard_category, kb_authoriz


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
    category = State()
    tariff = State()
    mask = State()
    reserv = State()


class authorization(StatesGroup):
    login = State()
    password = State()


def sql_start():
    global base, cur, curr, basee, cur_lp, base_lp
    base = sq.connect('filter.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS fil(num TEXT, symbol_mask TEXT, category TEXT, tariff TEXT, mask TEXT, reserv TEXT)')

    basee = sq.connect('filter.db')
    curr = basee.cursor()
    basee.execute('CREATE TABLE IF NOT EXISTS fill(num TEXT, category TEXT, tariff TEXT, mask TEXT, reserv TEXT)')

    base_lp = sq.connect('filter.db')
    cur_lp = base_lp.cursor()
    base_lp.execute('CREATE TABLE IF NOT EXISTS authoriz(login TEXT, password TEXT)')



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    global r, session, flag
    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'. format(message.from_user))

    for ret in cur_lp.execute('SELECT * FROM authoriz ORDER BY rowid DESC LIMIT 1'):

        url = 'https://store-old.bezlimit.ru/app/login'
        session = requests.Session()
        session.headers.update(headers)
        r = session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf-auth'})['value']
        data_authorization = {
            '_csrf-auth': csrf_token,
            'LoginForm[login]': ret[0],
            'LoginForm[password]': ret[1]
        }
        r = session.post(url, data=data_authorization)

    flag = True
    await bot.send_message(message.from_user.id, 'Бот авторизовался на сайте!', reply_markup=kb_authoriz)


@dp.message_handler(text=['Сменить логин'])
async def login(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите логин')
    await authorization.login.set()


@dp.message_handler(state=authorization.login)
async def login_authoriz(message: types.Message, state: FSMContext):

    async with state.proxy() as data_log:
        data_log['login'] = message.text

        await authorization.password.set()
        await bot.send_message(message.from_user.id, 'Введите пароль')


@dp.message_handler(state=authorization.password)
async def password_authoriz(message: types.Message, state: FSMContext):

    async with state.proxy() as data_log:
        data_log['password'] = message.text

    async with state.proxy() as data:
        cur_lp.execute('INSERT INTO authoriz VALUES (?, ?)', tuple(data.values()))
        base_lp.commit()

    for ret in cur_lp.execute('SELECT * FROM authoriz').fetchall():

        url = 'https://store-old.bezlimit.ru/app/login'
        session = requests.Session()
        session.headers.update(headers)
        r = session.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        csrf_token = soup.find('input', {'name': '_csrf-auth'})['value']
        data_authorization = {
            '_csrf-auth': csrf_token,
            'LoginForm[login]': ret[0],
            'LoginForm[password]': ret[1]
        }
        r = session.post(url, data=data_authorization)

    flag = True
    await bot.send_message(message.from_user.id, f'Бот под логином {ret[0]} авторизовался на сайте!', reply_markup=kb_client)
    await state.finish()



@dp.message_handler(text=['Фильтр'])
async def filter(message: types.Message, state=FSMContext):

    await bot.send_message(message.from_user.id, 'Введите номер телефона или комбинацию цифр\n'
                                                 'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=kb_mask)
    await FSMAdmin.name.set()
    return sql_start()


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    global flag, trf

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    flag = False
    trf = '0'
    cur.execute('DROP TABLE fil')
    base.close()
    curr.execute('DROP TABLE fill')
    basee.close()
    await message.reply('OK')
    await bot.send_message(message.from_user.id, '🛑Перезагрузите бота🛑')


@dp.message_handler(state=FSMAdmin.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

        if message.text == 'Дальше':
            data['name'] = data['name'].replace('Дальше', '')
            await FSMAdmin.next()
            await bot.send_message(message.from_user.id, 'Для ввода используйте A,B,C,N или цифры\n'
                                                         'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=kb_skip)

        if message.text.isdigit() == True:
            async with state.proxy() as data:
                data['symbol_mask'] = 'Пропустить'
                if data['symbol_mask'] == 'Пропустить':
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
            await FSMAdmin.category.set()
            await bot.send_message(message.from_user.id, 'Введите тариф\n'
                                                         'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=keyboard_category)


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
    await bot.send_message(message.from_user.id, 'Выберите категорию\n'
                        'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=keyboard_category)


@dp.message_handler(state=FSMAdmin.category)
async def category(message: types.Message, state:  FSMContext):
    global key
    async with state.proxy() as data:
        data['category'] = message.text
        key = 'PhonePromoSearch[categoryList][]'
        if message.text == 'Без категории':
            data['category'] = data['category'].replace('Без категории', '')
            key = 'PhonePromoSearch[categoryList]'

    await FSMAdmin.next()
    await bot.send_message(message.from_user.id, 'Введите тариф\n'
                                                 'Если хотите продолжить без этого условия, жмите на кнопку!', reply_markup=keyboard_tariff)

@dp.message_handler(state=FSMAdmin.tariff)
async def tariff(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['tariff'] = message.text
        if message.text == 'Без тарифа':
            data['tariff'] = data['tariff'].replace('Без тарифа', '')
        if message.text == '2000+':
            data['tariff'] = '2000, 2500, 3000, 4000'

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

    try:
        async with state.proxy() as data:
            cur.execute('INSERT INTO fil VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values()))
            base.commit()

        for ret in cur.execute('SELECT * FROM fil').fetchall():
            num = ret[0]
            sym_mask = ret[1]
            ctg = ret[2]
            trf = ret[3]
            msk = ret[4]
            rev = ret[5]

    except sqlite3.ProgrammingError:
        async with state.proxy() as data:
            curr.execute('INSERT INTO fill VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
            basee.commit()

        for ret in curr.execute('SELECT * FROM fill').fetchall():
            num = ret[0]
            ctg = ret[1]
            trf = ret[2]
            msk = ret[3]
            rev = ret[4]
        sym_mask = '          '

    list_num = []
    page = 1
    run = 1

    if rev == 'YES' and trf == '2000, 2500, 3000, 4000':

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
            'PhonePromoSearch[tariffList][0]': trf[0:4],
            'PhonePromoSearch[tariffList][1]': trf[6:10],
            'PhonePromoSearch[tariffList][2]': trf[12:16],
            'PhonePromoSearch[tariffList][3]': trf[18:23],
            key: ctg,
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.get(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')
        numbers_base = soup_filter.find_all('div', class_='phone-container')
        for i in numbers_base:
            num_base = i.find('h2').text
            list_num.append(num_base)

        await bot.send_message(message.from_user.id, f'Бот собрал {len(list_num)} номер(-ов)', reply_markup=kb_s)

    if rev == 'YES' and trf != '2000, 2500, 3000, 4000':

        await message.reply('Бот набирает базу номеров...')

        for _ in range(1, 20):

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
                key: ctg,
                'PhonePromoSearch[regionList]': '',
                'PhonePromoSearch[maskPattern]': msk
            }
            r_filter = session.post(url_work, data=data_filter, headers=headers)
            soup_filter = BeautifulSoup(r_filter.content, 'lxml')
            await asyncio.sleep(3)
            numbers_base = soup_filter.find_all('div', class_='phone-container')

            if len(soup_filter.find_all('div')) <= 82:
                page = 1
                break

            for i in numbers_base:
                num_base = i.find('h2').text
                if num_base not in list_num:
                    list_num.append(num_base)

            if len(list_num) < 500:
                page = ''
                break

            if len(list_num) < 2000:
                page += 1
                continue

            else:
                break

        await bot.send_message(message.from_user.id, f'Бот собрал {len(list_num)} номер(-ов)', reply_markup=kb_s)

    if rev == 'NO' and trf == '2000, 2500, 3000, 4000':
        run = 2
        url_work = "https://store-old.bezlimit.ru/promo"
        soup_filter = BeautifulSoup(r.content, 'lxml')
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
            'PhonePromoSearch[tariffList][0]': trf[0:4],
            'PhonePromoSearch[tariffList][1]': trf[6:10],
            'PhonePromoSearch[tariffList][2]': trf[12:16],
            'PhonePromoSearch[tariffList][3]': trf[18:23],
            key: ctg,
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.get(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')
        await bot.send_message(message.from_user.id, 'Публикация номеров...', reply_markup=kb_s)

    if rev == 'NO' and trf != '2000, 2500, 3000, 4000':
        run = 2
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
            key: ctg,
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.post(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')
        await bot.send_message(message.from_user.id, 'Публикация номеров...', reply_markup=kb_s)

    while trf == '2000, 2500, 3000, 4000':
        await asyncio.sleep(1)
        soup_filter = BeautifulSoup(r.content, 'lxml')
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
            'PhonePromoSearch[tariffList][0]': trf[0:4],
            'PhonePromoSearch[tariffList][1]': trf[6:10],
            'PhonePromoSearch[tariffList][2]': trf[12:16],
            'PhonePromoSearch[tariffList][3]': trf[18:23],
            key: ctg,
            'PhonePromoSearch[regionList]': '',
            'PhonePromoSearch[maskPattern]': msk
        }
        r_filter = session.get(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')

        if len(soup_filter.find_all('div')) <= 82:
            continue

        if len(soup_filter.find_all('div')) <= 3583:

            number_trf = soup_filter.find_all('div', class_='phone-container')
            for q in number_trf:
                new_trf = q.find('h2').text
                if new_trf not in list_num:
                    if rev == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_trf})
                        await message.reply(f'Бот забронировал номер - {new_trf}')
                        list_num.append(new_trf)
                        continue
                    await bot.send_message(message.from_user.id, new_trf, reply_markup=kb_s)
                    await asyncio.sleep(run)
                    list_num.append(new_trf)
                else:
                    continue


    while flag != False:
        await asyncio.sleep(1)
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
        key: ctg,
        'PhonePromoSearch[regionList]': '',
        'PhonePromoSearch[maskPattern]': msk
    }
        r_filter = session.post(url_work, data=data_filter, headers=headers)
        soup_filter = BeautifulSoup(r_filter.content, 'lxml')

        if len(list_num) > 500:
            page += 1

        if len(soup_filter.find_all('div')) <= 82:
            page = 1
            continue

        if len(soup_filter.find_all('div')) <= 3585:
            number_phone = soup_filter.find_all('div', class_='phone-container')
            for j in number_phone:
                new_phone = j.find('h2').text
                if new_phone not in list_num:
                    if rev == 'YES':
                        session.post("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                        await asyncio.sleep(1)
                        await message.reply(f'Бот забронировал номер - {new_phone}')
                        list_num.append(new_phone)
                        continue
                    await bot.send_message(message.from_user.id, new_phone, reply_markup=kb_s)
                    list_num.append(new_phone)
                    await asyncio.sleep(run)
                else:
                    continue

        elif flag == False:
            break



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)