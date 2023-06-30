import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import customtkinter
matplotlib.use('TkAgg')
import customtkinter
from ascii import ascii

 
class MountainGraphFrame(customtkinter.CTkFrame):
    """
    A custom frame class for displaying a 3D graph.

    This frame inherits from the customtkinter.CTkFrame class and provides
    functionality to display a 3D graph with updating data.

    Attributes:
        container_frame (customtkinter.CTkFrame): The container frame within the MountainGraphFrame.
        client: The client object used for data retrieval.
        x (numpy.ndarray): The range of values for the x-axis.
        y (numpy.ndarray): The range of values for the y-axis.
        Z (numpy.ndarray): The initial matrix for the 3D graph.
        X (numpy.ndarray): The meshgrid for the x-axis.
        Y (numpy.ndarray): The meshgrid for the y-axis.
        ax: The matplotlib Axes3D object for the graph.
        ani: The FuncAnimation object for the animation.

    Methods:
        show_graph(): Displays the 3D graph.
        update_graph(i): Updates the graph with new data.
    """

    def __init__(self, master, client):
        """
        Initialize the graph plotter.

        Args:
            master: The parent widget.
            client: The client object for data retrieval.
        """
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=2, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.client = client

        res = 20
        self.Z = np.zeros((res,res))
        
        # Create the range of values for the x and y axes
        self.x = np.linspace(-23000, 23000, res)
        self.y = np.linspace(-23000, 23000, res)

        # Create the initial meshgrid based on the values of x and y
        self.X, self.Y = np.meshgrid(self.x, self.y)


    def show_graph(self):
        """
        Shows the graph plot.
        """
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.plot_surface(self.X, self.Y, self.Z)
        
        self.ani = FuncAnimation(fig, self.update_graph, interval=1000, blit=False, repeat=False)

        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


    # Update function
    def update_graph(self, i):
        """
        Updates the graph plot.

        Args:
            i: The update iteration index.
        """
        # Get updated data from the client
        info = self.client.get_data()

        # Update the values of Z on the surface
        for team, climbers in info.items():
            for climber, data in climbers.items():
                x2 = data['x']
                y2 = data['y']
                z2 = data['z']

                # Check if the point already exists in the peak list

                # Calculate the distances between the points (x, y) and (x2, y2) -> EUCLIDEAN
                # Find the position of the nearest point
                idx_x = np.argmin(np.abs(self.x - x2))
                idx_y = np.argmin(np.abs(self.y - y2))

                # Assign the height value to the corresponding point in Z
                self.Z[idx_x, idx_y] = z2

        self.ax.clear()
        self.ax.plot_surface(self.X, self.Y, self.Z, cmap="terrain")


        


