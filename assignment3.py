from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape(url, lang):
	print("Scraping url: {}".format(url))
	tech = []
	language = []

	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	
	for h4 in soup.findAll('h4', class_="course-block__title"):
		tech.append(h4.text.strip())
		language.append(lang)


	return tech, language

def concat_lists(l1, l2):
	return l1 + l2
	
def make_df(list1, list2, name1, name2):
	print("creating the dataframe, names for columns: {}, {}".format(name1, name2))
	d = {name1:list1, name2:list2}

	df = pd.DataFrame.from_dict(d, orient='index')

	return df


url_1 = "https://www.datacamp.com/courses/tech:r"
url_2 = "https://www.datacamp.com/courses/tech:python"

r_list, r_language = scrape(url_1, "R")
p_list, p_language = scrape(url_2, "Python")

tech = concat_lists(r_list, p_list)
language = concat_lists(r_language, p_language)

df_coursenames = make_df(tech, language, "Tech", "Language")
df_coursenames = df_coursenames.transpose()

print("Data Frame Created looks like this:")
print(df_coursenames)