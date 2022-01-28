from threading import Thread

import schedule
import telebot

import config
from html_parser import Parser

bot = telebot.TeleBot(config.TOKEN)
parser = Parser(config.TT_URL)


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    user_id = message.from_user.id
    print(user_id)
    bot.send_message(user_id, 'Здарова хуй')


# allowed_users = [config.MY_ID, config.MATZ_ID]
allowed_users = [config.MY_ID]


def make_msg(stats):
    videos = ''
    vid_stats = stats['videos']
    vid_all_views = 0
    for i in vid_stats:
        videos += f'Видео: №{i} Просмотры: {vid_stats[i]}\n'
        vid_all_views += int(vid_stats[i])

    return f'''
Подписки: {stats['following']}
Подписчики: {stats['followers']}
Лайки: {stats['likes']}

Общее количество видео: {len(vid_stats)}
Общее количество просмотров: {vid_all_views}

{videos}
    '''


def job():
    parser.parse_tt_views()
    stats = make_msg(parser.stats)
    for i in allowed_users:
        bot.send_message(i, stats)


def scheduler():
    schedule.every(5).hours.do(job)
    while True:
        schedule.run_pending()

job()
Thread(target=scheduler, args=()).start()
bot.polling(none_stop=True)