class HikersPositionFrame(customtkinter.CTkFrame): #GRAPH Hikers
    """
    A class representing the second frame of a customtkinter application.

    This frame displays a 3D graph and a scrollable team list. The graph is updated based on data received from a server.

    Attributes:
        master (tkinter.Tk): The master tkinter window.
        client (Client): The client object for communication with the server.
        container_frame (customtkinter.CTkFrame): The frame that contains the graph and team list.
        selected_team (str): The currently selected team.
        client (Client): The client object for communication with the server.
        team_colors (dict): A dictionary mapping team names to colors for graph visualization.
        ax (matplotlib.axes._subplots.Axes3DSubplot): The subplot for the 3D graph.
        points (matplotlib.collections.PathCollection): The scatter plot points on the graph.
        ani (matplotlib.animation.FuncAnimation): The animation object for updating the graph.

    Methods:
        __init__(self, master, client): Initializes the HikersPositionFrame instance.
        show_graf3D(self): Displays the 3D graph.
        update_graph(self, _): Updates the graph based on data received from the server.
        get_team_list_from_server(self): Retrieves the list of teams from the server.
        create_scrollable_frame(self): Creates and configures a scrollable frame for the team list.
        select_team(self, team): Updates the selected team and updates the graph accordingly.
    """
    def __init__(self, master,client,team_colors:dict):
        """
        Initializes the HikersPositionFrame instance.

        Args:
            master (tkinter.Tk): The master tkinter window.
            client (Client): The client object for communication with the server.
        """
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.selected_team = 'Everyone'
        self.client = client

        self.team_colors = team_colors

        
        self.create_scrollable_frame()

    def show_graf3D(self):
        """
        Displays the 3D graph.

        This method sets up the 3D graph, initializes the scatter plot, and starts the animation for updating the graph.

        """
        # Set up the figure and subplot for the 3D graph
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        # Set labels for the X, Y, and Z axes
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Set the limits for the X, Y
        self.ax.set_xlim3d(-23000, 20000)
        self.ax.set_ylim3d(-23000, 20000)

        # Determine the color for the scatter plot based on the selected team
        
        color = self.team_colors[self.selected_team]

        # Initialize the scatter plot points with empty data and specified color and marker
        self.points = self.ax.scatter([], [], [], c=color, marker='o')

        # Create an animation object for updating the graph using the update_graph method
        self.ani = FuncAnimation(fig, self.update_graph, interval=1000, blit=False, repeat=False)

        # Create a Tkinter canvas for the figure and display it in the container frame
        canvas = FigureCanvasTkAgg(fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew") # To obtain the underlying Tkinter widget associated with the canvas and then configure it.

        # Start the animation
        self.ani._start()

    def update_graph(self, _):
        """
        Update the graph based on the data received from the server.

        Args:
            frame: The frame to update the graph on.

        Returns:
            The updated points object.
        """
        # Get the data from the server
        self.info = self.client.get_data()  

        points = []
        colors = []
        for team, climbers in self.info.items():
            # To show all the points (teams/hikers) on the map
            if self.selected_team == 'Everyone':  
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    # Assign the colors for each team
                    color = self.team_colors.get(team)
                    colors.append(color)
                    points.append((x, y, z))

            # To show the selected team
            elif team == self.selected_team: 
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    z = data['z']
                    
                    # Get the color representing the team
                    color = self.team_colors.get(team)
                    colors.append(color)
                    points.append((x, y, z))


        #Display the points
        x, y, z = zip(*points) if points else ([], [], []) 
        self.points.set_3d_properties(z, zdir='z')
        self.points.set_offsets(np.column_stack((x, y)))
        self.points.set_color(colors)

        if points:
            max_z = max(z)
            #Redefine the limits for the z axis
            self.ax.set_zlim3d(0, max_z)


    def get_team_list_from_server(self):
        """
        Retrieves the list of teams from the server.

        Returns:
            A list of team names.
        """
        teams = []
        self.info = self.client.get_data()
        #Get the teams from the server
        for team, climbers in self.info.items(): 
            teams.append(team)
        return teams



    def create_scrollable_frame(self):
        """
        Create and configure a scrollable frame to display the team list.

        """
        scrollable_frame = ScrollableLabelButtonFrame(self.container_frame)
        scrollable_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

        teams = self.get_team_list_from_server()
        # Select the team to display its hikers
        scrollable_frame.add_item("Everyone", command=self.select_team) 

        #Add the option to see each team that is registered on the server
        for team in teams:
            scrollable_frame.add_item(team, command=self.select_team)

        scrollable_frame.configure(width=150, height=100)


    def select_team(self, team):
        """
        Update the selected team and update the graph accordingly.

        Args:
            team: The selected team.

        """
        self.selected_team = team
        self.update_graph(None)



class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    """
    A custom frame class that displays a scrollable list of labels and buttons.

    This frame inherits from the customtkinter.CTkScrollableFrame class and provides
    functionality to add labels and buttons dynamically.

    Attributes:
        command: Optional command function to be executed by the buttons.
        label_list: A list containing the label instances added to the frame.
        button_list: A list containing the button instances added to the frame.

    Methods:
        add_item(item, image=None, command=None): Adds a label and button to the frame.
    """
    def __init__(self, master, command=None, **kwargs):
        """
        Initialize the ScrollableLabelButtonFrame.

        Args:
            master: The master widget.
            command: Optional command function to be executed by the buttons.
            **kwargs: Additional keyword arguments to be passed to the parent class.

        """
        # Call the __init__ method of the parent class (customtkinter.CTkScrollableFrame)
        super().__init__(master, **kwargs)
        # Configure the first column of the grid to expand and fill any remaining space
        self.grid_columnconfigure(0, weight=1) #weight means the priority of the column if the space given has to be distributed among other columns.

        # Set the 'command' attribute of the instance to the provided 'command' argument
        self.command = command
        
        # Create an empty list to store label instances
        self.label_list = []
        # Create an empty list to store button instances
        self.button_list = []

    def add_item(self, item, image=None, command=None):
        """
        Add a label and button to the frame.

        Args:
            item: The text to display in the label.
            image: Optional image to display alongside the text.
            command: Optional command function to be executed by the button.

        """
        # Create a label instance with the provided 'item' as the text and optional 'image'
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        # Create a button instance with the text "Show" and specified width and height
        button = customtkinter.CTkButton(self, text="Show", width=30, height=24)
        # If a 'command' argument is provided, configure the button's command to execute it with 'item' as an argument
        if command is not None:
            button.configure(command=lambda: command(item))
        # Add the label to the grid at a new row based on the current length of 'label_list' and in the first column
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        # Add the button to the grid at a new row based on the current length of 'button_list' and in the second column
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        # Append the label to the 'label_list'
        self.label_list.append(label)
        # Append the button to the 'button_list'
        self.button_list.append(button)

   

class ASCIIFrame(customtkinter.CTkFrame):
    def __init__(self, master,client):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.state = False

        self.client = client
        info = self.client.get_data()
        num_jugador = 65
        self.letter_asig = {}
        counter = 0
        while self.client.is_registering_teams() or (counter == 0):
            for equipo, escaladores in info.items():
                self.letter_asig[equipo] = num_jugador
                num_jugador += 1
            counter += 1
        label_resultado = customtkinter.CTkLabel(self, text=ascii(self.letter_asig), font=('Courier New', 10))
        label_resultado.pack()
        self.call_function()
        
    def change(self):
        self.state = True
        self.call_function()

    def call_function(self):
        for widgets in self.winfo_children():
            widgets.destroy()
        label_resultado = customtkinter.CTkLabel(self, text=ascii(self.letter_asig), font=('Courier New', 10))
        label_resultado.pack()
        self.after(2000,self.call_function)


class HeatmapFrame(customtkinter.CTkFrame):
    """
    A custom frame class for displaying an animation.

    This frame displays an animation that visualizes data using a heatmap.
    It inherits from the customtkinter.CTkFrame class.

    Attributes:
        container_frame (customtkinter.CTkFrame): The container frame within the FourthFrame.
        client: The client object used for data retrieval.
        x (numpy.ndarray): The range of values for the x-axis.
        y (numpy.ndarray): The range of values for the y-axis.
        fig: The matplotlib Figure object for the animation.
        ax: The matplotlib Axes object for the animation.
        hist (numpy.ndarray): The histogram matrix used for the heatmap.
        heatmap: The matplotlib Image object representing the heatmap.
        animation: The FuncAnimation object for the animation.
        canvas: The FigureCanvasTkAgg object for displaying the animation on a tkinter window.
        colorbar: The colorbar object for the heatmap.

    Methods:
        show_animation(): Displays the animation.
        update_heatmap(_: Any): Updates the heatmap based on new data.
    """
    def __init__(self, master, client):
        """
        Initialize the FourthFrame.

        Args:
            master (Tk): The master tkinter window.
            client: The client object for data retrieval.
        """
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        self.client = client
       

        res = 100

       
        # Create the range of values for the x and y axes
        self.x = np.linspace(-23000, 23000, res)
        self.y = np.linspace(-23000, 23000, res)


    def show_animation(self):
        """Shows the animation."""
        self.fig, self.ax = plt.subplots()

        # Set x and y labels    
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Set the x and y limits
        self.ax.set_xlim(-25000, 25000)
        self.ax.set_ylim(-25000, 25000)

        self.hist = np.zeros((len(self.x), len(self.y)))
        self.heatmap = self.ax.imshow(self.hist, cmap='viridis', origin='lower', extent=[-23000, 23000, -23000, 23000])

        self.animation = FuncAnimation(self.fig, self.update_heatmap, interval=1000)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.colorbar = self.fig.colorbar(self.heatmap, ax=self.ax)

        self.animation._start()

    def update_heatmap(self, _):
        """
        Update the heatmap based on new data.

        Args:
            _: Unused argument required by FuncAnimation.

        Returns:
            The updated heatmap.
        """
        self.ax.clear()
        self.hist.fill(0)  # Reset the histogram matrix on each update

        self.info = self.client.get_data()

        for team, climbers in self.info.items():
            for climber, data in climbers.items():
                x2 = data['x']
                y2 = data['y']

                idx_x = np.argmin(np.abs(self.x - x2))
                idx_y = np.argmin(np.abs(self.y - y2))

                # Assign the height value to the corresponding point in Z
                self.hist[idx_x, idx_y] += 1  # Increment the value by 1 instead of directly assigning

        

        # Create a colormap with higher intensity for more players and lower intensity for fewer players
        cmap = plt.cm.get_cmap('viridis')

        self.heatmap = self.ax.imshow(self.hist, cmap=cmap, origin='lower', extent=[-23000, 23000, -23000, 23000])

        



class ScatterFrame(customtkinter.CTkFrame):
    """
    A class representing the scatter frame of a customtkinter application.

    This frame displays a 2D graph and a scrollable team list. The graph is updated based on data received from a server.

    Attributes:
        master (tkinter.Tk): The master tkinter window.
        client (Client): The client object for communication with the server.
        container_frame (customtkinter.CTkFrame): The frame that contains the graph and team list.
        selected_team (str): The currently selected team.
        client (Client): The client object for communication with the server.
        team_colors (dict): A dictionary mapping team names to colors for graph visualization.
        ax (matplotlib.axes._subplots.Axes3DSubplot): The subplot for the 3D graph.
        points (matplotlib.collections.PathCollection): The scatter plot points on the graph.
        ani (matplotlib.animation.FuncAnimation): The animation object for updating the graph.

    Methods:
        __init__(self, master, client): Initializes the ScatterFrame instance.
        show_scatter(self): Displays the 2D graph.
        update_scatter(self, _): Updates the graph based on data received from the server.
        get_team_list_from_server(self): Retrieves the list of teams from the server.
        create_scrollable_frame(self): Creates and configures a scrollable frame for the team list.
        select_team(self, team): Updates the selected team and updates the graph accordingly.
    """
    def __init__(self, master,client,team_colors:dict):
        """
        Initialize the object.

        Args:
            master: The master widget.
            client: The client object.
            team_colors: A dictionary containing team colors.
        """
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)

        # Create container frame with grid layout
        self.container_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

        self.selected_team = 'Everyone'
        self.team_colors = team_colors

        # Create container frame with grid layout
        self.client = client
        self.info = self.client.get_data()

        
        self.create_scrollable_frame()

        

    def show_scatter(self):
        """
        Shows the scatter plot.
        """
        # Create a scatter plot
        self.fig, self.ax = plt.subplots()

        # Set x and y labels
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Set the x and y limits
        self.ax.set_xlim(-23000, 23000)
        self.ax.set_ylim(-23000, 23000)

        # Get the color for the selected team
        color = self.team_colors[self.selected_team]

        # Create an empty scatter plot
        self.points = self.ax.scatter([], [], c=color, marker='o')


        # Create the animation
        self.animation = FuncAnimation(self.fig, self.update_scatter, interval=1000, blit=False, repeat=False)


        # Create the Tkinter canvas for the plot    
        canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Start the animation
        self.animation._start()

    def update_scatter(self, _):
        """
        Update the scatter plot based on the data received from the server.

        Args:
            frame: The frame to update the scatter plot on.

        Returns:
            The updated points object.

        """
        self.info = self.client.get_data()  # Get the data from the server

        points = []
        colors = []
        for team, climbers in self.info.items():

            if self.selected_team == 'Everyone':
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                    
                    color = self.team_colors.get(team)
                    self.team_colors[team] = color
                    colors.append(color)

                    points.append((x, y))
            elif team == self.selected_team:
                for climber, data in climbers.items():
                    x = data['x']
                    y = data['y']
                   
                    color = self.team_colors.get(team)
                    colors.append(color)
                    points.append((x, y))

        x, y = zip(*points) if points else ([], [])
        self.points.set_offsets(np.column_stack((x, y)))
        self.points.set_color(colors)



    def show_animation(self):
        """
        Shows the animation.
        """
        self.animation = FuncAnimation(self.fig, self.update_scatter, interval=1000)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.container_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def get_team_list_from_server(self):
        """
        Retrieves the list of teams from the server.

        Returns:
            list: A list containing the names of the teams on the server.
        """
        teams = []
        for team, climbers in self.info.items():
            teams.append(team)
        return teams



    def create_scrollable_frame(self):
        """
        Create and configure a scrollable frame to display the team list.

        """
        scrollable_frame = ScrollableLabelButtonFrame(self.container_frame)
        scrollable_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

        teams = self.get_team_list_from_server()
        scrollable_frame.add_item("Everyone", command=self.select_team)

        for team in teams:
            scrollable_frame.add_item(team, command=self.select_team)

        scrollable_frame.configure(width=150, height=100)


    def select_team(self, team):
        """
        Update the selected team and update the graph accordingly.

        Args:
            team: The selected team.

        """
        self.selected_team = team
        


