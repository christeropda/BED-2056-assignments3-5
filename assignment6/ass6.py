from bs4 import BeautifulSoup
import requests
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import time
import datetime

def scrape(days, month, counties, year, result):
	for i in range(len(month)):
		if (i+1) > datetime.date.today().month and year == 2020:
			break

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
				
				if "Konkursåpning" in text or "Konkursåpning i hjemlandet" in text:
					counter += 1
		
		if curent_county in counties:
			curr_month = {i+1:counter}
			result[year][curent_county].update(curr_month)

	return result

def init_days_in_month_arr(year):
	days = []
	for i in range(1,13):
		days.append(calendar.monthrange(year, i)[1])

	return days

def plot_thelot(first, counties):
	month = []
	konkurs = []
	
	count = 0
	for year in first:
		fylker = first[year]
		for fylke in fylker:
			month.clear()
			konkurs.clear()
			count = 0		
			plt.figure(counties.index(fylke))
			for key, value in fylker[fylke].items():
				count += value
				month.append(key)
				konkurs.append(count)

			plt.plot(month, konkurs)
			plt.title(fylke)
	
	
	plt.show()

county = ["Troms og Finnmark", "Nordland", "Trøndelag", "Møre og Romsdal", "Vestland", "Rogaland", "Agder", "Vestfold og Telemark", "Viken", "Oslo", "Utenlands"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
result = {2019:{}, 2020:{}}

days_2019 = init_days_in_month_arr(2019)
days_2020 = init_days_in_month_arr(2020)

all_2019 = scrape(days_2019, months, county, 2019, result)
all_2020 = scrape(days_2020, months, county, 2020, result)

plot_thelot(result, county)
