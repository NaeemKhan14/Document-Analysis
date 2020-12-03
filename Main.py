from DataHandler import DataHandler
from GraphHandler import GraphHandler
from GUIHandler import GUIHandler

#graph = GraphHandler("sample_3m_lines.json")
#g = graph.show_likes_graph("140109173556-a4b921ab7619621709b098aa9de4d736")

gui = GUIHandler()
gui.mainloop()

# data = DataHandler('sample_100k_lines.json')
# top_readers = data.get_top_ten_likes("100806162735-00000000115598650cb8b514246272b5")
# print(top_readers)
#
#graph = GraphHandler("issuu_cw2.json")
#
#graph.get_country_graph("140213232558-bdd53a3a2ae91f2c5f951187668edd50")
# graph.get_continent_graph()
# graph.get_browser_data_graph()
# graph.get_browser_names_graph()
