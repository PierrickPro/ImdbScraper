from bs4 import BeautifulSoup
import requests
import re
import csv
from episode import Episode
from review import Review


class Scraper:
    episodes_page = ''
    episodes = []
    reviews = []

    # region episodes
    def __init__(self, url):
        # extract series_id from url
        series_id = re.search(r"/tt(.*)/", url).group(0)

        # generate episode_page url using series_id
        self.episodes_page = 'https://www.imdb.com/title' + series_id + 'episodes?season='

    def scrap_all_episodes(self):
        season_counter = 1
        episode_counter = 1

        print('Scraping episodes...')

        # loop every season, until there is no more next_season url
        while True:
            print('\tseason ' + str(season_counter), ':')

            html_page = requests.get(self.episodes_page + str(season_counter)).text  # get html page from url
            html_page_soup = BeautifulSoup(html_page, 'html.parser')  # create BeautifulSoup object

            # extract every episode being in a div with attribute itemprop="episodes"
            episodes_soup = html_page_soup.find_all('div', itemprop="episodes")

            for episode_soup in episodes_soup:  # extract details of every episode
                e = self.scrap_episode(episode_soup, episode_counter, season_counter)
                self.episodes.append(e)
                episode_counter += 1
                print('\t\t' + e.__str__())

            next_season = html_page_soup.find('a', id='load_next_episodes')  # get next season href by id
            if not next_season:
                break  # if there is no next season, all episodes have been scraped

            season_counter += 1

    @staticmethod
    def scrap_episode(episode_soup, episode_counter, season_counter):
        # inside strong tag, extract episode_id from href in tag a
        episode_id = episode_soup.strong.a.get('href').split('/')[2]

        # inside strong tag, extract episode_title from text in tag a
        episode_title = episode_soup.strong.a.text

        # inside div tag with attribute class_='airdate', extract episode_year from text
        episode_year = episode_soup.find('div', class_='airdate').text.strip().split()[-1]

        # build review link by inserting episode_id in url template
        episode_review_link = "https://www.imdb.com/title/" + episode_id + "/reviews"

        # save details in episode object
        e = Episode(episode_counter, episode_title, season_counter, episode_review_link, episode_year)

        return e

    def save_episodes_as_csv(self, path):
        open(path, 'w').close()  # erase content of path
        with open(path, 'w', ) as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Episode Nbr', 'Name', 'Season Nbr', 'Review Link', 'Year'])
            for episode in self.episodes:
                writer.writerow([episode.episode_number, episode.episode_title, episode.season_number,
                                 episode.review_link, episode.year])
        print(path, 'saved\n')

    def read_episodes_csv(self, path):
        self.episodes = []
        with open(path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            data.pop(0)  # remove header row

            for row in data:
                self.episodes.append(Episode(row[0], row[1], row[2], row[3], row[4]))

            print(path, 'read')
            return self.episodes
    # endregion

    # region reviews
    def scrap_all_reviews(self, episodes=None):
        if episodes is None:
            episodes = self.episodes

        print('scraping reviews ...')

        for episode in episodes:  # for each episode in the list
            reviews = self.scrap_episode_reviews(episode)  # scrap reviews of the episode
            self.reviews = self.reviews + reviews
            print('\t', episode.episode_title, ': reviews scraped')

            # if len(self.reviews) > 200:  # only scrap the first 200 reviews
            #    break

        return self.reviews

    @staticmethod
    def scrap_episode_reviews(episode):
        reviews = []
        html_page = requests.get(episode.review_link).text  # get html page from url
        html_soup = BeautifulSoup(html_page, 'html.parser')  # create BeautifulSoup object

        reviews_soup = html_soup.find_all('div', class_='review-container')  # get reviews

        for review_soup in reviews_soup:  # extract score and comment from each review

            # inside span tag with attribute class_=None, extract score from text
            score = review_soup.find('span', class_=None).text

            # inside div tag with attribute class_='text show-more__control', extract comment from text
            comment = review_soup.find('div', class_='text show-more__control').text

            # extract title from href in tag a with attribute class_='title'
            title = review_soup.find('a', class_='title').text
            title = '' if title is None else title.strip('\n')

            if score.isdigit():  # only save reviews that have a score
                review = Review(episode.episode_number, episode.season_number, title, score, comment)
                reviews.append(review)
        return reviews

    def save_reviews_as_csv(self, path):
        open(path, 'w').close()  # erase content of path
        with open(path, 'w', ) as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(['Season Nbr', 'Episode Nbr', 'Title', 'Score', 'Comment'])
            for review in self.reviews:
                writer.writerow(
                    [review.season_number, review.episode_number, review.review_title, review.score, review.comment])
        print(path, 'saved\n')

    def read_reviews_csv(self, path):
        self.reviews = []
        with open(path, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
            data.pop(0)  # remove header row

            for row in data:
                self.reviews.append(Review(row[0], row[1], row[2], row[3], row[4]))

            print(path, 'read')
            return self.reviews
    # endregion
