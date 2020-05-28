import tkinter as tk
from tkinter import ttk
import matplotlib as mpl
from matplotlib import style
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import os
import data_processing as dp
import backtesting as bt
import data_mining as dm


# GUI setting
mpl.rcParams['lines.linewidth'] = 1  # define the line width in all graphs
mpl.use("TkAgg")  # let matplotlib work with tkinter
style.use('ggplot')  # define graph style
TITLE_FONT = ("Verdana", 30)  # define title font

# cross page global variable
stock = "AAPL"  # current looking stock
last_stock = "no"
search_entry = "AAPL"  # search bar value
fig = plt.figure()  # init figure
period = 30
update_toggle = False
mode = "start"

# page instance
advance_instance = "no"
backtest_instance = "no"
heatmap_instance = "no"
basic_instance = "no"
#test_instance = "no"

# basic page global variable
basic_criteria = ["High", "Low"]

# advance page global variable
advance_window = "no"
advance = "no"
advance_type = "candle"
display_volume = False
display_nontrading = False
mav_tuple = ()

# heatmap page global variable
search_corr = "AAPL"
corr_list = ["AAPL", "WU", "GOOGL", "GD", "GM", "ADM"]

# backtest page global var
min_entry = "5"
max_entry = "30"
min_emas = [3,5,8,10,12,15]
max_emas = [30,35,40,45,50,60]
ress1 = 0
ress2 = 0
ress3 = 0
ress4 = 0
ress5 = 0
ress6 = 0
ress7 = 0
ress8 = 0
ress9 = 0


def animate(i):
    global update_toggle
    if mode == "advance" and not update_toggle:
        update_toggle = True
        advance_instance.update_fig()
    elif mode == "heatmap" and not update_toggle:
        update_toggle = True
        heatmap_instance.update_fig()
    elif mode == "backtest" and not update_toggle:
        update_toggle = True
        backtest_instance.update_label()
    elif mode == "basic" and not update_toggle:
        update_toggle = True
        basic_instance.update_fig()
    else:
        pass


def change_stock():
    global stock, last_stock, search_entry, update_toggle
    update_toggle = False
    last_stock = stock
    tmp = search_entry.get().upper()
    dm.check_exist(tmp)
    dm.check_df_update(tmp)
    stock = tmp


def change_corr():
    global corr_list, update_toggle
    update_toggle = False
    tickers = search_corr.get()
    if tickers == "":
        return
    corr_list = []
    tickers = list(tickers.split(","))
    for ticker in tickers:
        corr_list.append(ticker.strip().upper())


def change_criteria(what):
    global basic_criteria, update_toggle
    update_toggle = False
    if what in basic_criteria:
        basic_criteria.remove(what)
    else:
        basic_criteria.append(what)


def change_period(what):
    global period, update_toggle
    update_toggle = False
    period = what


def change_mode(what):
    global mode, update_toggle
    update_toggle = False
    mode = what


def change_advance_type(what):
    global advance_type, update_toggle
    update_toggle = False
    advance_type = what


def change_mav(what):
    global mav_tuple, update_toggle
    update_toggle = False
    mav_tuple = list(mav_tuple)
    if what in mav_tuple:
        mav_tuple.remove(what)
        mav_tuple = tuple(mav_tuple)
    else:
        mav_tuple.append(what)
        mav_tuple = tuple(mav_tuple)


def setting_toggle(what):
    global update_toggle, display_volume, display_nontrading
    update_toggle = 0
    if what == "volume":
        display_volume = not display_volume
    elif what == "nontrading":
        display_nontrading = not display_nontrading


def change_ema():
    global update_toggle, max_emas, min_emas
    update_toggle = 0
    max_list = max_entry.get()
    max_list = list(max_list.split(","))
    max_emas = []
    for i in max_list:
        max_emas.append(i.strip())
    min_list = min_entry.get()
    min_list = list(min_list.split(","))
    min_emas = []
    for i in min_list:
        min_emas.append(i.strip())


def my_label(frame, text, font=None):
    if font is None:
        label = ttk.Label(frame, text=text, font=(TITLE_FONT, 17))
        label.pack(side=tk.LEFT)
    else:
        label = ttk.Label(frame, text=text, font=font)
        label.pack(side=tk.LEFT)
    return label


