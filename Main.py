from DataHandler import DataHandler
from GraphHandler import GraphHandler
from GUIHandler import GUIHandler
import argparse


class Main:
    """
    Main class to run the program from CMD.
    This class is made to help with unit testing.
    """
    def run_task(self, file_name, task_id, doc_uuid=None, visitor_uuid=None):
        # File name is required, so every condition needs to check for this.
        if file_name:
            if file_name.split('.')[-1] != 'json':
                return 'Invalid file format. Only .json files are allowed.'
            tasks = ['2a', '2b', '3a', '3b', '4', '5d', '6']
            if task_id in tasks:
                if task_id == '2a':
                    if doc_uuid:  # If document uuid is provided.
                        graph = GraphHandler(file_name)
                        graph.get_country_graph(doc_uuid)
                    else:
                        return 'No document uuid provided. Please use -h for more help.'
                elif task_id == '2b':
                    if doc_uuid:
                        graph = GraphHandler(file_name)
                        graph.get_country_graph(doc_uuid, True)
                        graph.get_continent_graph()
                    else:
                        return 'No document uuid provided. Please use -h for more help.'
                elif task_id == '3a':
                    graph = GraphHandler(file_name)
                    graph.get_browser_data_graph()
                elif task_id == '3b':
                    graph = GraphHandler(file_name)
                    graph.get_browser_names_graph()
                elif task_id == '4':
                    data = DataHandler(file_name)
                    rank = 1
                    print('Rank    Visitor ID      Hours Spent Reading')
                    for values in data.get_top_reader().iteritems():
                        print('{rank}    {visitor_uuid}     {read_time}'.format(rank=rank,
                                                                                visitor_uuid=values[0],
                                                                                read_time=int(values[1])))
                        rank += 1
                elif task_id == '5d':
                    if doc_uuid:
                        data = DataHandler(file_name)
                        rank = 1
                        print('Rank    Visitor ID                    Document ID')
                        for values in data.get_top_ten_likes(doc_uuid, visitor_uuid).iteritems():
                            print('{rank}    {visitor_uuid}     {doc_uuid}'.format(rank=rank,
                                                                                   visitor_uuid=values[0][0],
                                                                                   doc_uuid=values[0][1]))
                            rank += 1
                    else:
                        return 'No document uuid provided. Please use -h for more help.'
                elif task_id == '6':
                    if doc_uuid:
                        graph = GraphHandler(file_name)
                        graph.show_likes_graph(doc_uuid, visitor_uuid)
                    else:
                        return 'No document uuid provided. Please use -h for more help.'
            else:
                return 'Invalid or no task ID given. Please use -h for more help.'
        else:  # If file is not provided.
            print('No file given. Opening GUI instead.')
            gui = GUIHandler()
            gui.mainloop()


if __name__ == '__main__':
    # Set up arguments
    parser = argparse.ArgumentParser(description='Document Helper for analysing data.')
    parser.add_argument("-u", "--visitor_uuid", help="Visitor UUID")
    parser.add_argument("-d", "--doc_uuid", help="Document UUID")
    parser.add_argument("-t", "--task_id", help="Task ID. Available IDs: 2a, 2b, 3a, 3b, 4, 5d, 6")
    parser.add_argument("-f", "--file_name", help="File Name must only be .json file")
    parser.add_argument("-g", "--gui", help="Open GUI")

    args = parser.parse_args()

    m = Main()
    print(m.run_task(args.file_name, args.task_id, args.doc_uuid, args.visitor_uuid))
