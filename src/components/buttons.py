from discord import ButtonStyle, Interaction
from discord.ui import Button

from components.embed import CreateEmbed


class JoinButton(Button):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__(label="参加", style=ButtonStyle.green)
        self.recruitment_id = recruitment_id
        self.cache_manager = cache_manager

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        update_cache = self.cache_manager.get_recruitment_data(self.recruitment_id)

        if update_cache is None:
            await interaction.response.send_message("ERROR: Recruitment is not found.")

        self.cache_manager.update_participant(
            self.recruitment_id, user_id, is_participating=True
        )
        embed = CreateEmbed(update_cache).create_embed()
        await interaction.response.edit_message(embed=embed, view=self.view)


class LeaveButton(Button):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__(label="不参加", style=ButtonStyle.red)
        self.recruitment_id = recruitment_id
        self.cache_manager = cache_manager

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        update_cache = self.cache_manager.get_recruitment_data(self.recruitment_id)

        if update_cache is None:
            await interaction.response.send_message("ERROR: Recruitment is not found.")

        self.cache_manager.update_participant(
            self.recruitment_id, user_id, is_participating=False
        )
        embed = CreateEmbed(update_cache).create_embed()
        await interaction.response.edit_message(embed=embed, view=self.view)


class CancelButton(Button):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__(label="キャンセル", style=ButtonStyle.gray)
        self.recruitment_id = recruitment_id
        self.cache_manager = cache_manager

    async def callback(self, interaction: Interaction):
        user_id = interaction.user.id
        update_cache = self.cache_manager.get_recruitment_data(self.recruitment_id)

        if update_cache is None:
            await interaction.response.send_message("ERROR: Recruitment is not found.")

        self.cache_manager.cancel_participation(self.recruitment_id, user_id)
        embed = CreateEmbed(update_cache).create_embed()
        await interaction.response.edit_message(embed=embed, view=self.view)