def my_basic_button(frame, text, callback, para):
    button = ttk.Button(frame, text=text, command=lambda: callback(para))
    button.pack(side=tk.LEFT)


def my_color_button(frame, text, callback, color, height, width,  para=None):
    if para is None:
        button = tk.Button(frame, text=text, command=lambda: callback(), fg=color, height=height, width=width)
        button.pack(side=tk.LEFT)
    else:
        button = tk.Button(frame, text=text, command=lambda: callback(para), fg=color, height=height, width=width)
        button.pack(side=tk.LEFT)


def my_checkbox(frame, text, selected, callback, para, var):
    checkbox = tk.Checkbutton(frame, text=text, variable=var, command=lambda: callback(para))
    if selected:
        checkbox.select()
    else:
        checkbox.deselect()
    checkbox.pack(side=tk.LEFT)


class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # *args store non-keyworded arguments, **kwargs store keyworded arguments
        tk.Tk.wm_title(self, "CSCI4140 Group8")  # Define application title
        tk.Tk.wm_geometry(self, '1600x1000')  # define window size

        # nav bar group
        top_frame = tk.Frame(self)
        top_frame.pack()
        my_color_button(top_frame, "Basic", self.change_page, "orange", 4, 20, "basic")
        my_color_button(top_frame, "Advance", self.change_page, "green", 4, 20, "advance")
        my_color_button(top_frame, "Heatmap (Correlation)", self.change_page, "blue", 4, 20, "heatmap")
        my_color_button(top_frame, "Backtest", self.change_page, "purple", 4, 20, "backtest")

        # search bar group
        search_frame = tk.Frame(self)
        search_frame.pack()
        global search_entry
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT)
        my_color_button(search_frame, "Set Stock", change_stock, "red", 2, 10)

        # main group, showing pages
        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # it is a empty dictionary at first, used to store page
        global advance_instance, heatmap_instance, backtest_instance, basic_instance
        for F in (BasicPage, Heatmap, Advance, StartPage, Backtest): # order can not be changed
            frame = F(container, self)
            if F == Advance:
                advance_instance = frame
            elif F == Heatmap:
                heatmap_instance = frame
            elif F == Backtest:
                backtest_instance = frame
            elif F == BasicPage:
                basic_instance = frame

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def change_page(self, what):
        change_mode(what)
        if what == "advance":
            self.show_frame(Advance)
        elif what == "heatmap":
            self.show_frame(Heatmap)
        elif what == "backtest":
            self.show_frame(Backtest)
        elif what == "basic":
            self.show_frame(BasicPage)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Home Page", font=TITLE_FONT)
        label.pack(pady=20, padx=10)

        button2 = ttk.Button(self, text="Quit", command=quit)
        button2.pack()

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class Backtest(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Backtesting", font=TITLE_FONT)
        label.pack(pady=10, padx=10)
        global min_entry, max_entry
        min_frame = tk.Frame(self)
        min_frame.pack()
        my_label(min_frame, "Lower bound exponential moving average (default 3,5,8,10,12,15): ", ("Verdana", 20))
        min_entry = tk.Entry(min_frame)
        min_entry.pack(side=tk.LEFT)
        max_frame = tk.Frame(self)
        max_frame.pack()
        my_label(max_frame, "Upper bound exponential moving average (default 30, 35,40,45,50,60): ", ("Verdana", 20))
        max_entry = tk.Entry(max_frame)
        max_entry.pack(side=tk.LEFT)
        submit_button = ttk.Button(self, text="Submit", command=lambda: change_ema())
        submit_button.pack()

        global ress1, ress2, ress3, ress4, ress5, ress6, ress7, ress8, ress9
        res1_frame = tk.Frame(self)
        res1_frame.pack()
        my_label(res1_frame, "Number of trade: ", ("Verdana", 20))
        self.res1 = ttk.Label(res1_frame, text=ress1, font=("Verdana", 20))
        self.res1.pack(side=tk.LEFT)

        res2_frame = tk.Frame(self)
        res2_frame.pack()
        my_label(res2_frame, "EMAs used: ", ("Verdana", 20))
        self.res2 = ttk.Label(res2_frame, text=ress2, font=("Verdana", 20))
        self.res2.pack(side=tk.LEFT)

        res3_frame = tk.Frame(self)
        res3_frame.pack()
        my_label(res3_frame, "Batting Avg: ", ("Verdana", 20))
        self.res3 = ttk.Label(res3_frame, text=ress3, font=("Verdana", 20))
        self.res3.pack(side=tk.LEFT)

        res4_frame = tk.Frame(self)
        res4_frame.pack()
        my_label(res4_frame, "Gain/loss ratio: ", ("Verdana", 20))
        self.res4 = ttk.Label(res4_frame, text=ress4, font=("Verdana", 20))
        self.res4.pack(side=tk.LEFT)

        res5_frame = tk.Frame(self)
        res5_frame.pack()
        my_label(res5_frame, "Average Gain: ", ("Verdana", 20))
        self.res5 = ttk.Label(res5_frame, text=ress5, font=("Verdana", 20))
        self.res5.pack(side=tk.LEFT)

        res6_frame = tk.Frame(self)
        res6_frame.pack()
        my_label(res6_frame, "Average Loss: ", ("Verdana", 20))
        self.res6 = ttk.Label(res6_frame, text=ress6, font=("Verdana", 20))
        self.res6.pack(side=tk.LEFT)

        res7_frame = tk.Frame(self)
        res7_frame.pack()
        my_label(res7_frame, "Max Return: ", ("Verdana", 20))
        self.res7 = ttk.Label(res7_frame, text=ress7, font=("Verdana", 20))
        self.res7.pack(side=tk.LEFT)

        res8_frame = tk.Frame(self)
        res8_frame.pack()
        my_label(res8_frame, "Max Loss: ", ("Verdana", 20))
        self.res8 = ttk.Label(res8_frame, text=ress8, font=("Verdana", 20))
        self.res8.pack(side=tk.LEFT)

        res9_frame = tk.Frame(self)
        res9_frame.pack()
        my_label(res9_frame, "Total return over: ", ("Verdana", 20))
        self.res9 = ttk.Label(res9_frame, text=ress9, font=("Verdana", 20))
        self.res9.pack(side=tk.LEFT)

    def update_label(self):
        global max_emas, min_emas, stock
        res = bt.backtesting(stock, max_emas, min_emas)
        self.res1.config(text=res[0])
        self.res2.config(text=[res[1]])
        self.res3.config(text=res[2])
        self.res4.config(text=res[3])
        self.res5.config(text=res[4])
        self.res6.config(text=res[5])
        self.res7.config(text=res[6])
        self.res8.config(text=res[7])
        self.res9.config(text=str(res[8])+"%")
        print(res)


class Heatmap(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Heatmap", font=TITLE_FONT)
        label.pack(pady=10, padx=10)

        global search_corr
        search_frame = tk.Frame(self)
        search_frame.pack()
        my_label(search_frame, "Search correlation of stocks (e.g. 'aapl, amzn'): ")
        search_corr = tk.Entry(search_frame)
        search_corr.pack(side=tk.LEFT)
        my_color_button(search_frame, "Set tickers", change_corr, "red", 2, 10)

        self.canvas = FigureCanvasTkAgg(fig, self)

    def update_fig(self):
        global corr_list
        self.canvas.get_tk_widget().destroy()
        myfig = dp.gen_heatmap(corr_list)
        self.canvas = FigureCanvasTkAgg(myfig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class BasicPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="BasicPage", font=TITLE_FONT)
        label.pack(pady=10, padx=10)

        checkbox_frame = tk.Frame(self)
        checkbox_frame.pack()
        my_label(checkbox_frame, "Criteria: ")
        self.var1 = tk.IntVar(value=0)
        self.var2 = tk.IntVar(value=0)
        self.var3 = tk.IntVar(value=0)
        self.var4 = tk.IntVar(value=0)
        my_checkbox(checkbox_frame, "High", True, change_criteria, "High", self.var1)
        my_checkbox(checkbox_frame, "Low", True, change_criteria, "Low", self.var2)
        my_checkbox(checkbox_frame, "Open", False, change_criteria, "Open", self.var3)
        my_checkbox(checkbox_frame, "Close", False, change_criteria, "Close", self.var4)

        # define period
        period_frame = tk.Frame(self)
        period_frame.pack()
        my_label(period_frame, "Period: ")
        my_basic_button(period_frame, "1 Week", change_period, 7)
        my_basic_button(period_frame, "1 Month", change_period, 30)
        my_basic_button(period_frame, "3 Months", change_period, 90)
        my_basic_button(period_frame, "6 Months", change_period, 180)
        my_basic_button(period_frame, "1 Year", change_period, 365)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_fig(self):
        global basic_criteria, stock, period
        self.canvas.get_tk_widget().destroy()
        myfig = dp.basic(stock, basic_criteria, period)
        self.canvas = FigureCanvasTkAgg(myfig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class Advance(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Advance analysis", font=TITLE_FONT)
        label.pack(pady=10, padx=10)

        type_frame = tk.Frame(self)
        type_frame.pack()
        my_label(type_frame, "Graph type: ")
        my_basic_button(type_frame, "OHLC", change_advance_type, "ohlc")
        my_basic_button(type_frame, "candle", change_advance_type, "candle")
        my_basic_button(type_frame, "renko", change_advance_type, "renko")
        my_basic_button(type_frame, "pnf", change_advance_type, "pnf")


        # define period
        period_frame = tk.Frame(self)
        period_frame.pack()
        my_label(period_frame, "Period: ")
        my_basic_button(period_frame, "1 Week", change_period, 7)
        my_basic_button(period_frame, "1 Month", change_period, 30)
        my_basic_button(period_frame, "3 Month", change_period, 90)
        my_basic_button(period_frame, "6 Month", change_period, 180)
        my_basic_button(period_frame, "1 Year", change_period, 365)

        # define simple moving average
        self.var1 = tk.IntVar(value=0)
        self.var2 = tk.IntVar(value=0)
        self.var3 = tk.IntVar(value=0)
        self.var4 = tk.IntVar(value=0)
        self.var5 = tk.IntVar(value=0)
        self.var6 = tk.IntVar(value=0)
        mav_frame = tk.Frame(self)
        mav_frame.pack()
        my_label(mav_frame, "Moving Average: ")
        my_checkbox(mav_frame, "5 days", False, change_mav, 5, self.var1)
        my_checkbox(mav_frame, "10 days", False, change_mav, 10, self.var2)
        my_checkbox(mav_frame, "20 days", False, change_mav, 20, self.var3)
        my_checkbox(mav_frame, "30 days", False, change_mav, 30, self.var4)
        my_checkbox(mav_frame, "40 days", False, change_mav, 40, self.var5)
        my_checkbox(mav_frame, "60 days", False, change_mav, 60, self.var6)

        # define volume display
        setting_frame = tk.Frame(self)
        setting_frame.pack()
        my_label(setting_frame, "Other settings")
        self.vol_var = tk.IntVar(value=0)
        self.trad_var = tk.IntVar(value=0)
        my_checkbox(setting_frame, "Display Volume", False, setting_toggle, "volume", self.vol_var)
        my_checkbox(setting_frame, "Display non-trading day", False, setting_toggle, "nontrading", self.trad_var)

        self.canvas = FigureCanvasTkAgg(fig, self)

    def update_fig(self):
        global stock, period, advance_type, display_volume, display_nontrading, mav_tuple
        self.canvas.get_tk_widget().destroy()  # destroy last graph
        myfig = dp.advance_graph(stock, advance_type, display_volume, display_nontrading, mav_tuple, period)
        self.canvas = FigureCanvasTkAgg(myfig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


if not os.path.exists('sp500tickers.pickle') and not os.path.exists('stock_dfs'):
    dm.retrieve_sp500_stocks(True)
elif not os.path.exists('sp500tickers.pickle'):
    dm.save_sp500_tickers()
elif not os.path.exists('stock_dfs'):
    dm.retrieve_sp500_stocks()

dm.check_df_update(stock)
app = GUI()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
