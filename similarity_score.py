import pandas as pn
import re
import difflib


class IV:

    def run(self):
        filename = "/home/venkatramanann/Downloads/Jll125K_AllMatcheddata.xls"
        data = pn.ExcelFile(filename)
        df = data.parse(data.sheet_names[0])
        df = df.fillna('')
        df['company_similarity_score'] = map(self.find_similarity, df['company_name'], df['IV Name'])
        df['city_similarity_score'] = map(self.find_similarity, df['city'], df['IV_City'])
        df['state_similarity_score'] = map(self.find_similarity, df['state_province'], df['State'])
        df['country_similarity_score'] = map(self.find_similarity, df['country'], df['IV_Country'])
        df['street_similarity_score'] = map(self.find_similarity, df['address_line_1'], df['Address'])
        df['postalcode_similarity_score'] = map(self.find_similarity, df['postal_code'], df['IV_postal_code'])
        df['website_similarity_score'] = map(self.find_similarity, df['Website'], df['IV_Website'])
        output = "/home/venkatramanann/Desktop/Jll125K_AllMatcheddata_SimilarityScore.csv"
        df.to_csv(output, sep=',', encoding='utf-8')

    def replace_brackets(self, company_name):
        return re.sub(r'\([^)]*\)', '', company_name)

    def get_brackets_val(self, company_name):
        try:
            m = re.search(r'([^(]+)\s*\(([^)]+)\)\s*', company_name)
            return m.group(2)
        except Exception as e:
            print e
            pass

    def find_similarity(self, source_name, srch_name):
        try:
            seq = difflib.SequenceMatcher(a=source_name.lower(), b=srch_name.lower())
            return seq.ratio()
        except Exception as e:
            print e
            pass

    def replace_hash(self, company_name):
        return company_name.replace("#", "")

if __name__ == '__main__':
    iv = IV()
    iv.run()
