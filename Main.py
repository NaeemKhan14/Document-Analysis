from DataHandler import DataHandler
from GraphHandler import GraphHandler

data = DataHandler("issuu_cw2.json")
print(data.get_user_also_likes("100713205147-2ee05a98f1794324952eea5ca678c026"))
# top_readers = data.get_top_reader()
# print(top_readers)
#
# graph = GraphHandler("issuu_cw2.json")
#
# graph.get_country_graph("131224090853-45a33eba6ddf71f348aef7557a86ca5f")
# graph.get_continent_graph()
# graph.get_browser_data_graph()
# graph.get_browser_names_graph()
