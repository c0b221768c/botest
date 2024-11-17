import discord
from cache.cache_manager import CacheManager
from components.embed import CreateEmbed
from components.views import CreateView
from config.settings import settings
from discord.ext import commands
from utils import helpers
from utils.validator import DateValidator, HeadcountValidator, ParticipantsValidator

# Intents 設定
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Bot 設定
bot = commands.Bot(command_prefix="/", intents=intents)


# Bot 起動時のイベント
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready. Logged in as {bot.user}")


# /joinus コマンド
@bot.tree.command(
    name="joinus",
    description="Valorantのメンバー募集を行います。引数は任意で指定できます。",
)
@discord.app_commands.describe(
    headcount="募集人数を指定できます (2, 3, 5, 10)",
    participants="参加者をメンションで指定できます（半角スペース区切り）",
    date="日付を指定できます（HH:MM, MM/DD HH:MM, YYYY/MM/DD HH:MM, または NN 分後）",
)
async def joinus(
    interaction: discord.Interaction,
    headcount: int = None,
    participants: str = None,
    date: str = None,
):
    try:
        # 引数のバリデーション
        headcount = HeadcountValidator(headcount).validate()
        headcount = str(headcount)
        participants = await ParticipantsValidator(participants, interaction).validate()
        date = DateValidator(date).validate()

        # create & update cache
        recruitment_id = helpers.generate_uuid()
        cache_manager = CacheManager()
        cache_manager.create_recruitment(recruitment_id, headcount, participants)

        # create embed & view
        embed = CreateEmbed(
            cache_manager.get_recruitment_data(recruitment_id)
        ).create_embed()
        view = CreateView(cache_manager, recruitment_id)

        await interaction.response.send_message(embed=embed, view=view)
    except ValueError as e:
        await interaction.response.send_message(str(e), ephemeral=True)


bot.run(settings.DISCORD_TOKEN)
