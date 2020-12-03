import matplotlib.pyplot as plt
from DataHandler import DataHandler
from graphviz.dot import Digraph


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
        plt.savefig('countries_graph.png', bbox_inches='tight')
        return plt.show()

    def get_continent_graph(self):
        """
        Shows the continent graph.
        :return: Graph of the continents data.
        """
        continent = self.data.get_continents()
        continent.value_counts().plot(kind='bar', title='Continents')
        plt.savefig('continents_graph.png', bbox_inches='tight')
        return plt.show()

    def get_browser_data_graph(self):
        """
        Shows the graph of all browser meta-data.
        :return: Graph of browser meta-data.
        """
        browser_metadata = self.data.get_browser_data()
        browser_metadata.value_counts().plot(kind='bar', title='Browser Data')
        plt.savefig('browser_data_graph.png', bbox_inches='tight')
        return plt.show()

    def get_browser_names_graph(self):
        """
        Shows the graph of browser agents.
        :return: Graph of different browser agents.
        """
        browser_names = self.data.get_browser_name()
        browser_names.value_counts().plot(kind='bar', title='Browser Names')
        plt.savefig('browser_names_graph.png', bbox_inches='tight')
        return plt.show()

    def show_likes_graph(self, doc_uuid, visitor_uuid=None):
        """
        Makes the graph from the results taken from DataHandler.get_top_ten_likes()
        function.
        :param doc_uuid: Document ID taken from the .json file.
        :param visitor_uuid: (Optional) Visitor Document ID taken from the .json file.
        """
        graph = Digraph("likes_graph")
        graph_data = self.data.get_top_ten_likes(doc_uuid, visitor_uuid).iteritems()
        # Go through each element in the list.
        for g_data in graph_data:
            # Takes the last 4 digits of visitor and doc ID.
            visitor_id = g_data[0][0][-4:]
            doc_id = g_data[0][1][-4:]
            # If the visitor or doc ID of this iteration value matches
            # the ones taken from function parameter, we set a color
            # scheme for them. Otherwise they are directly added to the
            # graph.
            if visitor_uuid and visitor_id == visitor_uuid[-4:]:
                graph.node(visitor_id, color='green', style='filled', shape='box')
            else:
                graph.node(visitor_id, shape='box')

            if doc_id == doc_uuid[-4:]:
                graph.node(doc_id, color='green', style='filled', shape='circle')
            else:
                graph.node(doc_id, shape='circle')
            graph.edge(visitor_id, doc_id)
        if visitor_uuid:
            graph.node(visitor_uuid[-4:], color='green', style='filled', shape='box')
            graph.edge(visitor_uuid[-4:], doc_uuid[-4:])

        graph.render("likes_graph.gv", view=True)

