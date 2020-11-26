import matplotlib.pyplot as plt
from DataHandler import DataHandler

data = DataHandler("issuu_cw2.json")

country = data.get_country_name("131224090853-45a33eba6ddf71f348aef7557a86ca5f")
country.value_counts().plot(kind='bar', title='Countries')
plt.show()

continent = data.get_continents()
continent.value_counts().plot(kind='bar', title='Continents')
plt.show()

browser_metadata = data.get_browser_data()
browser_metadata.value_counts().plot(kind='bar', title='Browser Data')

plt.show()

browser_names = data.get_browser_name()
browser_names.value_counts().plot(kind='bar', title='Browser Names')
plt.show()
