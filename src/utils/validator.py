import re
from datetime import datetime, timedelta


def is_valid_time(hour: int, minute: int) -> bool:
    return 0 <= hour <= 23 and 0 <= minute <= 59


def is_valid_date(year: int, month: int, day: int) -> bool:
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False


class HeadcountValidator:
    def __init__(self, headcount):
        self.headcount = headcount if headcount is not None else 5

    def validate(self):
        if self.headcount not in (2, 3, 5, 10):
            raise ValueError("募集人数は 2, 3, 5, 10 のいずれかにしてください。")
        return self.headcount


class ParticipantsValidator:
    def __init__(self, participants, interaction):
        self.interaction = interaction
        self.guild = interaction.guild
        self.executor = interaction.user
        self.participants = participants.split() if participants else []

    async def validate(self):
        member_mentions = [f"{self.executor.id}"]

        for user in self.participants:
            match = re.match(r"^<@!?(\d{18})>$", user)
            if match:
                user_id = int(match.group(1))
                member = self.guild.get_member(user_id)
                if member and member.id != self.executor.id:
                    member_mentions.append(f"{member.id}")
                else:
                    raise ValueError(f"無効なメンバーです: {user}")
            else:
                raise ValueError(f"無効なメンション形式です: {user}")

        return member_mentions


class DateValidator:
    def __init__(self, date_str: str = None):
        self.date_str = date_str

    def validate(self) -> datetime:
        now = datetime.now()

        if not self.date_str:
            return now + timedelta(minutes=30)

        patterns = [
            (r"^(\d{1,2}):(\d{2})$", self.parse_time_only),
            (r"^(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{2})$", self.parse_date_time),
            (r"^(\d{4})/(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{2})$", self.parse_full_date),
            (r"^\d+$", self.parse_minutes_later),
        ]

        for pattern, parser in patterns:
            match = re.match(pattern, self.date_str)
            if match:
                return parser(match)

        raise ValueError(
            "入力形式が不正です。許可されている形式は 'HH:MM', 'MM/DD HH:MM', 'YYYY/MM/DD HH:MM', 'NN (分後)' です。"
        )

    def parse_time_only(self, match):
        now = datetime.now()
        hour, minute = int(match.group(1)), int(match.group(2))
        if is_valid_time(hour, minute):
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        raise ValueError("不正な時間指定です。")

    def parse_date_time(self, match):
        now = datetime.now()
        month, day, hour, minute = map(int, match.groups())
        if is_valid_date(now.year, month, day) and is_valid_time(hour, minute):
            return now.replace(
                month=month, day=day, hour=hour, minute=minute, second=0, microsecond=0
            )
        raise ValueError("不正な日付または時間指定です。")

    def parse_full_date(self, match):
        year, month, day, hour, minute = map(int, match.groups())
        if is_valid_date(year, month, day) and is_valid_time(hour, minute):
            return datetime(year, month, day, hour, minute)
        raise ValueError("不正な日付または時間指定です。")

    def parse_minutes_later(self, match):
        minutes_later = int(match.group(0))
        if minutes_later > 0:
            return datetime.now() + timedelta(minutes=minutes_later)
        raise ValueError("分後の指定は正の整数でなければなりません。")
