from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from pymongo import MongoClient
from utils.datatable import  DataTable
import pyodbc


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.widgettable = Label()
        # self.outtt()

    def on_spinner_select(self, text):
        print (text)
        table_name = ''
        if text == 'Customer table':
            table_name = 'Customer'
        elif text == 'transactions':
            table_name = 'Trn_Src_Des'
        elif text == 'Deposits':
            table_name = 'Deposit'
        elif text == 'Deposits type':
            table_name = 'Deposit_Type'
        elif text == 'Deposits status':
            table_name = 'Deposit_Status'
        elif text == 'Branchs':
            table_name = 'Branch'

        self.outtt(table_name)

    def outtt(self , table_name):
        conn = pyodbc.connect('Driver={SQL Server};'
                                  'Server=DESKTOP-7MGG4HH;'
                                  'Database=bank_trn;'
                                  'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bank_trn.dbo.%s' % (table_name))
        SQLtable = cursor.fetchall()

        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '%s'" % (table_name,))
        SQLheaders = cursor.fetchall()

        self.widgettable = DataTable(table = SQLtable, SQLheaders = SQLheaders)
        content = self.ids.Bscrn_content
        content.clear_widgets()
        whatever = self.ids.whatever

        content.add_widget(whatever)
        content.add_widget(self.widgettable)




    def change_screen(self, instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text =='customers INFO':
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'



class AdminApp(App):
    def build(self):
        return AdminWindow()

if __name__ == '__main__':
    AdminApp().run()
