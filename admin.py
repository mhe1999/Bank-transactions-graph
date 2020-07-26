from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from utils.datatable import DataTable
import pyodbc
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import gc

class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idx = 0
        gc.disable()

    def on_spinner_select(self, text):

        self.ids.whatever = self.ids.whatever.__self__
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
        self.ids.whatever = self.ids.whatever.__self__

    def SQLquery(self, table_name):
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-7MGG4HH;'
                              'Database=bank_trn;'
                              'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bank_trn.dbo.%s' % (table_name))
        SQLtable = cursor.fetchall()

        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '%s'" % (table_name,))
        SQLheaders = cursor.fetchall()

        self.widgettable = DataTable(table=SQLtable, SQLheaders=SQLheaders)
        content = self.ids.Bscrn_customerINFO
        content.clear_widgets()
        whatever = self.ids.whatever

        content.add_widget(whatever)
        content.add_widget(self.widgettable)

    def change_screen(self, instance):
        if instance.text == 'transaction path graph':
            self.ids.scrn_mngr.current = 'scrn_graph'
        elif instance.text == 'customers INFO':
            self.ids.scrn_mngr.current = 'scrn_customerINFO'
            if self.ids.whatever.text != 'Choose a table':
                self.on_spinner_select(self.ids.whatever.text)
        else:
            self.ids.scrn_mngr.current = 'scrn_CRUD'

    def insert_data(self):
        if self.ids.voucherID.text == '':
            self.ids.error_message.text = '[color=#FF0000]voucherID cant be empty[/color]'
        elif not self.ids.voucherID.text.isnumeric():
            self.ids.error_message.text = '[color=#FF0000]voucherID should be a number[/color]'
        elif self.ids.date.text == '':
            self.ids.error_message.text = '[color=#FF0000]data cant be empty[/color]'
        elif re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', self.ids.date.text) == None:
            self.ids.error_message.text = '[color=#FF0000]date should be in 1400-01-01 form[/color]'
        elif self.ids.time.text == '':
            self.ids.error_message.text = '[color=#FF0000]time cant be empty[/color]'
        elif re.search('[0-2][0-9][0-6][0-9][0-6][0-9]', self.ids.time.text) == None:
            self.ids.error_message.text = '[color=#FF0000]time should be in 246060 form[/color]'
        elif str(self.ids.amount.text) == '':
            self.ids.error_message.text = '[color=#FF0000]amount cant be empty[/color]'
        elif not self.ids.amount.text.isnumeric():
            self.ids.error_message.text = '[color=#FF0000]amount should be a number[/color]'
        elif self.ids.Source_Deposit.text.isnumeric() == False and self.ids.Source_Deposit.text != '':
            self.ids.error_message.text = '[color=#FF0000]Source_Deposit should be a number[/color]'
        elif self.ids.Destination_Deposit.text.isnumeric() == False and self.ids.Destination_Deposit.text != '':
            self.ids.error_message.text = '[color=#FF0000]Destination_Deposit should be a number[/color]'
        else:
            self.ids.error_message.text = '[color=#00FF00]every things good, working on it...[/color]'

            sql_voucherID = self.ids.voucherID.text
            sql_date = self.ids.date.text
            sql_time = self.ids.time.text
            sql_amount = int(self.ids.amount.text)
            if self.ids.Source_Deposit.text != '':
                sql_Source_Deposit = int(self.ids.Source_Deposit.text)
            else:
                sql_Source_Deposit = None
            if self.ids.Destination_Deposit.text != '':
                sql_Destination_Deposit = int(self.ids.Destination_Deposit.text)
            else:
                sql_Destination_Deposit = None
            if self.ids.Branch_ID.text != '':
                sql_Branch_ID = int(self.ids.Branch_ID.text)
            else:
                sql_Branch_ID = None

            try:
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=DESKTOP-7MGG4HH;'
                                      'Database=bank_trn;'
                                      'Trusted_Connection=yes;')

                cursor = conn.cursor()
                cursor.execute('INSERT INTO bank_trn.dbo.Trn_Src_Des VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (
                    sql_voucherID, sql_date, sql_time, sql_amount, sql_Source_Deposit, sql_Destination_Deposit,
                    sql_Branch_ID, None))
                conn.commit()
                self.ids.error_message.text = '[color=#00FF00]row successfuly added[/color]'

            except:
                self.ids.error_message.text = '[color=#FF0000]there is a problem with server[/color]'

    def delete_data(self):
        if self.ids.voucherID_delete.text == '':
            self.ids.error_message_delete.text = '[color=#FF0000]voucherID cant be empty[/color]'
        elif not self.ids.voucherID_delete.text.isnumeric():
            self.ids.error_message_delete.text = '[color=#FF0000]voucherID should be a number[/color]'

        else:
            sql_voucherID = self.ids.voucherID_delete.text
            try:
                conn = pyodbc.connect('Driver={SQL Server};'
                                      'Server=DESKTOP-7MGG4HH;'
                                      'Database=bank_trn;'
                                      'Trusted_Connection=yes;')

                cursor = conn.cursor()
                cursor.execute('DELETE FROM bank_trn.dbo.Trn_Src_Des WHERE VoucherId = %s' % (sql_voucherID,))
                conn.commit()
                self.ids.error_message_delete.text = '[color=#00FF00]row successfuly deleted[/color]'

            except:
                self.ids.error_message_delete.text = '[color=#FF0000]there is a problem with server[/color]'

    def find_nexts_in_graph(self, voucherID, cursor, G, edge_labels):
        cursor.execute('EXEC [dbo].[myproc] @VoucherId = %d' % (voucherID,))
        cursor.execute('SELECT * FROM bank_trn.dbo.%s' % ('final',))
        table = cursor.fetchall()

        for row in table:
            if row[5] == None:
                print(self.idx)
                row[5] = 'out' + str(self.idx)
                self.idx += 1
            G.add_node(row[4])
            G.add_node(row[5])
            G.add_edge(row[4], row[5])
            edge_labels[(row[4], row[5])] = str(row[3]) + '\n' + row[1] + '\n' + row[2]
            self.find_nexts_in_graph(int(row[0]), cursor, G, edge_labels)

    def find_previous_in_graph(self, voucherID, cursor, G, edge_labels):
        cursor.execute('EXEC [dbo].[myproc_back] @VoucherId = %d' % (voucherID,))
        cursor.execute('SELECT * FROM bank_trn.dbo.%s' % ('final_back',))
        table = cursor.fetchall()
        # print(table)
        # input("damn")
        for row in table:
            if row[4] == None:
                row[4] = 'out' + str(self.idx)
                self.idx += 1
            G.add_node(row[4])
            G.add_node(row[5])
            G.add_edge(row[4], row[5])
            edge_labels[(row[4], row[5])] = str(row[3]) + '\n' + row[1] + '\n' + row[2]
            self.find_previous_in_graph(int(row[0]), cursor, G, edge_labels)

    def create_graph(self):
        G1 = nx.DiGraph()
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=DESKTOP-7MGG4HH;'
                              'Database=bank_trn;'
                              'Trusted_Connection=yes;')
        cursor = conn.cursor()
        edge_labels1 = dict()

        self.find_nexts_in_graph(int(self.ids.graph_ID.text), cursor, G1, edge_labels1)
        self.find_previous_in_graph(int(self.ids.graph_ID.text), cursor, G1, edge_labels1)
        print(self.ids.graph_ID.text)
        print(type(self.ids.graph_ID.text))
        cursor.execute('SELECT * FROM bank_trn.dbo.%s WHERE VoucherId = %s ' % ('Trn_Src_Des', self.ids.graph_ID.text))
        table = cursor.fetchall()
        G1.add_edge(table[0][4], table[0][5])
        edge_labels1[(table[0][4], table[0][5])] = str(table[0][3]) + '\n' + table[0][1] + '\n' + table[0][2]
        print(table)

        pos1 = graphviz_layout(G1, prog='dot', args="-Grankdir=LR")
        nx.draw(G1, pos1, font_size=8, edge_color='black', width=1, linewidths=1,
                node_size=400, node_color='#0F7373', alpha=1,
                labels={node: node for node in G1.nodes()})
        nx.draw_networkx_edge_labels(G1, pos1, font_size=8, font_color='#0F7373', edge_labels=edge_labels1)

        print(self.ids.graph_image.source)
        try:
            index = int(self.ids.graph_image.source[-5]) + 1
        except:
            index = 0
        name = "simple_path" + str(index) + ".jpg"
        plt.savefig(name)
        self.ids.graph_image.source = name

        print(self.ids.graph_image.source)
        plt.show()


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == '__main__':
    AdminApp().run()
