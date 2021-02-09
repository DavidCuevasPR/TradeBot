import aiohttp.web
import discord
from discord.ext import commands
from disputils import BotEmbedPaginator, BotMultipleChoice

from libs import alpha_vantage, database, utils


class Forex(commands.Cog):
    """Commands to monitor Forex related information"""

    def __init__(self, bot):
        self.bot = bot
        self.alpha_v = alpha_vantage.AlphaVantage()
        self.db = database.TradeBotDatabase()

    @commands.cooldown(1, 12)
    @commands.command(aliases=["exrate"])
    async def exchangerate(self, ctx: commands.Context, from_currency: str, to_currency: str):
        embed = discord.Embed(title=f"Currency Exchange Rate for: {from_currency} to {to_currency}")
        try:
            api_dict = await self.alpha_v.get_exchange_rate(from_currency, to_currency)
            for key in api_dict.keys():
                embed.add_field(name=key, value=api_dict[key])
            embed.set_footer(text="Do $help to see modules | Do $currencies to see a list of currencies")
        except aiohttp.web.HTTPNotFound:
            await ctx.send(embed=discord.Embed(title="The currencies entered are not available, "
                                                     "please do $currencies to see all currencies."))
        await ctx.send(embed=embed)

    # TODO:Multiple Choice for Phys or Digi & Paginator
    @commands.command()
    async def currencies(self, ctx: commands.Context):
        await (BotEmbedPaginator(ctx, utils.pages(utils.numbered(
            [f"{tup.code} | {tup.name}"
             for tup in self.db.phys_currency_list]
        ), n=15, title="List of physical currencies"))).run()


def setup(bot):
    bot.add_cog(Forex(bot))
