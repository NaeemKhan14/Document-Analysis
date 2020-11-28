import pandas as pd
import pycountry_convert as pc


class DataHandler:
    """
    This class contains all the methods that will help us in
    processing the data out of .json files. It is responsible
    for creating and serving of all the pandas datasets/series.
    """
    def __init__(self, file_name):
        """
        Constructor of the class is used to get the name/path of the
        .json file to work with. It also creates the 'doc' variable
        which is used throughout the class to avoid loading the
        results repetitively and work with a single dataset.
        :param file_name: Name of the .json file.
        """
        self.country_codes = None
        self.doc = pd.read_json(file_name, lines=True)
        # Pandas dataset properties
        pd.set_option("max_columns", None)      # Displays all the columns in result
        pd.set_option("max_colwidth", None)     # Stretches the results to full column width
        pd.set_option("max_rows", None)         # Displays the max number of rows
        pd.set_option("max_seq_item", None)     # Shows all results by removing "..." from results

    def get_country_name(self, doc_uuid):
        """
        Converts the ISO 3166-1 country codes into country names for
        the given document. The document is searched through the
        doc_uuid found inside the .json file and for each result found,
        the corresponding visitor_country name is displayed.
        :param doc_uuid: Unique ID of the document read on the website.
        :return: Pandas dataset with all the country names.
        """
        # Fetch the results containing visitors' country codes which viewed this document
        results = self.doc.loc[self.doc['subject_doc_id'] == doc_uuid, 'visitor_country']
        # Convert all ISO 3166-1 alpha-3 country names to ISO 3166-1 alpha-2 country names.
        # This is to ensure that we don't get any errors later on converting them to
        # continent codes as pycountry_convert can only convert ISO 3166-1 alpha-2 country
        # names to continent codes.
        self.country_codes = results.apply(lambda x: pc.country_alpha3_to_country_alpha2(x) if len(x) == 3 else x)
        country_names = self.country_codes.apply(lambda x: pc.country_alpha2_to_country_name(x))

        return country_names

    def get_continents(self):
        """
        Converts the country codes into continent codes to get continent
        names.
        :return: Pandas series containing all the continent names.
        """
        continent_codes = self.country_codes.apply(lambda x: pc.country_alpha2_to_continent_code(x))
        continent_names = continent_codes.apply(lambda x: pc.convert_continent_code_to_continent_name(x))

        return continent_names

    def get_browser_data(self):
        """
        Gets all of the visitor_useragent column from the document.
        :return: Pandas series containing the entire visitor_useragent column of the document.
        """
        return self.doc['visitor_useragent']

    def get_browser_name(self):
        """
        Gets the browser agent from each entry of the file.
        :return: Pandas series containing browser agents.
        """
        # We split each entry of visitor_useragent column using "/" as the user
        # agents are always the first word of the sentence followed by "/". So
        # after splitting it, the browser agent is always going to be at index 0.
        return self.doc.visitor_useragent.apply(lambda x: x.split("/")[0])

    def get_top_reader(self):
        """
        Gets the top 10 readers from the .json document based on their read time.
        :return: Pandas dataset containing top 10 readers.
        """
        top_readers = self.doc.groupby(['visitor_uuid'])['event_readtime'].sum()
        return top_readers.nlargest(10)

    #################################
    # Also-likes functions (Task 5) #
    #################################
    # Task 5a
    def get_visitors_uuid(self, doc_uuid):
        """
        Gets list of all visitors' uuid which have read the given document.
        :param doc_uuid: Uuid of the document to get visitors' list from.
        :return: Visitors' uuid column of the .json file for the given doc_uuid.
        """
        return self.doc.loc[self.doc['subject_doc_id'] == doc_uuid, 'visitor_uuid']

    # Task 5b
    def get_documents_uuid(self, visitor_uuid):
        """
        Gets the list of documents read by the given visitor.
        :param visitor_uuid: Uuid of the visitor.
        :return: Documents' Uuid read by the given visitor.
        """
        return self.doc.loc[self.doc['visitor_uuid'] == visitor_uuid, 'subject_doc_id']

    # Task 5c.1
    def sort_documents_liked(self, doc_uuid):
        """
        Sorting function to get similar books related to the given document.
        :param doc_uuid: Document ID to find similar books for.
        :return: List of books read by users who have read the same book.
        """
        # Gets a boolean mask of the entire document where True will only be the values
        # where doc_uuid is present.
        docs_mask = self.doc['subject_doc_id'].eq(doc_uuid)
        # self.doc.loc[docs_mask, 'visitor_uuid'] = Gets the visitors' ID who have read the document
        # with our given doc_uuid.
        return self.doc.loc[self.doc['visitor_uuid'].isin(self.doc.loc[docs_mask, 'visitor_uuid']), ['visitor_uuid','subject_doc_id']]

    # Task 5c.2
    def get_user_also_likes(self, doc_uuid, visitor_uuid='', sort=sort_documents_liked):
        return sort(self, doc_uuid)

    # Task 5d
    def get_top_ten_likes(self, doc_uuid, sort=sort_documents_liked):
        return sort(self, doc_uuid).value_counts().nlargest(10)


