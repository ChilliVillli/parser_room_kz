import requests
from fake_useragent import UserAgent
from aiogram.types import CallbackQuery
from bs4 import BeautifulSoup
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keybord import kb_client, keyboard_stop
# from selenium_web import all_numbers


bot = Bot(token='5601906129:AAH1k-asnKub2yCS36TUmjHMUlr9UtcarW4')
dp = Dispatcher(bot, storage=MemoryStorage())
ua = UserAgent()
# headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
headers = {'User-agent': ua.random}


async def on_startup(_):
    print('Бот вышел в онлайн')


class FSMAdmin(StatesGroup):
    name = State()
    form_1 = State()
    form_2 = State()
    form_3 = State()
    form_4 = State()
    form_5 = State()
    form_6 = State()
    form_7 = State()
    form_8 = State()
    form_9 = State()
    form_10 = State()
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
        'LoginForm[login]': '519891',
        'LoginForm[password]': '4qt'
    }
    r = session.post(url, data=data_authorization)

    await bot.send_message(message.from_user.id, 'Бот авторизовался на сайте!')


@dp.message_handler(text=['Фильтр'])
async def filter(message: types.Message, state=FSMContext):

    await bot.send_message(message.from_user.id, 'Введите номер телефона или комбинацию цифр\n'
                                                 'Если хотите продолжить без этого значения введите 👉 q 👈')
    await FSMAdmin.name.set()


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


@dp.message_handler(state=FSMAdmin.name)
async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        for symbol in message.text:
            for count in len(message.text):
                if symbol == 'q':
                    data['name'][count] = data['name'].replace('q', '')
                if symbol != 'q':
                    data['name'][count] = symbol



    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-1\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')

@dp.message_handler(state=FSMAdmin.form_1)
async def form_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_1'] = message.text
        if message.text == 'q':
            data['form_1'] = data['form_1'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-2\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_2)
async def form_2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_2'] = message.text
        if message.text == 'q':
            data['form_2'] = data['form_2'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-3\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_3)
async def form_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_3'] = message.text
        if message.text == 'q':
            data['form_3'] = data['form_3'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-4\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_4)
async def form_4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_4'] = message.text
        if message.text == 'q':
            data['form_4'] = data['form_4'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-5\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_5)
async def form_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_5'] = message.text
        if message.text == 'q':
            data['form_5'] = data['form_5'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-6\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_6)
async def form_6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_6'] = message.text
        if message.text == 'q':
            data['form_6'] = data['form_6'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-7\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_7)
