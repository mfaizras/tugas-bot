import newsScraper, vclassScrape, ifLabScrape

class runScrapper:
    @staticmethod
    def scrape_assignment():
        vclass = vclassScrape.ScraperTugas()
        vclass.runScrape()

        iflab = ifLabScrape.ScraperTugas()
        iflab.runScrape()

    @staticmethod
    def scrape_news():
        news = newsScraper.ScraperNews()
        news.runScrape()