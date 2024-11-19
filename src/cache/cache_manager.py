class CacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def create_recruitment(
        self, recruitment_id: str, headcount: int, participants: set, date
    ):
        self.cache[recruitment_id] = {
            "headcount": headcount,
            "participants": participants,
            "non_participants": set(),
            "date": date,
        }

    def get_recruitment_data(self, recruitment_id: str):
        return self.cache.get(recruitment_id)

    def update_participant(
        self, recruitment_id: str, user_id: int, is_participating: bool
    ):
        if recruitment_id not in self.cache:
            return

        data = self.cache[recruitment_id]
        participants = data["participants"]
        non_participants = data["non_participants"]

        if is_participating:
            non_participants.discard(user_id)
            participants.add(user_id)
        else:
            participants.discard(user_id)
            non_participants.add(user_id)

    def cancel_participation(self, recruitment_id: str, user_id: int):
        if recruitment_id not in self.cache:
            return

        data = self.cache[recruitment_id]
        data["participants"].discard(user_id)
        data["non_participants"].discard(user_id)

    def delete_recruitment(self, recruitment_id: str):
        self.cache.pop(recruitment_id, None)
