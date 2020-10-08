from bs4 import BeautifulSoup
import requests
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import time

def scrape(days, month, counties, year):
	result = {year:{}}
	
	for i in range(len(month)):
		url = ("https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=01.{}.{}&datoTil={}.{}.{}&id_region=0&id_niva1=51&id_niva2=56&id_bransje1=0").format(month[i], year,days[i], month[i], year)														

		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')

		curent_county = None

		counter = 0
		for tr in soup.findAll('tr'):
			if tr.text.strip() in counties:
				curr_month = None
				if curent_county != None:
					curr_month = {i+1:counter}
					result[year][curent_county].update(curr_month)

				counter = 0
				curent_county = tr.text.strip()
				if curent_county not in result[year]:
					result[year][curent_county] = {}
			else:
				text = tr.text.strip()
				
				if "Konkursåpning" in text:
					counter += 1

	return result

def init_days_in_month_arr(year):
	days = []
	for i in range(1,13):
		days.append(calendar.monthrange(year, i)[1])

	return days

def plot_thelot(first, second, counties):
	for i in counties:
		plt.figure(counties.index(i))
		x = []
		y = []
		
		x2 = []
		y2 = []
		
		count = 0
		count2 = 0

		for number in range(1,13):
			try:
				count += first[2019][i][number]
				y.append(count)
				x.append(number)
				
				count2 += second[2020][i][number]
				y2.append(count2)
				x2.append(number)
			except:
				pass
		
		plt.plot(x,y)
		plt.plot(x2,y2)
		plt.savefig(i)


start = time.time()
county = ["Troms og Finnmark", "Nordland", "Trøndelag", "Møre og Romsdal", "Vestland", "Rogaland", "Agder", "Vestfold og Telemark", "Viken", "Oslo", "Utenlands"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

days_2019 = init_days_in_month_arr(2019)
days_2020 = init_days_in_month_arr(2020)

all_2019 = scrape(days_2019, months, county, 2019)
all_2020 = scrape(days_2020, months, county, 2020)

plot_thelot(all_2019, all_2020, county)

print(time.time()-start)