async def form_7(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_7'] = message.text
        if message.text == 'q':
            data['form_7'] = data['form_7'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-8\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_8)
async def form_8(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_8'] = message.text
        if message.text == 'q':
            data['form_8'] = data['form_8'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-9\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_9)
async def form_9(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['form_9'] = message.text
        if message.text == 'q':
            data['form_9'] = data['form_9'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Для ввода используйте A,B,C,N или цифры-10\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')


@dp.message_handler(state=FSMAdmin.form_10)
async def form_10(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['form_10'] = message.text
        if message.text == 'q':
            data['form_10'] = data['form_10'].replace('q', '')
    await FSMAdmin.next()
    await message.reply('Введите тариф\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')

@dp.message_handler(state=FSMAdmin.tariff )
async def tariff(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['tariff'] = message.text
        if message.text == 'q':
            data['tariff'] = data['tariff'].replace('q', '')

    await FSMAdmin.next()
    await message.reply('Введите нужную маску, через запятую без пробела!\n'
                        'Например-AAABCBC,NAAABBB\n'
                        'Если хотите продолжить без этого значения введите 👉 q 👈')

@dp.message_handler(state=FSMAdmin.mask)
async def mask(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['mask'] = message.text
        if message.text == 'q':
            data['mask'] = data['mask'].replace('q', '')

    await FSMAdmin.next()
    await message.reply('Бронировать номера? Введите нужный вариант Yes/No')

@dp.message_handler(state=FSMAdmin.reserv)
async def reserv(message: types.Message, state: FSMContext):
    global r, session

    async with state.proxy() as data:
        data['reserv'] = message.text.upper()
        if message.text == 'YES':
            reserv_num = 'YES'
        else:
            reserv_num = 'NO'

    page = 1
    list_num = []
    url_work = "https://store-old.bezlimit.ru/promo"
    soup_filter = BeautifulSoup(r.content, 'lxml')
    csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
    data_filter = {
        '_csrf-auth': csrf_token_filter,
        'PhonePromoSearch[page]': str(page),
        'PhonePromoSearch[phoneCombs][1]': data['name'],
        'PhonePromoSearch[phoneCombs][2]': '',
        'PhonePromoSearch[phoneCombs][3]': '',
        'PhonePromoSearch[phonePattern][1]': data['form_1'].upper(),
        'PhonePromoSearch[phonePattern][2]': data['form_2'].upper(),
        'PhonePromoSearch[phonePattern][3]': data['form_3'].upper(),
        'PhonePromoSearch[phonePattern][4]': data['form_4'].upper(),
        'PhonePromoSearch[phonePattern][5]': data['form_5'].upper(),
        'PhonePromoSearch[phonePattern][6]': data['form_6'].upper(),
        'PhonePromoSearch[phonePattern][7]': data['form_7'].upper(),
        'PhonePromoSearch[phonePattern][8]': data['form_8'].upper(),
        'PhonePromoSearch[phonePattern][9]': data['form_9'].upper(),
        'PhonePromoSearch[phonePattern][10]': data['form_10'].upper(),
        'PhonePromoSearch[tariffList]': '',
        'PhonePromoSearch[tariffList][]': data['tariff'],
        'PhonePromoSearch[categoryList]': '',
        'PhonePromoSearch[regionList]': '',
        'PhonePromoSearch[maskPattern]': data['mask']
    }
    r_filter = session.post(url_work, data=data_filter)
    soup_filter = BeautifulSoup(r_filter.content, 'lxml')

    await state.update_data({"parsing_continue": True})
    while (await state.get_data()).get("parsing_continue"):

        if len(soup_filter.find_all('div')) < 500:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': '',
                'PhonePromoSearch[phoneCombs][1]': data['name'],
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': data['form_1'].upper(),
                'PhonePromoSearch[phonePattern][2]': data['form_2'].upper(),
                'PhonePromoSearch[phonePattern][3]': data['form_3'].upper(),
                'PhonePromoSearch[phonePattern][4]': data['form_4'].upper(),
                'PhonePromoSearch[phonePattern][5]': data['form_5'].upper(),
                'PhonePromoSearch[phonePattern][6]': data['form_6'].upper(),
                'PhonePromoSearch[phonePattern][7]': data['form_7'].upper(),
                'PhonePromoSearch[phonePattern][8]': data['form_8'].upper(),
                'PhonePromoSearch[phonePattern][9]': data['form_9'].upper(),
                'PhonePromoSearch[phonePattern][10]': data['form_10'].upper(),
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
                    await bot.send_message(message.from_user.id, new_phone, parse_mode="Markdown",
                                           reply_markup=keyboard_stop)
                    if reserv_num == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    sleep(1)
                    await bot.send_message(message.from_user.id, 'новых номеров нет, прервать цикл?', parse_mode="Markdown",
                                           reply_markup=keyboard_stop)
                    break
        if len(soup_filter.find_all('div')) > 500:
            csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
            data_filter = {
                '_csrf-auth': csrf_token_filter,
                'PhonePromoSearch[page]': '',
                'PhonePromoSearch[phoneCombs][1]': data['name'],
                'PhonePromoSearch[phoneCombs][2]': '',
                'PhonePromoSearch[phoneCombs][3]': '',
                'PhonePromoSearch[phonePattern][1]': data['form_1'].upper(),
                'PhonePromoSearch[phonePattern][2]': data['form_2'].upper(),
                'PhonePromoSearch[phonePattern][3]': data['form_3'].upper(),
                'PhonePromoSearch[phonePattern][4]': data['form_4'].upper(),
                'PhonePromoSearch[phonePattern][5]': data['form_5'].upper(),
                'PhonePromoSearch[phonePattern][6]': data['form_6'].upper(),
                'PhonePromoSearch[phonePattern][7]': data['form_7'].upper(),
                'PhonePromoSearch[phonePattern][8]': data['form_8'].upper(),
                'PhonePromoSearch[phonePattern][9]': data['form_9'].upper(),
                'PhonePromoSearch[phonePattern][10]': data['form_10'].upper(),
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
                    await bot.send_message(message.from_user.id, new_phone, parse_mode="Markdown", reply_markup=keyboard_stop)
                    if reserv_num == 'YES':
                        session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
                    list_num.append(new_phone)
                else:
                    sleep(1)
                    await bot.send_message(message.from_user.id, 'новых номеров нет, прервать цикл?',
                                           parse_mode="Markdown", reply_markup=keyboard_stop)
                    break
            page += 1
            if page >= 20:
                page = 1




@dp.callback_query_handler(Text(equals="stop"), state='*')
async def stop_callback(query: CallbackQuery, state: FSMContext):

    await state.update_data({"parsing_continue": False})
    await query.answer("Цикл остановлен")
    await state.finish()
    return await query.message.edit_text("Вы остановили цикл", reply_markup=None, disable_web_page_preview=True)


# @dp.message_handler(text=['go'])
# async def parsing_num(message: types.Message):
#     global r, session
#     list_num = []
#     page = 1

    # while page != 20:
    #     url_work = "https://store-old.bezlimit.ru/promo"
    #     soup_filter = BeautifulSoup(r.content, 'lxml')
    #     csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
    #     data_filter = {
    #         '_csrf-auth': csrf_token_filter,
    #         'PhonePromoSearch[page]': str(page),
    #         'PhonePromoSearch[phoneCombs][1]': '',
    #         'PhonePromoSearch[phoneCombs][2]': '',
    #         'PhonePromoSearch[phoneCombs][3]': '',
    #         'PhonePromoSearch[phonePattern][1]': '',
    #         'PhonePromoSearch[phonePattern][2]': '',
    #         'PhonePromoSearch[phonePattern][3]': '',
    #         'PhonePromoSearch[phonePattern][4]': '',
    #         'PhonePromoSearch[phonePattern][5]': '',
    #         'PhonePromoSearch[phonePattern][6]': '',
    #         'PhonePromoSearch[phonePattern][7]': '',
    #         'PhonePromoSearch[phonePattern][8]': '',
    #         'PhonePromoSearch[phonePattern][9]': '',
    #         'PhonePromoSearch[phonePattern][10]': '',
    #         'PhonePromoSearch[tariffList]': '',
    #         'PhonePromoSearch[tariffList][]': '',
    #         'PhonePromoSearch[categoryList]': '',
    #         'PhonePromoSearch[regionList]': '',
    #         'PhonePromoSearch[maskPattern]': ''
    #     }
    #     r_filter = session.post(url_work, data=data_filter)
    #     sleep(3)
    #     soup_filter = BeautifulSoup(r_filter.content, 'html.parser')
    #     number = soup_filter.find_all('div', class_='phone-container')
    #     for i in number:
    #         name = i.find('h2').text
    #         if name not in list_url:
    #             list_url.append(name)
    #         else:
    #             continue
    #     page += 1
    #
    #
    # while True:
    #
    #     url_work = "https://store-old.bezlimit.ru/promo"
    #     soup_filter = BeautifulSoup(r.content, 'lxml')
    #     csrf_token_filter = soup_filter.find('input', {'name': '_csrf-auth'})['value']
    #     data_filter = {
    #         '_csrf-auth': csrf_token_filter,
    #         'PhonePromoSearch[page]': str(page),
    #         'PhonePromoSearch[phoneCombs][1]': '',
    #         'PhonePromoSearch[phoneCombs][2]': '',
    #         'PhonePromoSearch[phoneCombs][3]': '',
    #         'PhonePromoSearch[phonePattern][1]': '',
    #         'PhonePromoSearch[phonePattern][2]': '',
    #         'PhonePromoSearch[phonePattern][3]': '',
    #         'PhonePromoSearch[phonePattern][4]': '',
    #         'PhonePromoSearch[phonePattern][5]': '',
    #         'PhonePromoSearch[phonePattern][6]': '',
    #         'PhonePromoSearch[phonePattern][7]': '',
    #         'PhonePromoSearch[phonePattern][8]': '',
    #         'PhonePromoSearch[phonePattern][9]': '',
    #         'PhonePromoSearch[phonePattern][10]': '',
    #         'PhonePromoSearch[tariffList]': '',
    #         'PhonePromoSearch[tariffList][]': '',
    #         'PhonePromoSearch[categoryList]': '',
    #         'PhonePromoSearch[regionList]': '',
    #         'PhonePromoSearch[maskPattern]': ''
    #     }
    #     r_filter = session.post(url_work, data=data_filter)
    #     soup_filter = BeautifulSoup(r_filter.content, 'lxml')
    #     number_phone = soup_filter.find_all('div', class_='phone-container')
    #     for j in number_phone:
    #         new_phone = j.find('h2').text
    #         if new_phone not in list_num:
    #             sleep(1)
    #             await bot.send_message(message.from_user.id, new_phone, parse_mode="Markdown")
    #             # session.get("https://store-old.bezlimit.ru/promo/reservation-turbo", data={'phone': new_phone})
    #             list_num.append(new_phone)
    #         else:
    #             continue
    #     page += 1
    #
    #     if page >= 50:
    #         page = 1



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)