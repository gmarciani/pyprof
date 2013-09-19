class baseprofiler:
    """
    Profiler interface.
    """
    
    def profile(self, params = {}):
        """
        Profiles a single Algorithm/Data-Structure, basing analysis upon the specified profiling parameters.
        
        profile(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """        
        raise NotImplementedError("profile: You should have implemented this method!")
    
    def profile_all(self, params = {}):
        """
        Profiles all Algorithm/Data-Structure, basing analysis upon the specified profiling parameters.
        
        profile_all(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """        
        raise NotImplementedError("profile_all: You should have implemented this method!")
    
    def plot_data(self, dataset, directory):
        """
        Stores to the specified directory a MathPlotLib plot based on the specified dataset.
        
        plot_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be plotted.
        @type directory: string
        @param directory: directory to store the computed MatPlotLib plot.
        """
        
        raise NotImplementedError("plot_data: You should have implemented this method!")
    
    def table_data(self, dataset, directory):
        """
        Stores to the specified directory a table-as-string based on the specified dataset.
        
        table_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be represented in table.
        @type directory: string
        @param directory: directory to store the computed table.
        """        
        raise NotImplementedError("table_data: You should have implemented this method!")