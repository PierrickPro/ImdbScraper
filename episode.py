class Episode:
    episode_title = ''
    season_number = ''
    episode_number = ''
    review_link = ''
    year = ''

    def __init__(self, episode_number, episode_title, season_number, review_link, year):
        self.episode_title = episode_title
        self.season_number = season_number
        self.review_link = review_link
        self.year = year
        self.episode_number = episode_number

    def __str__(self):
        return str(self.episode_number) + ' ' + str(self.episode_title) + ' ' + str(self.year)
