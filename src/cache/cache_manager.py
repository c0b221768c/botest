class CacheManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def create_recruitment(self, recruitment_id, headcount, participants=None):
        self.cache[recruitment_id] = {
            "headcount": headcount,
            "participants": participants or [],
            "non_participants": [],
        }
        return self.cache[recruitment_id]

    def get_recruitment_data(self, recruitment_id):
        return self.cache.get(recruitment_id)

    def update_participant(self, recruitment_id, user_id, is_participating=True):
        if recruitment_id not in self.cache:
            return

        participants = self.cache[recruitment_id]["participants"]
        non_participants = self.cache[recruitment_id]["non_participants"]

        if is_participating:
            if user_id in non_participants:
                non_participants.remove(user_id)
            if user_id not in participants:
                participants.append(user_id)
        else:
            if user_id in participants:
                participants.remove(user_id)
            if user_id not in non_participants:
                non_participants.append(user_id)

    def cancel_participation(self, recruitment_id, user_id):
        if recruitment_id not in self.cache:
            return

        participants = self.cache[recruitment_id]["participants"]
        non_participants = self.cache[recruitment_id]["non_participants"]

        if user_id in participants:
            participants.remove(user_id)
        if user_id in non_participants:
            non_participants.remove(user_id)

    def delete_recruitment(self, recruitment_id):
        self.cache.pop(recruitment_id, None)
