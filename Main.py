from DataHandler import DataHandler
from GraphHandler import GraphHandler


graph = GraphHandler("sample_3m_lines.json")
#start_time = time.time()
d = graph.show_likes_graph("140213232558-bdd53a3a2ae91f2c5f951187668edd50")
#print("--- %s seconds ---" % (time.time() - start_time))


# top_readers = data.get_top_reader()
# print(top_readers)
#
#graph = GraphHandler("issuu_cw2.json")
#
#graph.get_country_graph("140213232558-bdd53a3a2ae91f2c5f951187668edd50")
# graph.get_continent_graph()
# graph.get_browser_data_graph()
# graph.get_browser_names_graph()
