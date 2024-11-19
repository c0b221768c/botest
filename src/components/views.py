from discord.ui import View

from components.buttons import CancelButton, JoinButton, LeaveButton


class RecruitmentView(View):
    def __init__(self, cache_manager, recruitment_id):
        super().__init__()
        self.add_item(JoinButton(cache_manager, recruitment_id))
        self.add_item(LeaveButton(cache_manager, recruitment_id))
        self.add_item(CancelButton(cache_manager, recruitment_id))
