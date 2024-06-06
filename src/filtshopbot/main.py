import argparse
import re

import discord


class Bot(discord.Client):
    def __init__(self, banwords: list[str]) -> None:
        self.banwords: list[str] = banwords
        self.filter = re.compile(
            r"(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?"
        )

        intents = discord.Intents.default()
        intents.message_content = True
        super(Bot, self).__init__(intents=intents)

    async def on_message(
        self,

        message: discord.Message
    ) -> None:
        for invite_link in self.filter.findall(message.content):
            invite = await self.fetch_invite(invite_link)
            if invite.guild is None:
                continue
            info: str = f"{invite.guild.name} {invite.guild.description}"
            print(f"{message.content}: {info}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="filtshopbot",
        description="bot for filtering messages with invites to shops"
    )
    parser.add_argument(
        "token",
        help="discord bot token"
    )

    args = parser.parse_args()
    bot = Bot([])
    bot.run(args.token)
