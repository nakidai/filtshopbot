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
            info: str = f"{invite.guild.name} {invite.guild.description}".lower()
            for banword in self.banwords:
                if banword in info:
                    print(f"{message.content}: {info}")
                    break


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="filtshopbot",
        description="bot for filtering messages with invites to shops"
    )
    parser.add_argument(
        "token",
        help="discord bot token"
    )
    parser.add_argument(
        "banwordspath",
        help="path to file with banwords"
    )

    args = parser.parse_args()

    with open(args.banwordspath, "r") as file:
        banwords = [line.strip() for line in file]
    bot = Bot(banwords)
    bot.run(args.token)
