class DataAnalyst:
    """
    Calss to analize data on all hykers on map
    """
    def __init__(self, name:str = 'dataAnalyst'):
        self.name = name
        self.data = {}
        self.all_h_pos = []
        self.someone_won = False
        self.info = {}

    def update_data(self, data):
        """
        Updates data of DataAnalyst with data of hikers on all the map
        Parameters
        ----------
        data : function
            function that returns new data
        """
        self.data = data
    
    def check_win(self)-> tuple[bool,tuple[float,float,float]]:
        """
        Checks if a team won the game

        Returns
        -------
        tuple
            tuple with:
            0: True if a team won / False is not
            1: if a team won tuple with xyz coords of wining point / None if no team won
        """
        for team in self.data:
            for player in self.data[team]:
                if self.data[team][player]['cima'] == True:
                    self.someone_won = True
                    return True, self.get_max()
        return False, None
    
    def get_all_pos(self):
        """
        Stores the positions of all hikers in a list of tuples with x, y, and z coordinates.
        
        Returns:
            None
        """
        for team in self.data:
            for player in self.data[team]:
                self.all_h_pos.append((self.data[team][player]['x'], self.data[team][player]['y'], self.data[team][player]['z']))

    def get_max(self) -> tuple[float, float, float]:
        """
        Returns the maximum z position found by any hiker as a tuple of (x, y, zMAX).
        
        Returns:
            tuple[float, float, float]: The maximum z position.
        """
        self.get_all_pos()
        self.all_h_pos = sorted(self.all_h_pos, key=lambda z: z[2])
        max_xyz = self.all_h_pos.pop()
        
        # Reduce the list of all positions to only keep the top n maximum positions.
        n = 5
        self.all_h_pos = self.all_h_pos[-n:]

        return max_xyz

    
    def get_all_info(self)-> dict[bool,tuple,list]:
        """
        Using data on DataAnalyst attributes returns a dictionary with useful info
        
        Returns
        -------
        dict
        """
        self.info = {'win': self.check_win(), 'max_pos': self.get_max(), 'n_max_pos': self.all_h_pos}
        return self.info

