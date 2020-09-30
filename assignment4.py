from bs4 import BeautifulSoup
import requests
import pandas as pd
import html 

def scrape(url):
	print("Scraping url: {}".format(url))
	
	tr_list = []
	td_list = []
	
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	
	for tr in soup.findAll('tr', class_="table-primary"):
		td_list.clear()
		for td in tr.findAll('td'):
			td_list.append(td.text.replace('Mandag', '').replace('TromsøForelesning', 'Tromsø Forelesning'))
		tr_list.append(td_list.copy())
		
	return tr_list

def separate_items_create_df(item_list):
	datelist = []
	timelist = []
	roomlist = []
	clist = []
	dlist = []
	tlist = []
	
	for element in item_list:
		datelist.append(element[0])
		timelist.append(element[1])
		roomlist.append(element[2])
		clist.append(element[3])
		dlist.append(element[4])
		tlist.append(element[5])

	d = {"Date":datelist, "Time":timelist, "Room":roomlist, "Course":clist, "Description":dlist, "Teacher":tlist}

	df_schedule = pd.DataFrame.from_dict(d, orient='index')
	
	return df_schedule.transpose()

#seting the url to be scraped 
url = "http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list"

#scare the url and get set the wanted items into a list containing lists of items
time_liste = scrape(url)

#separate equal types of items into lists and create dataframe for the dataset.
df = separate_items_create_df(time_liste)

print(df)