from DataHandler import DataHandler
from GraphHandler import GraphHandler
from GUIHandler import GUIHandler
import argparse


if __name__ == '__main__':
    # Set up arguments
    parser = argparse.ArgumentParser(description='Document Helper for analysing data.')
    parser.add_argument("-u", "--visitor_uuid", help="Visitor UUID")
    parser.add_argument("-d", "--doc_uuid", help="Document UUID")
    parser.add_argument("-t", "--task_id", help="Task ID")
    parser.add_argument("-f", "--file_name", help="File Name")
    parser.add_argument("-g", "--gui", help="Open GUI")

    args = parser.parse_args()
    # File name is required, so every condition needs to check for this.
    if args.file_name:
        if args.task_id == '2a':
            if args.doc_uuid:  # If document uuid is provided.
                graph = GraphHandler(args.file_name)
                graph.get_country_graph(args.doc_uuid)
            else:
                print('No document uuid provided. Please use -h for more help.')
        elif args.task_id == '2b':
            if args.doc_uuid:
                graph = GraphHandler(args.file_name)
                graph.get_country_graph(args.doc_uuid)
                graph.get_continent_graph()
            else:
                print('No document uuid provided. Please use -h for more help.')
        elif args.task_id == '3a':
            graph = GraphHandler(args.file_name)
            graph.get_browser_data_graph()
        elif args.task_id == '3b':
            graph = GraphHandler(args.file_name)
            graph.get_browser_names_graph()
        elif args.task_id == '4d':
            data = DataHandler(args.file_name)
            rank = 1
            print('Rank    Visitor ID      Hours Spent Reading')
            for values in data.get_top_ten_likes().iteritems():
                print('{rank}    {visitor_uuid}     {read_time}'.format(rank=rank,
                                                                        visitor_uuid=values[0],
                                                                        read_time=int(values[1])))
                rank += 1
        elif args.task_id == '5':
            if args.doc_uuid:
                data = DataHandler(args.file_name)
                results = data.get_top_ten_likes(args.doc_uuid, args.visitor_uuid)
                rank = 1
                print('Rank    Visitor ID                    Document ID')
                for values in data.get_top_ten_likes(args.doc_uuid, args.visitor_uuid).iteritems():
                    print('{rank}    {visitor_uuid}     {doc_uuid}'.format(rank=rank,
                                                                           visitor_uuid=values[0][0],
                                                                           doc_uuid=values[0][1]))
                    rank += 1
            else:
                print('No document uuid provided. Please use -h for more help.')
        elif args.task_id == '6':
            if args.doc_uuid:
                graph = GraphHandler(args.file_name)
                graph.show_likes_graph(args.doc_uuid, args.visitor_uuid)
            else:
                print('No document uuid provided. Please use -h for more help.')

    else:  # If file is not provided.
        gui = GUIHandler()
        gui.mainloop()

