from tkinter import *
from tkinter import ttk
import sqlite3
import webbrowser


class Window:
    def __init__(self, width, height, title='MyWindow', resizable=(False, True), icon=None):
        '''Program window designer(options)'''
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}+670+450')
        self.root.resizable(resizable[0], resizable[1])

    def run(self):
        '''Start the program and widget creation functions'''
        self.draw_widgets()
        self.root.mainloop()

    def draw_widgets(self):
        '''Создание виджетов
        ___
            Widget creation'''
        l1 = Label(self.root, text="RAM")
        l2 = Label(self.root, text="Other")
        l3 = Label(self.root, text="Color")
        l4 = Label(self.root, text="Min. Price")
        l5 = Label(self.root, text="Max. Price")

        l1.grid(row=0, column=0, padx=5, pady=5)
        l2.grid(row=0, column=1, padx=5, pady=5)
        l3.grid(row=0, column=2, padx=5, pady=5)
        l4.grid(row=0, column=3, padx=5, pady=5)
        l5.grid(row=0, column=4, padx=5, pady=5)

        self.ram_enter = ttk.Entry(self.root, width=15)
        self.other_enter = ttk.Entry(self.root, width=15)
        self.color_enter = ttk.Entry(self.root, width=15)
        self.min_price_enter = ttk.Entry(self.root, width=15)
        self.max_price_enter = ttk.Entry(self.root, width=15)
        SearchButton = ttk.Button(self.root, text="Search", command=self.printRecords)

        SearchButton.grid(row=2, column=0, columnspan=5, padx=5, pady=5, sticky=EW)
        self.ram_enter.grid(row=1, column=0, padx=5, pady=5)
        self.other_enter.grid(row=1, column=1, padx=5, pady=5)
        self.color_enter.grid(row=1, column=2, padx=5, pady=5)
        self.min_price_enter.grid(row=1, column=3, padx=5, pady=5)
        self.max_price_enter.grid(row=1, column=4, padx=5, pady=5)

    def printRecords(self):
        '''Database connection, input processing, database generation and query,
        results output in the form of interactive widgets'''
        connection = sqlite3.connect('s2b_test.db')
        cur = connection.cursor()
        ram = self.ram_enter.get()
        other = self.other_enter.get()
        color = self.color_enter.get()
        min_price = self.min_price_enter.get()
        max_price = self.max_price_enter.get()

        description = (f'%{ram}/%{other}%{color}%')
        cur.execute('''SELECT * FROM smartphones WHERE model LIKE ? 
        AND price BETWEEN ? AND ? 
        AND availability_status = 'Є в наявності' GROUP BY model''',
                    (description, min_price, max_price))  # GROUP BY model - delete multiple duplicates in the response


        results = cur.fetchall()
        count = 0
        row_button = 3

        for i in results:
            count += 1
            link_to = f"{i[3]}"
            cmd = lambda link_to=link_to: self.open_browser(
                link_to)  # link processing function, without lambda set the last iteration result
            web_button = ttk.Button(self.root, text=f"{i[1]}, цена {i[4]}", command=cmd)
            web_button.grid(row=row_button, column=0, columnspan=5, sticky=EW, padx=5, pady=5)
            row_button += 1
            print(i)

    def open_browser(self, link):
        '''Opening a web document link in your browser'''
        webbrowser.open(link)


if __name__ == '__main__':
    window = Window(670, 450, 'Model Search')
    window.run()
