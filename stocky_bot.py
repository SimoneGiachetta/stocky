import logging
from typing import Dict
from stocky_news import general, tech, finance, creative
from tabulate import tabulate
from book_suggest import viz, book_iteng, podcast
import pandas as pd
from portfolio import daily
from statista import parse_and_extract
import telegram
from pytrends.request import TrendReq
from index_data import america_oceania,europe,asia_africa, gainers, most_active, loosers, earnings_today
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    PicklePersistence,
    CallbackContext,
    CallbackQueryHandler,
)

bot = telegram.Bot(token='YOUR-TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND, RETRIVEDATA, RESOURCES, PODCAST, BOOK = range(6)

# Callback data
DATA, NEWS, MARKETS, RESOURCES = range(4)

def start(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    name = user.first_name
    keyboard = [
        ['DATA', 'NEWS'],
        ['MARKETS','RESOURCES'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(f"Welcome to Stocky, {name}!\nHere what you can do:\n\n"
    "\n• <b>Data</b>: infographics and trending data \n"
    "\n• <b>News</b>: read news from the globe\n"
    "\n• <b>Markets</b>: check real-time markets data\n "
    "\n• <b>Resources</b>: our update suggestions on papers, books, podcast or video we liked most", reply_markup=markup, parse_mode="HTML")
    return FIRST

def back_home(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s back to home.", user.first_name)
    name = user.first_name
    keyboard = [
        ['DATA', 'NEWS'],
        ['MARKETS','RESOURCES'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)    
    update.message.reply_text(f"Here we go, {name}.\nWhat would you like to check now?\n\n"
    "\n• <b>Data</b>: infographics and trending data\n"
    "\n• <b>News</b>: read news from the globe\n"
    "\n• <b>Markets</b>: check real-time markets data\n "
    "\n• <b>Resources</b>: our update suggestions on papers, books, podcast or video we liked most", reply_markup=markup, parse_mode="HTML")
    return FIRST    

def data(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose data section.", user.first_name)
    keyboard = [
        ['INFOGRAPHICS', 'TRENDS US'],
        ['TRENDS ITALY','BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
    "\n• <b>Infographics</b>: visualize up-to-date infographics\n"
    "\n• <b>Trends US</b>: discover trending topic in United States\n"
    "\n• <b>Trend Italy</b>: discover trending topic in Italy\n "
    "\n• <b>Economics</b>: retrive updated economics and business data", reply_markup=markup, parse_mode="HTML")
    return RETRIVEDATA

def trends_us(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose trends us.", user.first_name)
    keyboard = [
        ['INFOGRAPHICS', 'TRENDS US'],
        ['TRENDS ITALY','BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    pytrends = TrendReq(hl='en-US', tz=360)
    dd = pytrends.trending_searches(pn='united_states')
    trends = tabulate(dd, tablefmt="psql")
    update.message.reply_text(
        f'US TRENDS: \n\n {trends}', parse_mode="HTML", reply_markup=markup
    )
    return RETRIVEDATA

def trends_it(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose trends italy.", user.first_name)
    keyboard = [
        ['INFOGRAPHICS', 'TRENDS US'],
        ['TRENDS ITALY','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    pytrends = TrendReq(hl='en-US', tz=360)
    dd = pytrends.trending_searches(pn='italy')
    trends = tabulate(dd, tablefmt="psql")
    update.message.reply_text(
        f'ITALY TRENDS: \n\n {trends}', parse_mode="HTML", reply_markup=markup
    )
    return RETRIVEDATA

def data_viz(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose infographics.", user.first_name)
    keyboard = [
        ['INFOGRAPHICS', 'TRENDS US'],
        ['TRENDS ITALY','BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    viz_1, viz_2, viz_3, viz_4 = parse_and_extract('https://www.statista.com/chartoftheday/')
    update.message.reply_text('Daily Infographics', parse_mode="HTML", reply_markup=markup)
    bot.send_photo(chat_id=update.message.chat_id, photo=f'{viz_1}')
    bot.send_photo(chat_id=update.message.chat_id, photo=f'{viz_2}')
    bot.send_photo(chat_id=update.message.chat_id, photo=f'{viz_3}')
    bot.send_photo(chat_id=update.message.chat_id, photo=f'{viz_4}')

    return RETRIVEDATA

def news(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose news section", user.first_name )
    keyboard = [
        ['GENERAL NEWS','MARKETS &\nBUSINESS'],
        [ 'TECH & SCIENCE','ENTERTAINMENT'],
        ['BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(f'<b>What would you like to read?</b>\n\n\n'
    '• <b>General News</b>: Worldwide latest news\n\n'
    '• <b>Markets & Business</b>: News and articles on markets, finance and business\n\n'
    '• <b>Tech & Science</b>: Updates from technology, science and startup universe\n\n'
    '• <b>Creative</b>: News and articles from entertainment and creative industry', parse_mode='HTML', reply_markup=markup)
    return SECOND

def general_news(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose general news", user.first_name)
    keyboard = [
        ['GENERAL NEWS','MARKETS &\nBUSINESS'],
        [ 'TECH & SCIENCE','ENTERTAINMENT'],
        ['BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    gen_news = general()
    title_1, url_1 = gen_news[0][0], gen_news[0][1]
    title_2, url_2 = gen_news[1][0], gen_news[1][1]
    title_3, url_3 = gen_news[2][0], gen_news[2][1]
    title_4, url_4 = gen_news[3][0], gen_news[3][1]
    title_5, url_5 = gen_news[4][0], gen_news[4][1]
    title_6, url_6 = gen_news[5][0], gen_news[5][1]
    title_7, url_7 = gen_news[6][0], gen_news[6][1]
    title_8, url_8 = gen_news[7][0], gen_news[7][1]
    title_9, url_9 = gen_news[8][0], gen_news[8][1]
    title_10, url_10 = gen_news[9][0], gen_news[9][1]
    update.message.reply_text(f'<b>Latest general news</b>\n\n'
    f'- {title_1} <a href="{url_1}">(link)</a>\n\n'
    f'- {title_2} <a href="{url_2}">(link)</a>\n\n'
    f'- {title_3}<a href="{url_3}">(link)</a> \n\n'
    f'- {title_4} <a href="{url_4}">(link)</a>\n\n'
    f'- {title_5} <a href="{url_5}">(link)</a>\n\n'
    f'- {title_6} <a href="{url_6}">(link)</a>\n\n'
    f'- {title_7} <a href="{url_7}">(link)</a>\n\n'
    f'- {title_8} <a href="{url_8}">(link)</a>\n\n'
    f'- {title_9} <a href="{url_9}">(link)</a>\n\n'
    f'- {title_10} <a href="{url_10}">(link)</a>\n\n',
    parse_mode="HTML", reply_markup=markup)
    
    return SECOND

def tech_news(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose tech news", user.first_name)
    keyboard = [
        ['GENERAL NEWS','MARKETS &\nBUSINESS'],
        [ 'TECH & SCIENCE','ENTERTAINMENT'],
        ['BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    gen_news = tech()
    title_1, url_1 = gen_news[0][0], gen_news[0][1]
    title_2, url_2 = gen_news[1][0], gen_news[1][1]
    title_3, url_3 = gen_news[2][0], gen_news[2][1]
    title_4, url_4 = gen_news[3][0], gen_news[3][1]
    title_5, url_5 = gen_news[4][0], gen_news[4][1]
    title_6, url_6 = gen_news[5][0], gen_news[5][1]
    title_7, url_7 = gen_news[6][0], gen_news[6][1]
    title_8, url_8 = gen_news[7][0], gen_news[7][1]
    title_9, url_9 = gen_news[8][0], gen_news[8][1]
    title_10, url_10 = gen_news[9][0], gen_news[9][1]
    update.message.reply_text(f'<b>Latest articles on Technology & Science</b>\n\n'
    f'- {title_1} <a href="{url_1}">(link)</a>\n\n'
    f'- {title_2} <a href="{url_2}">(link)</a>\n\n'
    f'- {title_3} <a href="{url_3}">(link)</a>\n\n'
    f'- {title_4} <a href="{url_4}">(link)</a>\n\n'
    f'- {title_5} <a href="{url_5}">(link)</a>\n\n'
    f'- {title_6} <a href="{url_6}">(link)</a>\n\n'
    f'- {title_7} <a href="{url_7}">(link)</a>\n\n'
    f'- {title_8} <a href="{url_8}">(link)</a>\n\n'
    f'- {title_9} <a href="{url_9}">(link)</a>\n\n'
    f'- {title_10} <a href="{url_10}">(link)</a>\n\n',
    parse_mode="HTML", reply_markup=markup)

    return SECOND


def finance_news(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose financial news", user.first_name)
    keyboard = [
        ['GENERAL NEWS','MARKETS &\nBUSINESS'],
        [ 'TECH & SCIENCE','ENTERTAINMENT'],
        ['BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    gen_news = finance()
    title_1, url_1 = gen_news[0][0], gen_news[0][1]
    title_2, url_2 = gen_news[1][0], gen_news[1][1]
    title_3, url_3 = gen_news[2][0], gen_news[2][1]
    title_4, url_4 = gen_news[3][0], gen_news[3][1]
    title_5, url_5 = gen_news[4][0], gen_news[4][1]
    title_6, url_6 = gen_news[5][0], gen_news[5][1]
    title_7, url_7 = gen_news[6][0], gen_news[6][1]
    title_8, url_8 = gen_news[7][0], gen_news[7][1]
    title_9, url_9 = gen_news[8][0], gen_news[8][1]
    title_10, url_10 = gen_news[9][0], gen_news[9][1]
    update.message.reply_text(f'<b>Latest articles on Markets & Business</b>\n\n'
    f'- {title_1} <a href="{url_1}">(link)</a>\n\n'
    f'- {title_2} <a href="{url_2}">(link)</a>\n\n'
    f'- {title_3}<a href="{url_3}">(link)</a> \n\n'
    f'- {title_4} <a href="{url_4}">(link)</a>\n\n'
    f'- {title_5} <a href="{url_5}">(link)</a>\n\n'
    f'- {title_6} <a href="{url_6}">(link)</a>\n\n'
    f'- {title_7} <a href="{url_7}">(link)</a>\n\n'
    f'- {title_8} <a href="{url_8}">(link)</a>\n\n'
    f'- {title_9} <a href="{url_9}">(link)</a>\n\n'
    f'- {title_10} <a href="{url_10}">(link)</a>\n\n',
    parse_mode="HTML", reply_markup=markup)

    return SECOND

def creative_news(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose creative news", user.first_name)
    keyboard = [
        ['GENERAL NEWS','MARKETS &\nBUSINESS'],
        [ 'TECH & SCIENCE','ENTERTAINMENT'],
        ['BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    gen_news = creative()
    title_1, url_1 = gen_news[0][0], gen_news[0][1]
    title_2, url_2 = gen_news[1][0], gen_news[1][1]
    title_3, url_3 = gen_news[2][0], gen_news[2][1]
    title_4, url_4 = gen_news[3][0], gen_news[3][1]
    title_5, url_5 = gen_news[4][0], gen_news[4][1]
    title_6, url_6 = gen_news[5][0], gen_news[5][1]
    title_7, url_7 = gen_news[6][0], gen_news[6][1]
    title_8, url_8 = gen_news[7][0], gen_news[7][1]
    title_9, url_9 = gen_news[8][0], gen_news[8][1]
    title_10, url_10 = gen_news[9][0], gen_news[9][1]
    update.message.reply_text(f'<b>Latest news on Entertainment & Creative industry</b>\n\n'
    f'- {title_1} <a href="{url_1}">(link)</a>\n\n'
    f'- {title_2} <a href="{url_2}">(link)</a>\n\n'
    f'- {title_3}<a href="{url_3}">(link)</a> \n\n'
    f'- {title_4} <a href="{url_4}">(link)</a>\n\n'
    f'- {title_5} <a href="{url_5}">(link)</a>\n\n'
    f'- {title_6} <a href="{url_6}">(link)</a>\n\n'
    f'- {title_7} <a href="{url_7}">(link)</a>\n\n'
    f'- {title_8} <a href="{url_8}">(link)</a>\n\n'
    f'- {title_9} <a href="{url_9}">(link)</a>\n\n'
    f'- {title_10} <a href="{url_10}">(link)</a>\n\n',
    parse_mode="HTML", reply_markup=markup)

    return SECOND

def resources(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose resources section", user.first_name)
    keyboard = [
        ['PAPER', 'BOOK'],
        ['PODCAST','BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Updated list of sources and texts we find interesting", reply_markup=markup)
    return RESOURCES

def market(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s market section.", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('\n• <b>Earnings</b>: who publish the financial results today?\n\n• <b>Moves US</b>: check the daily gainers, loosers and the most active stocks\n\n• <b>America & Oceania</b>: daily performance of main index in America and Oceania\n \n• <b>Asia & Africa</b>: daily performance of main index in Asia and Africa\n\n• <b>Europe</b>: daily performance of main index in Europe',parse_mode='HTML', reply_markup=markup)
    return SECOND


def index_amoc(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose America&Oceania", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    indices = america_oceania()
    indices = tabulate(indices, tablefmt="psql" ,numalign="center",colalign=("left",))
    update.message.reply_text('<b>America & Oceania index |% Change|:</b>\n \n'+str(indices), parse_mode='HTML', reply_markup=markup)
    
    return SECOND

def index_europe(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose europe", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    indices = europe()
    indices = tabulate(indices, tablefmt="psql" ,numalign="center",colalign=("left",))
    update.message.reply_text('<b>European Index |% Change|:</b>\n \n'+str(indices), parse_mode='HTML', reply_markup=markup)

    return SECOND

def index_asaf(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose Asia&Africa", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    indices = asia_africa()
    indices = tabulate(indices, tablefmt="psql" ,numalign="center",colalign=("left",))
    update.message.reply_text('<b>Asia & Africa Index |% Change|:</b>\n'+str(indices), parse_mode='HTML', reply_markup=markup)

    return SECOND

def top_moves(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose top movers", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('<b>LOSERS |% Change|</b>\n'+str(loosers())+'\n\n<b>GAINERS |% Change|</b>\n'+str(gainers())+'\n\n<b>MOST ACTIVE |% Change|</b>:\n'+str(most_active()), parse_mode="HTML", reply_markup=markup)

    return SECOND

def earnings(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose today earnings", user.first_name)
    keyboard = [
        ['EARNINGS', 'MOVES'],
        ['AMERICA&OCEANIA', 'ASIA&AFRICA'],
        ['EUROPE','BACK']
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('<b>Today Earnings and Expected Result:</b>\n'+str(earnings_today()), parse_mode='HTML', reply_markup=markup)

    return SECOND


def paper_suggestion(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose papers.", user.first_name)
    keyboard = [
        ['PAPER', 'BOOK'],
        ['PODCAST','BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        'In our Drive folder <a href="link-folder">here</a> you can find lots of papers about Economics, Finance, Behavioural Science, Innovation&Technology and more.', parse_mode="HTML", reply_markup=markup
    )
    return RESOURCES

def podcast_lang(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose podcast section.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Choose the language you prefer', reply_markup=markup)

    return PODCAST


def podcast_ita(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose podcast italian.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    podcasts = podcast()
    podcasts = podcasts.loc[podcasts['Lang'] == 'IT',['Title','Topic','Url']]
    title_1, topic_1, url_1 = podcasts.iloc[0] 
    title_2, topic_2, url_2 = podcasts.iloc[1,]
    title_3, topic_3, url_3 = podcasts.iloc[2,]
    title_4, topic_4, url_4 = podcasts.iloc[3,]
    update.message.reply_text(f'<b>I nostri consigli</b>'u'\U0001F1EE\U0001F1F9'
    f'\n\n<b>Titolo</b>: {title_1}\n<b>Argomento</b>: {topic_1}\n<b>Spotify</b>: ' f'<a href="{url_1}">QUI</a>'
    f'\n\n<b>Titolo</b>: {title_2}\n<b>Argomento</b>: {topic_2}\n<b>Spotify</b>: ' f'<a href="{url_2}">QUI</a>'
    f'\n\n<b>Titolo</b>: {title_3}\n<b>Argomento</b>: {topic_3}\n<b>Spotify</b>: ' f'<a href="{url_3}">QUI</a>'
    f'\n\n<b>Titolo</b>: {title_4}\n<b>Argomento</b>: {topic_4}\n<b>Spotify</b>: ' f'<a href="{url_4}">QUI</a>',
    parse_mode="HTML", reply_markup=markup)

    return PODCAST

def podcast_eng(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose podcast english.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    podcasts = podcast()
    podcasts = podcasts.loc[podcasts['Lang'] == 'EN',['Title','Topic','Url']]
    title_1, topic_1, url_1 = podcasts.iloc[0] 
    title_2, topic_2, url_2 = podcasts.iloc[1,]
    title_3, topic_3, url_3 = podcasts.iloc[2,]
    title_4, topic_4, url_4 = podcasts.iloc[3,]
    update.message.reply_text(f'<b>Our suggestions</b>'u'\U0001F1EC\U0001F1E7'
    f'\n\n<b>Title</b>: {title_1}\n<b>Topic</b>: {topic_1}\n<b>Spotify</b>: ' f'<a href="{url_1}">HERE</a>'
    f'\n\n<b>Title</b>: {title_2}\n<b>Topic</b>: {topic_2}\n<b>Spotify</b>: ' f'<a href="{url_2}">HERE</a>'
    f'\n\n<b>Title</b>: {title_3}\n<b>Topic</b>: {topic_3}\n<b>Spotify</b>: ' f'<a href="{url_3}">HERE</a>'
    f'\n\n<b>Title</b>: {title_4}\n<b>Topic</b>: {topic_4}\n<b>Spotify</b>: ' f'<a href="{url_4}">HERE</a>',
    parse_mode="HTML", reply_markup=markup)

    return PODCAST

def book_lang(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s closed the conversation book section.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text('Choose the language you prefer', reply_markup=markup)

    return BOOK

def book_ita(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose book italian.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    books = book_iteng()
    books = books.loc[books['Lang'] == 'IT',['Title','Topic','Url']]
    title_1, topic_1, url_1 = books.iloc[0] 
    title_2, topic_2, url_2 = books.iloc[1,]
    title_3, topic_3, url_3 = books.iloc[2,]
    title_4, topic_4, url_4 = books.iloc[3,]
    update.message.reply_text(f'<b>I nostri consigli del mese</b>'u'\U0001F1EE\U0001F1F9''\n\n'
    f'<b>Titolo</b>: {title_1}\n<b>Argomento</b>: {topic_1}\n<b>Acquista</b>:'  f' <a href="{url_1}">QUI</a>  '
    f'\n\n<b>Titolo</b>: {title_2}\n<b>Argomento</b>: {topic_2}\n<b>Acquista</b>:' f' <a href="{url_2}">QUI</a>  '
    f'\n\n<b>Titolo</b>: {title_3}\n<b>Argomento</b>: {topic_3}\n<b>Acquista</b>:' f' <a href="{url_3}">QUI</a>  '
    f'\n\n<b>Titolo</b>: {title_4}\n<b>Argomento</b>: {topic_4}\n<b>Acquista</b>:'f' <a href="{url_4}">QUI</a>  ',
    parse_mode="HTML", reply_markup=markup)

    return BOOK


def book_eng(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s choose book english.", user.first_name)
    keyboard = [
        ['ENG', 'ITA'],
        ['BACK'],
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    books = book_iteng()
    books = books.loc[books['Lang'] == 'EN',['Title','Topic','Url']]
    title_1, topic_1, url_1 = books.iloc[0] 
    title_2, topic_2, url_2 = books.iloc[1,]
    title_3, topic_3, url_3 = books.iloc[2,]
    title_4, topic_4, url_4 = books.iloc[3,]
    update.message.reply_text(f'<b>Our monthly suggestions</b>'u'\U0001F1EC\U0001F1E7''\n\n'
    f'<b>Title</b>: {title_1}\n<b>Topic</b>: {topic_1}\n<b>Buy</b>:'  f' <a href="{url_1}">HERE</a>'
    f'\n\n<b>Title</b>: {title_2}\n<b>Topic</b>: {topic_2}\n<b>Buy</b>:' f' <a href="{url_2}">HERE</a>'
    f'\n\n<b>Title</b>: {title_3}\n<b>Topic</b>: {topic_3}\n<b>Buy</b>:' f' <a href="{url_3}">HERE</a>'
    f'\n\n<b>Title</b>: {title_4}\n<b>Topic</b>: {topic_4}\n<b>Buy</b>:'f' <a href="{url_4}">HERE</a>',
    parse_mode="HTML", reply_markup=markup)

    return BOOK


def main() -> None:

    updater = Updater("TELEGRAM -TOKEN")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                MessageHandler(Filters.regex('^DATA$'), data),
                MessageHandler(Filters.regex('^NEWS$'), news),
                MessageHandler(Filters.regex('^MARKETS$'), market),
                MessageHandler(Filters.regex('^RESOURCES$'), resources),
            ],
            RETRIVEDATA: [
                MessageHandler(Filters.regex('^INFOGRAPHICS$'), data_viz),
                MessageHandler(Filters.regex('^TRENDS US$'), trends_us),
                MessageHandler(Filters.regex('^TRENDS ITALY$'), trends_it),
                MessageHandler(Filters.regex('^BACK$'), back_home),
                ],
            SECOND: [
                MessageHandler(Filters.regex('^GENERAL NEWS$'), general_news),
                MessageHandler(Filters.regex('^TECH & SCIENCE$'), tech_news),
                MessageHandler(Filters.regex('^MARKETS &\nBUSINESS$'), finance_news),
                MessageHandler(Filters.regex('^AMERICA&OCEANIA$'), index_amoc),
                MessageHandler(Filters.regex('^ASIA&AFRICA$'), index_asaf),
                MessageHandler(Filters.regex('^EUROPE$'), index_europe),
                MessageHandler(Filters.regex('^MOVES$'), top_moves),
                MessageHandler(Filters.regex('^BACK$'), back_home),
                MessageHandler(Filters.regex('^ENTERTAINMENT$'), creative_news),
                MessageHandler(Filters.regex('^EARNINGS$'), earnings),
                
            ],
            RESOURCES: [
                MessageHandler(Filters.regex('^BACK$'), back_home),
                MessageHandler(Filters.regex('^BOOK$'), book_lang),
                MessageHandler(Filters.regex('^PAPER$'), paper_suggestion),
                MessageHandler(Filters.regex('^PODCAST$'), podcast_lang),
                ],
            BOOK:[
                MessageHandler(Filters.regex('^ENG$'), book_eng),
                MessageHandler(Filters.regex('^ITA$'), book_ita),
                MessageHandler(Filters.regex('^BACK$'), resources),
            ],
            PODCAST:[
                MessageHandler(Filters.regex('^ENG$'), podcast_eng),
                MessageHandler(Filters.regex('^ITA$'), podcast_ita),
                MessageHandler(Filters.regex('^BACK$'), resources),
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()