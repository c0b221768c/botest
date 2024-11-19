from discord import ButtonStyle, Interaction
from discord.ui import Button

from components.embed import EmbedFactory


class BaseButton(Button):
    def __init__(self, label: str, style: ButtonStyle, cache_manager, recruitment_id):
        super().__init__(label=label, style=style)
        self.recruitment_id = recruitment_id
        self.cache_manager = cache_manager

    async def update_message(self, interaction: Interaction):
        cache_data = self.cache_manager.get_recruitment_data(self.recruitment_id)
        if cache_data is None:
            await interaction.response.send_message("ERROR: Recruitment not found.")
            return

        embed = EmbedFactory(cache_data).build()
        await interaction.response.edit_message(embed=embed, view=self.view)


class JoinButton(BaseButton):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__("参加", ButtonStyle.green, cache_manager, recruitment_id)

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        self.cache_manager.update_participant(self.recruitment_id, user_id, True)
        await self.update_message(interaction)


class LeaveButton(BaseButton):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__("不参加", ButtonStyle.red, cache_manager, recruitment_id)

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        self.cache_manager.update_participant(self.recruitment_id, user_id, False)
        await self.update_message(interaction)


class CancelButton(BaseButton):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__("キャンセル", ButtonStyle.gray, cache_manager, recruitment_id)

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        self.cache_manager.cancel_participation(self.recruitment_id, user_id)
        await self.update_message(interaction)
