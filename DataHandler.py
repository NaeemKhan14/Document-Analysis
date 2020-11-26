import pandas as pd
import pycountry_convert as pc


class DataHandler:

    def __init__(self, file_name):
        self.country_codes = None
        self.doc = pd.read_json(file_name, lines=True)

        pd.set_option("max_columns", None)      # Displays all the columns in result
        pd.set_option("max_colwidth", None)     # Stretches the results to full column width
        pd.set_option("max_rows", None)         # Displays the max number of rows
        pd.set_option("max_seq_item", None)     # Shows all results by removing "..." from results

    def get_country_name(self, doc_uuid):
        results = self.doc.loc[self.doc['subject_doc_id'] == doc_uuid, 'visitor_country']
        # Convert all ISO 3166-1 alpha-3 country names to ISO 3166-1 alpha-2 country names
        self.country_codes = results.apply(lambda x: pc.country_alpha3_to_country_alpha2(x) if len(x) == 3 else x)
        country_names = self.country_codes.apply(lambda x: pc.country_alpha2_to_country_name(x))

        return country_names

    def get_continents(self):
        continent_codes = self.country_codes.apply(lambda x: pc.country_alpha2_to_continent_code(x))
        continent_names = continent_codes.apply(lambda x: pc.convert_continent_code_to_continent_name(x))

        return continent_names

    def get_browser_data(self):
        return self.doc['visitor_useragent']

    def get_browser_name(self):
        return self.doc.visitor_useragent.apply(lambda x: x.split("/")[0])
