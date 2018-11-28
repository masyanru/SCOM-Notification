import pymssql
from datetime import datetime, timedelta
import configparser
from telegram.ext import Updater, CommandHandler
import time

config = configparser.ConfigParser()
config.read("config.ini")


# SCOM connection
scom_server = config["scom"]["server"]
scom_user = config["scom"]["user"]
scom_password = config["scom"]["password"]
chat_id = config["scom"]["chat_id"]
bot_token = config["scom"]["bot_token"]


def get_alerts():

    conn = pymssql.connect(scom_server, scom_user, scom_password, 'OperationsManager')
    cursor = conn.cursor(as_dict=True)
    cursor.execute("""
    
    
select distinct
MonitoringObjectDisplayName,
Category,
dateadd(hour, 3, TimeAdded) as 'Time',
AlertStringName
-- AlertParams
from AlertView
where Severity = 2
and dateadd(hour, 3, TimeAdded) > DATEADD(MINUTE, -1, GETDATE())
and ResolutionState <> 255
    
    
    """)
    row = cursor.fetchall()

    result = []

    if len(row) != 0:
        for item in row:
            # age = (item['TimeAdded'] + timedelta(hours=3))
            item = 'Host: {0} \nCategory: {1} \nTime: *{2}* \n{3}'.format(item['MonitoringObjectDisplayName'], item['Category'], item['Time'].strftime('%H:%M %d-%m-%Y'), item['AlertStringName'])
            result.append(item)
        # print(result)
        return result
    conn.close()


def callback_minute(bot, job):
    # print('\n'.join(str(p) for p in get_alerts()))
    if get_alerts() is not None:
        bot.send_message(chat_id=chat_id, text='\n'.join(str(p) for p in get_alerts()), parse_mode="markdown", disable_web_page_preview=True)
    else:
        pass


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello!')


def main():
    """Run bot."""
    updater = Updater(bot_token)
    updater.start_polling()
    j = updater.job_queue
    jb = j.run_repeating(callback_minute, interval=60, first=0)


if __name__ == '__main__':
    main()
