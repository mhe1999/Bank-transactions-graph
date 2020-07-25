from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from pymongo import MongoClient
Builder.load_string('''
<DataTable>:
    id:main_win
    RecycleView:
        viewclass: 'custLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5

<custLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
''')
class DataTable(BoxLayout):
    def __init__(self, table='', SQLheaders='', **kwargs):
        super().__init__(**kwargs)
        products = table
        col_titles = []
        for k in SQLheaders:
            col_titles.append(k[0])
        rows_len = len(products[0])
        total_rows = len(products)
        self.columns = len(col_titles)
        print(rows_len)
        print(total_rows)
        table_data = []
        for t in col_titles:
            table_data.append({'text':str(t), 'size_hint_y':None, 'height':50, 'bcolor':(.06,.45,.45,1)})
        for t in range(total_rows//2):
            for r in range(rows_len):
                table_data.append({'text':str(products[2*t][r]), 'size_hint_y':None, 'height':30, 'bcolor':(.06,.25,.25,1)})
            for r in range(rows_len):
                table_data.append({'text':str(products[2*t +1][r]), 'size_hint_y':None, 'height':30, 'bcolor':(.06,.55,.55,1)})
        if total_rows % 2 == 1:
            for r in range(rows_len):
                table_data.append({'text':str(products[total_rows-1][r]), 'size_hint_y':None, 'height':30, 'bcolor':(.06,.25,.25,1)})


        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data


# class DataTableApp(App):
#     def build(self):
#         return DataTable()
#
# if __name__ == '__main__':
#     DataTableApp().run()
