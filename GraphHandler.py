import matplotlib.pyplot as plt
from DataHandler import DataHandler


class GraphHandler:
    """
    This class is used to get the Pandas data from DataHandler
    class and use matplotlib to show their respective graphs.
    """
    def __init__(self, file_name):
        """
        Constructor of the class which is used to get the filename to create
        a global variable to be used throughout the file. This is to avoid
        querying the file repetitively each time we need something from it.
        :param file_name: .json file name.
        """
        self.data = DataHandler(file_name)

    def get_country_graph(self, doc_uuid):
        """
        Shows the country graph.
        :param doc_uuid: Unique document ID located in the .json file.
        :return: Graph of the country data.
        """
        country = self.data.get_country_name(doc_uuid)
        country.value_counts().plot(kind='bar', title='Countries')
        return plt.show()

    def get_continent_graph(self):
        """
        Shows the continent graph.
        :return: Graph of the continents data.
        """
        continent = self.data.get_continents()
        continent.value_counts().plot(kind='bar', title='Continents')
        return plt.show()

    def get_browser_data_graph(self):
        """
        Shows the graph of all browser meta-data.
        :return: Graph of browser meta-data.
        """
        browser_metadata = self.data.get_browser_data()
        browser_metadata.value_counts().plot(kind='bar', title='Browser Data')
        return plt.show()

    def get_browser_names_graph(self):
        """
        Shows the graph of browser agents.
        :return: Graph of different browser agents.
        """
        browser_names = self.data.get_browser_name()
        browser_names.value_counts().plot(kind='bar', title='Browser Names')
        return plt.show()

