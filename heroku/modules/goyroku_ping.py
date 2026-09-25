# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ Codrago, 2024-2030
# This file is a part of Heroku Userbot
# 🌐 https://github.com/coddrago/Heroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# ©️ GardenYab, 2026-2030
# This file is a part of Goyroku Userbot
# 🌐 https://github.com/gardenyab/Goyroku
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

import getpass
import inspect
import logging
import os
import platform as lib_platform
import random
import time
from io import BytesIO

from herokutl.tl.types import Message
from herokutl.types import InputMediaWebPage

from .. import loader, main, utils
from ..inline.types import InlineCall

logger = logging.getLogger(__name__)

@loader.tds
class Ping(loader.Module):
    """Ping module for Goyroku"""

    strings = {
        "name": "Ping",
        "configping": "Your custom text. You can use placeholders: {ping} - This is your ping, {uptime} - This is your uptime, {ping_hint} - hint. You can use the placeholder {hostname} if you need a hostname.",
        "configpingph": "🤖 Custom placeholders: {}",
        "hint": "Specify hints. To add them to the text, add the {hint} placeholder to custom_message",
        "ping_emoji": "An emoji that appears when the ping increases slightly..",
        "banner_url": "Here's a picture of your ping, for example: https://raw.githubusercontent.com/gardenyab/Goyroku/refs/heads/master/assets/goyroku_ping.png",
        "always_show_hint": "Whether to always show the Hint",
        "quote_media": "Whether to show photos as quotes,",
        "invert_media": "Change the photo position (top or bottom)",
        "suspend_invalid_time": "<tg-emoji emoji-id=5210952531676504517>🚫</tg-emoji> <b>Incorrect freezing time</b>",
        "suspended": "<tg-emoji emoji-id=5452023368054216810>🥶</tg-emoji> <b>Bot frozen for <code>{}</code> <b>seconds</b>"
    }

    strings_ru = {
        "name": "Ping",
        "configping": "Ваш кастомный текст. Вы можете использовать плейсхолдеры: {ping} - Это ваш пинг, {uptime} - Это ваш аптайм, {ping_hint} - подсказка. Вы можете использовать плейсхолдер {hostname} если вам нужен hostname вашего сервера",
        "configpingph": "🤖Кастомные плейсхолдеры: {}",
        "hint": "Укажите Подсказки. Для добавления их в текст, добавье в custom_message плейсхолдер {hint}",
        "ping_emoji": "Эмодзи которое появляется при не значительном росте пинга.",
        "banner_url": "Картинка для вашего пинга, для примера: https://raw.githubusercontent.com/gardenyab/Goyroku/refs/heads/master/assets/goyroku_ping.png",
        "always_show_hint": "Показывать ли Подсказку всегда",
        "quote_media": "Показывать ли фото как цитату",
        "invert_media": "Поменять местоположение фото (сверху или снизу)",
        "suspend_invalid_time": "<tg-emoji emoji-id=5210952531676504517>🚫</tg-emoji> <b>Неверное время заморозки</b>",
        "suspended": "<tg-emoji emoji-id=5452023368054216810>🥶</tg-emoji> <b>Бот заморожен на</b> <code>{}</code> <b>секунд</b>"
    }
    
    def __init__(self):
        self._memory = {}
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                """<blockquote><tg-emoji emoji-id=5190648194043755386>🚀</tg-emoji> <b>Ping {ping}ms</b>
————
<tg-emoji emoji-id=5204072642608381541>🧩</tg-emoji> <b>Uptime {uptime}</b></blockquote>""",
                lambda: (
                    self.strings["configping"]
                    + (
                        "\n"
                        + self.strings["configpingph"].format(
                            "\n" + utils.config_placeholders()
                        )
                        if utils.config_placeholders()
                        else ""
                    )
                ),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "hints",
                None,
                lambda: self.strings["hint"],
                validator=loader.validators.RandomString(),
            ),
            loader.ConfigValue(
                "always_show_hint",
                False,
                lambda: self.strings["always_show_hint"],
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ping_emoji",
                "🍓",
                lambda: self.strings["ping_emoji"],
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "banner_url",
                None,
                lambda: self.strings["banner_url"],
                validator=loader.validators.RandomLink(),
            ),
            loader.ConfigValue(
                "quote_media",
                False,
                lambda: self.strings["quote_media"], #"Switch preview media to quote in ping",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "invert_media",
                False,
                lambda: self.strings["invert_media"], #"Switch preview invert media in ping",
                validator=loader.validators.Boolean(),
            ),
        )
        
    @loader.command()
    async def suspend(self, message: Message):
        try:
            time_sleep = float(utils.get_args_raw(message))
            if time_sleep > 86400 * 365 * 100:
                await utils.answer(message, self.strings["suspend_invalid_time"])
            else:
                await utils.answer(
                    message,
                    self.strings["suspended"].format(time_sleep),
                )
                time.sleep(time_sleep)
        except ValueError:
            await utils.answer(message, self.strings["suspend_invalid_time"])

    @loader.command()
    async def ping(self, message: Message):
        """- Find out your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, self.config["ping_emoji"])
        banner = str(self.config["banner_url"])

        if self.config["banner_url"] and self.config["quote_media"] is True:
            banner = InputMediaWebPage(str(self.config["banner_url"]), optional=True)

        elif not self.config["banner_url"]:
            banner = None
        hint = ""
        if self.config["always_show_hint"] and self.config["hints"]: hint = str(self.config["hints"])
        elif self.config["hints"]: 
            if random.choice([0, 0, 1]) == 1:
                hint = str(self.config["hints"])
        data = {
            "ping": round((time.perf_counter_ns() - start) / 10**6, 3),
            "uptime": utils.formatted_uptime(),
            "hint": hint,
            "hostname": lib_platform.node(),
            "user": getpass.getuser(),
            "platform": utils.get_platform_name(),
        }
        data = await utils.get_placeholders(data, self.config["custom_message"])
        try:
            placeholders_msg = self.config["custom_message"].format(**data)
        except KeyError:
            logger.exception("Missing placeholder in custom_message")
            placeholders_msg = "<tg-emoji emoji-id=5210952531676504517>🚫</tg-emoji>"
        await utils.answer(
            message,
            placeholders_msg,
            file=banner,
            invert_media=self.config["invert_media"],
        )

    async def client_ready(self):
        self._content_channel_id = await utils.wait_for_content_channel(self._db)
        self.logchat = int(f"-100{self._content_channel_id}")
        logging.getLogger().handlers[0].install_tg_log(self)
        logger.debug("Bot logging installed for %s", self.logchat)