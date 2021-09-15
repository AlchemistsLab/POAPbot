import discord
from discord.ext import commands
from tortoise.transactions import in_transaction

from constants import GUILD_INDEX
from app.models import PoapLink
from app.utils import ensure_registered
from app.constants import ALCHEMIST_ROLE


class POAPCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        guild = self.bot.guilds[GUILD_INDEX]
        if message.author == self.bot.user:
            # ignore bot's own messages
            return
        if not message.guild:
            # message is DM
            try:
                # check that user has Alchemists role in Covalent server
                member = guild.get_member(message.author.id)
                if not member:
                    member = await guild.fetch_member(message.author.id)
                db_user = await ensure_registered(message.author.id)
                member_is_alchemist = discord.utils.get(member.roles, name=ALCHEMIST_ROLE)
                member_has_poap = await PoapLink.exists(owner=db_user)

                async with in_transaction():
                    if member_is_alchemist and member_has_poap:
                        # member asks for POAP 2nd time
                        await message.channel.send("Sorry, only one POAP is allowed per person")
                    elif member_is_alchemist and not member_has_poap:
                        # member doesn't have POAP, give him POAP
                        # prevent race conditions via select_for_update + in_transaction
                        poap_link = await PoapLink.filter(is_activated=False).first().select_for_update()
                        if not poap_link:
                            await message.channel.send("Sorry, no more POAP links available")
                            return
                        poap_link.is_activated = True
                        poap_link.owner = db_user
                        await poap_link.save(update_fields=["is_activated", "owner_id", "modified_at"])
                        await message.channel.send(f"Hello, here is your POAP link {poap_link}")
                    # member isn't alchemist
                    else:
                        await message.channel.send("Sorry, you need to be an Alchemist to be eligible for the POAP")

            except discord.errors.Forbidden:
                pass
        return None


def setup(bot):
    bot.add_cog(POAPCog(bot))
