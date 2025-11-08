from src.spire.sts_profile import Profile


class ProfilesResponse:
    def __init__(self, profiles: list[Profile]):
        self.profiles = profiles
