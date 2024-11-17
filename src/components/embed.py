from cache.cache_manager import CacheManager
from discord import Embed


class CreateEmbed:
    def __init__(self, cache):
        self.headcount = cache["headcount"]
        self.participants = cache["participants"]
        self.non_participants = cache["non_participants"]
        self.slot = max(0, int(self.headcount) - len(self.participants))

    def set_title(self):
        titles = {
            "2": "VALORANT デュオ募集",
            "3": "VALORANT トリオ募集",
            "5": "VALORANT フルパ募集",
            "10": "VALORANT カスタム募集",
        }
        return titles.get(self.headcount, "VALORANT 募集")

    def create_embed(self):
        embed = Embed(title=self.set_title(), color=0xFFC0CB)
        embed.add_field(
            name="参加者一覧",
            value="\n".join(f"<@{p}>" for p in self.participants) or "なし",
            inline=True,
        )
        embed.add_field(
            name="不参加者一覧",
            value="\n".join(f"<@{p}>" for p in self.non_participants) or "なし",
            inline=True,
        )
        embed.set_footer(text=f"残り参加枠: {self.slot}人")
        # デバック
        # キャッシュの中身を表示
        print("------")
        cache = CacheManager()
        for i in cache.cache:
            print(i, cache.cache[i])
        print("------")
        return embed
