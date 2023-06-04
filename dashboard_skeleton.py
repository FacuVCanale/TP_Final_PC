import time
import threading
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3

from communication.client.client import MountainClient


class Dashboard:
    def __init__(self, client: MountainClient):
        self.root = Tk()
        self.root.title("Dashboard")
        self.client = client
        self.data = client.get_data()
        self.time_step = 500 # ms
        self.animations = [] # for animations to stay alive in memory
        self.figsize = (4.5, 3)

        # self.visualization_example(...)


    def visualization_example(self, frame):
	    # Code for visualization plot
        fig, ax = plt.subplots()
        # code for plot

        def animate(i):
            # code for animation
            pass


        self.animations.append(FuncAnimation(fig, func=animate, interval=self.time_step, blit=True))
        
        canvas = FigureCanvasTkAgg(fig, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack()

    def start(self):
        # No modificar
        t = threading.Thread(target=self.update_data)
        t.start()
        self.root.mainloop()  

    def update_data(self):
        # No modificar
        while not self.client.is_over():
            self.data = self.client.get_data()
            time.sleep(self.time_step/1000)

    def stop(self):
        # No modificar
        self.root.quit()

if __name__ == "__main__":
    # No modificar
    client = MountainClient('localhost', 8080)
    d = Dashboard(client)
    d.start()
