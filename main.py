import asyncio
from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
import requests
from bs4 import BeautifulSoup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

token = '6419289887:AAEboLioUQo0dPk12Xc-4SPBdO1R1J_cN78'
dis = Dispatcher()

@dis.message(CommandStart())
async def start(message):
    await message.answer('hey man, send me your request for wikipedia')

@dis.message()
async def request(message):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    link = f'https://en.wikipedia.org/w/index.php?search={message.text}&title=Special:Search&profile=advanced&fulltext=1&ns0=1'
    res = requests.get(link, headers=headers)
    bs = BeautifulSoup(res.text, 'lxml')

    search = list(bs.find('div', class_='mw-page-container').find('ul', class_='mw-search-results'))
    search_results = [{'link': x.a.get('href'), 'title': x.a.get('title')} for x in search]

    #buttoms = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=title, url=f'https://en.wikipedia.org/{link}')] for title, link in item.items()]for item in search_results)

    lst_buttoms = [[InlineKeyboardButton(text=item['title'], url=f'https://en.wikipedia.org{item["link"]}') for item in search_results]]
    buttoms2 = InlineKeyboardMarkup(inline_keyboard=lst_buttoms, row_width=2)

    #buttoms2.add(*lst_buttoms)

    await message.answer(text='Results of search:', reply_markup=buttoms2)



async def main():
    tb = Bot(token=token)
    await dis.start_polling(tb)

if __name__ == '__main__':
    asyncio.run(main())

