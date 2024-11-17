from discord.ui import View

from components.buttons import CancelButton, JoinButton, LeaveButton


class CreateView(View):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__()
        self.cache_manager = cache_manager
        self.recruitment_id = recruitment_id
        self.add_item(JoinButton(self.cache_manager, self.recruitment_id))
        self.add_item(LeaveButton(self.cache_manager, self.recruitment_id))
        self.add_item(CancelButton(self.cache_manager, self.recruitment_id))
