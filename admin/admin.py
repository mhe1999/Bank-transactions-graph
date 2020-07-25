from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from pymongo import MongoClient
from utils.datatable import  DataTable
import pyodbc
import re



class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def on_spinner_select(self, text):
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

        self.SQLquery(table_name)

    def SQLquery(self , table_name):
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
        content = self.ids.Bscrn_customerINFO
        content.clear_widgets()
        whatever = self.ids.whatever

        content.add_widget(whatever)
        content.add_widget(self.widgettable)

    def change_screen(self, instance):
        if instance.text == 'transaction path graph':
            self.ids.scrn_mngr.current = 'scrn_graph'
        elif instance.text =='customers INFO':
            self.ids.scrn_mngr.current = 'scrn_customerINFO'
        else:
            self.ids.scrn_mngr.current = 'scrn_CRUD'
            # self.ids.voucherID.focus = 'True'

    def insert_data(self):
        if str(self.ids.voucherID.text) == '':
            self.ids.error_message.text = '[color=#FF0000]voucherID cant be empty[/color]'
        elif self.ids.voucherID.text.isnumeric() == False :
            self.ids.error_message.text = '[color=#FF0000]voucherID should be a number[/color]'
        elif self.ids.date.text == '':
            self.ids.error_message.text = '[color=#FF0000]data cant be empty[/color]'
        elif re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]',self.ids.date.text) == None:
            self.ids.error_message.text = '[color=#FF0000]date should be in 1400-01-01 form[/color]'
        elif self.ids.time.text == '':
            self.ids.error_message.text = '[color=#FF0000]time cant be empty[/color]'
        elif re.search('[0-2][0-9][0-6][0-9][0-6][0-9]',self.ids.time.text) == None:
            self.ids.error_message.text = '[color=#FF0000]time should be in 246060 form[/color]'
        elif str(self.ids.amount.text) == '':
            self.ids.error_message.text = '[color=#FF0000]amount cant be empty[/color]'
        elif self.ids.amount.text.isnumeric() == False :
            self.ids.error_message.text = '[color=#FF0000]amount should be a number[/color]'
        elif self.ids.Source_Deposit.text.isnumeric() == False and self.ids.Source_Deposit.text != '':
            self.ids.error_message.text = '[color=#FF0000]Source_Deposit should be a number[/color]'
        elif self.ids.Destination_Deposit.text.isnumeric() == False and self.ids.Destination_Deposit.text != '' :
            self.ids.error_message.text = '[color=#FF0000]Destination_Deposit should be a number[/color]'




class AdminApp(App):
    def build(self):
        return AdminWindow()

if __name__ == '__main__':
    AdminApp().run()
