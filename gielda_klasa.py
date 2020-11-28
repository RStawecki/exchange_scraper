from bs4 import BeautifulSoup
import requests
import csv
import os


class Company:
    def __init__(self, nameCompany):
        self.url = 'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument='+nameCompany.upper()+'&date=&show_x=Poka%C5%BC+wyniki'
        self.path = os.path.join(r'D:\WebScraping\gielda',nameCompany.lower()+'.csv')
        try:
            self.connect_to_site()
        except:
            print("Problem connecting with site.")
        else:
            self.get_data_from_website()
            try:
                self.transformation_data()
            except ValueError:
                print("Company has no stock market since 2015.")
                exit()
            else:
                self.save_to_file()      

    def connect_to_site(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def get_data_from_website(self):
        data = self.soup.find('tbody')
        self.data = data.find_all('tr')
    
    @staticmethod
    def clean_data(data):
        cleanList = []
        for el in data:
            cleanList.append(el.text)
        return cleanList

    def transformation_data(self):
        listOfData = []
        for el in self.data:
            listOfData.append(list(el))

        dateData = [noRow[1] for noRow in listOfData]
        rateOpenDate= [noRow[5] for noRow in listOfData]
        rateMaxDate = [noRow[7] for noRow in listOfData]
        rateMinDate = [noRow[9] for noRow in listOfData]

        dates = Company.clean_data(dateData)
        openRates = Company.clean_data(rateOpenDate)
        maxRates = Company.clean_data(rateMaxDate)
        minRates = Company.clean_data(rateMinDate)

        indexDate = dates.index('02-01-2015')
        self.finalList = list(zip(dates[indexDate:], openRates[indexDate:], maxRates[indexDate:], minRates[indexDate:]))
        

    def save_to_file(self):
        try:
            with open(self.path, 'w', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Dates', 'Open rates', 'Max Rates', 'Min Rates'])
                writer.writerows(self.finalList)
        except FileNotFoundError:
            print("File does not exist.")

