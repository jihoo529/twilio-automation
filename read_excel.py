import pandas as pd

class ReadExcel:
    def __init__(self):
        self.col_names = ['Template name', 'Footer', 'Call to Action', 'Unnamed: 4', 'Message Content', 'Three Quick button reply', 'Category ', 'Language', 'Account SID']
        self.sheet_name = 'test3'
        self.file_path = r'C:\Users\02009465\Documents\automation\card.xlsx'

    def remove_blank(self,text):
        return text.replace(" ", "")
    def read_data(self):
        df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)

        self.template = df.to_dict()
        print(self.template)
        self.temp_name = self.template['Template name'][0].lower()
        self.img_name = self.temp_name
        self.temp_body = self.template['Message Content'][0]
        self.temp_footer = self.template['Footer'][0]


        if pd.isna(self.template['Three Quick button reply'][0]):
            self.btn_type = 'Call to Action'
            d1 = dict()

            for i in self.template['Call to Action']:
                value = self.template['Unnamed: 4'][i]
                new_value = self.remove_blank(value)
                d1[self.template['Call to Action'][i]] = new_value

            self.call_to_action_opts = d1

        else:
            self.btn_type = 'Quick Reply'
            self.quick_reply_opts = self.template['Three Quick button reply']


        self.temp_type = 'Card'
        self.temp_lang = self.template['Language'][0]
        self.temp_category = self.template['Category '][0]

        for idx ,value in self.template['Message Content'].items():
            if pd.isna(value):
                continue
            # print(value)
