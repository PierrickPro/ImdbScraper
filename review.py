class Review:
    score = 0
    comment = ''
    review_title = ''
    is_positive = bool
    episode_number = ''
    season_number = ''

    def __init__(self, episode_number, season_number, review_title, score, comment):
        self.episode_number = episode_number
        self.season_number = season_number
        self.review_title = review_title
        self.comment = comment
        self.score = float(score)
        self.is_positive = self.score >= 8.0

    def __str__(self):
        return str(self.review_title) + "," + str(self.comment) + "," + str(self.score)
