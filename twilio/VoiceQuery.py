class VoiceQuery(object):
        _skillID = "amzn1.ask.skill.3e0cb603-64a5-4b40-99ef-d849f537b22b"
    def __init__(self, query, loc, skill):
        self.query = query
        self.loc = loc
        self.skill = skill

    def isSkill(self):
        return VoiceQuery._skillID == self.skill
