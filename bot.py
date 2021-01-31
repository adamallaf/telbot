import os
import pytz
import sys
import logger

from datetime import datetime, date
from logging import getLogger
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import JobQueue
from threading import Thread

from cmds import CMDS
from ip_camera import IpCameraConfig
from msgs import any_msg_handler
from security import getUserByID
from security import owner_only
from utils import readToken
from utils import getToken


class BotAppConfig:
    token: str = None
    timezone: str = None
    alarm: bool = False
    camera_config: IpCameraConfig = None


class BotApp:
    def __init__(self, config: BotAppConfig):
        self.__config = config
        self.__logger = getLogger(self.__class__.__name__)
        self.__updater = Updater(self.__config.token)
        self.__dispatcher = self.__updater.dispatcher

        self.__dispatcher.add_handler(CommandHandler('restart', self.restart))
        self.__dispatcher.add_handler(CommandHandler('shutdown', self.shutdown))

        for cmd, handler in CMDS.items():
            self.__dispatcher.add_handler(CommandHandler(cmd, handler, pass_args=True))

        self.__dispatcher.add_handler(MessageHandler(Filters.all, any_msg_handler, pass_user_data=True))

        timezone = pytz.timezone(config.timezone)
        job_time = timezone.localize(
            datetime.combine(
                date.today(),
                datetime.strptime("0:00:00", "%H:%M:%S").time()
            )
        )

        self.__updater.job_queue.run_daily(
            self.daily_update_job,
            time=job_time
        )
        self.__logger.info(f"{self.__updater.bot.first_name} is ready!")

    def start(self):
        self.__logger.info(f"Starting {self.__updater.bot.first_name}...")
        self.__updater.start_polling()

    def stop(self):
        self.__updater.stop()
        self.__logger.info(f"{self.__updater.bot.first_name} is stopped.")

    def stop_and_restart(self):
        self.__logger.info(f"{self.__updater.bot.first_name} is restarting...")
        self.__updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    @owner_only
    def restart(self, bot, update):
        user_id = update.message.from_user.id
        user = getUserByID(user_id)
        self.__logger.info(f"{user}: restart!")
        update.message.reply_text('Restarting...')
        Thread(target=self.stop_and_restart).start()

    @owner_only
    def shutdown(self, bot, update):
        user_id = update.message.from_user.id
        user = getUserByID(user_id)
        self.__logger.info(f"{user}: shutdown !!!")
        update.message.reply_text('Shutting down...')
        Thread(target=self.stop).start()

    def daily_update_job(self, context, job):
        pass
