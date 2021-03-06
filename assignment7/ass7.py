import matplotlib.pyplot as plt

def read_data(filename):
	results = {
		"M":{},
		"F":{}
	}
	count = 0
	with open(filename, "rb") as f:
		data = f.readline()
		while(data):
			month = data[12:14].decode("utf-8")
			day = data[22:23].decode("utf-8")
			sex = data[474:475].decode("utf-8")
			weight= data[503:507].decode("utf-8")
			
			if month not in results[sex]:
				results[sex][month] = {}
			
			if day not in results[sex][month]:
				results[sex][month][day] = {"amount":0, "weight":0}

			results[sex][month][day]["amount"] += 1
			results[sex][month][day]["weight"] += int(weight)
	
			data = f.readline()

			count += 1

	print("read {} lines from {}".format(count, filename))
	return results
			

def wrangle(data):
	total = 0

	female_days= [0,0,0,0,0,0,0]
	male_days  = [0,0,0,0,0,0,0]

	female_total = 0
	male_total  = 0

	male_weight = 0
	female_weight  = 0

	for gender in data:
		months = data[gender]
		for month in months:
			days = months[month]
			for day in days:
				if gender == "M":
					male_days[int(day)-1] += days[day]['amount']
					male_total += days[day]['amount']
					male_weight += days[day]['weight']

				else:
					female_days[int(day)-1] += days[day]['amount']
					female_total += days[day]['amount']
					female_weight += days[day]['weight']
			
				total += days[day]['amount']

	return female_days, male_days, female_total, male_total, female_weight, male_weight
	
def bar_plot(f, m, title, name):

	year = ["2018", "2019"]

	plt.figure(name)
	plt.bar(year, m, label="Males births")
	plt.bar(year, f, label="Female births")
	plt.title(title)
	plt.legend(loc="best")
	plt.show()

def bar_plot_days(f_18, f_19, m_18, m_19):

	year = ["Sun", "Mon", "Tue", "Wed", "Thi", "Fri", "Sat"]

	plt.figure("births per day")
	plt.ylim(0,500000)
	
	plt.bar(year, m_18, label="Male births 2018")
	plt.bar(year, m_19, label="Males births 2019")
	plt.bar(year, f_18, label="Females births 2018")
	plt.bar(year, f_19, label="Female births 2019")

	plt.title("Gender born per day 2018/2019")
	plt.legend(loc="best")
	plt.show()

df_2018 = read_data("Nat2018us/2018.txt")
df_2019 = read_data("Nat2019us/2019.txt")

f_days_2018, m_days_2018, f_total_2018, m_total_2018, f_weight_2018, m_weight_2018 = wrangle(df_2018)
f_days_2019, m_days_2019, f_total_2019, m_total_2019, f_weight_2019, m_weight_2019 = wrangle(df_2019)

percent_f_18 = (f_total_2018 / (f_total_2018 + m_total_2018 )) * 100
percent_f_19 = (f_total_2019 / (f_total_2019 + m_total_2019 )) * 100

percent_m_18 = (m_total_2018 / (f_total_2018 + m_total_2018 )) * 100
percent_m_19 = (m_total_2019 / (f_total_2019 + m_total_2019 )) * 100

total_females = [percent_f_18, percent_f_19]
total_males = [percent_m_18, percent_m_19]

average_weight_male_2018 = m_weight_2018 / m_total_2018
average_weight_female_2018 = f_weight_2018 / f_total_2018
average_weight_male_2019 = m_weight_2019 / m_total_2019
average_weight_female_2019 = f_weight_2019 / f_total_2019

average_weight_f = [average_weight_female_2018, average_weight_female_2019 ]
average_weight_m = [average_weight_male_2018, average_weight_male_2019 ]

bar_plot(total_females, total_males, "Difference in genders born in percentage", "Born: Females VS Males")
bar_plot(average_weight_f, average_weight_m, "Difference in average weight for genders", "Weight: Born: Females VS Males")

bar_plot_days(f_days_2018, f_days_2019, m_days_2018, m_days_2019) 
