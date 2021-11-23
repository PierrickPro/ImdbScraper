from scraper import Scraper

got_url = 'https://www.imdb.com/title/tt0944947/?ref_=nv_sr_srsg_0'
black_mirror = 'https://www.imdb.com/title/tt2085059/?ref_=fn_al_tt_1'

data_path = 'data/episodes.csv'
review_path = 'data/review.csv'

scrapper = Scraper(black_mirror)

# scrap episodes
scrapper.scrap_all_episodes()
scrapper.save_episodes_as_csv(data_path)

scrapper.scrap_all_reviews()
scrapper.save_reviews_as_csv(review_path)