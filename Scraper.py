from selenium import webdriver
import time
import datetime
import csv


class Scraper:
    def __init__(self, headless=True):
        print('Initialisation...')
        start = time.time()
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(chrome_options=options)
        print('Scraper initialized in ' + str(round(time.time() - start, 1)) + ' seconds')

    def destroy(self):
        self.driver.quit()

    def get_items_for_sale(self):
        self.driver.get('http://annonces.aozora.me/en?view=grid')

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        all_articles = self.driver.find_element_by_xpath('//*[@id="homepage-filters"]/article/div/div[2]/div[2]/div[1]/div')
        for_sale = all_articles.find_elements_by_class_name('listing-transaction-vente')
        output = []
        for item in for_sale:
            print(str(for_sale.index(item)) + '/' + str(len(for_sale)-1))
            caracs = []
            infos = item.find_elements_by_class_name('listing-specific-info')
            for info in infos:
                caracs.append(info.text)
            price = item.find_element_by_class_name('fluid-thumbnail-grid-image-price-container')
            caracs.append(float(price.text[1:].replace(',', '')))
            seller = item.find_element_by_class_name('home-fluid-thumbnail-grid-author-name')
            caracs.append(seller.text)
            link = item.find_element_by_class_name('fluid-thumbnail-grid-image-item-link')
            caracs.append(link.get_attribute("href"))
            caracs.append(datetime.datetime.now())
            output.append(caracs)
            print(caracs)
        return output

    def save_csv(self, data):
        print('Generating .CSV file...')
        with open('Ventes.csv', 'a') as f:
            wr = csv.writer(f, lineterminator='\n', delimiter=';')
            wr.writerows(data)
        print('Done')


if __name__ == '__main__':
    while 1:
        try:
            s = Scraper()
            data = s.get_items_for_sale()
            s.save_csv(data)
            s.destroy()
            time.sleep(3600*3)
        except Exception as e:
            print(e)
            print("Error, trying again")
