from control.profile.base.baseprofiler import baseprofiler
from output.__init__ import OUTPUT_DIR
from exception.exceptions import UnsupportedParserError
from control.parse.c_element_tree import cElementTreeParser as cElementTree
from control.parse.element_tree import ElementTreeParser as ElementTree
from control.parse.sax import SaxParser as Sax
from control.profile.generator.osm_generator import OsmGenerator
from control.plot.plotter_controller import make_plot, save_plot, make_table, save_table
from utils.math_utils import average
import os
from time import clock

C_ELEMENT_TREE = 0
ELEMENT_TREE = 1
SAX = 2
PARSERS = [C_ELEMENT_TREE, ELEMENT_TREE, SAX]
PARSERS_INSTANCE = {C_ELEMENT_TREE: cElementTree, ELEMENT_TREE: ElementTree, SAX: Sax}
PARSERS_NAME = {C_ELEMENT_TREE: "cElementTree", ELEMENT_TREE: "ElementTree", SAX: "Sax"}

PARAMS = {"parser": C_ELEMENT_TREE, 
          "max_input": 20000, 
          "adjacency": 10, 
          "average_bound": 50, 
          "output_dir": OUTPUT_DIR}

class ParserProfiler(baseprofiler):    
    
    def __init__(self):        
        self._random_generator = OsmGenerator()
        
    def profile(self, params = {}):  
        """
        Profiles a single Parser, basing analysis upon the specified profiling parameters.
        
        profile(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """        
        params = dict(PARAMS.items() + params.items())
                
        parser = params["parser"]
        max_input = params["max_input"]
        adjacency = params["adjacency"]
        average_bound = params["average_bound"]
 
        try:
            parser_instance = PARSERS_INSTANCE[parser]()
        except KeyError:
            raise UnsupportedParserError()
           
        data = {"Parser": PARSERS_NAME[parser], "Max Input": max_input, "X": [], "Time": []}        
        
        interval = max_input / 10
        
        for X in range(0, max_input + 1, interval):
            self._random_generator.num_nodes = X
            self._random_generator.num_ways = X
            self._random_generator.adjacency = adjacency
            osm = self._random_generator.generate()
            
            raw_data = []
            
            for r in range(average_bound):
                start = clock()
                parser_instance.parse_string(osm)
                stop = clock()
                elapsed = (stop - start)
                raw_data.append(elapsed)
            
            averageElapsedTime = average(raw_data)
            
            data["X"].append(X)
            data["Time"].append(averageElapsedTime)
            
        return [data]        
            
    def profile_all(self, params = {}):
        """
        Profiles all Parsers, basing analysis upon the specified profiling parameters.
        
        profile_all(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """        
        params = dict(PARAMS.items() + params.items())
        dataset = []
        for parser in PARSERS:
            print "\t{} . . .".format(str(PARSERS_NAME[parser]))
            params["parser"] = parser
            dataset.append(self.profile(params)[0])
        return dataset
    
    def plot_data(self, dataset, directory = PARAMS["output_dir"]):
        """
        Stores to the specified directory a MathPlotLib plot based on the specified dataset.
        
        plot_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be plotted.
        @type directory: string
        @param directory: directory to store the computed MatPlotLib plot.
        """        
        max_input = dataset[0]["Max Input"]
        file_name = " ".join([data["Parser"] for data in dataset]) + " " + str(max_input)
        file_path = os.path.join(directory, str(file_name))
        plot_label = ", ".join([data["Parser"] for data in dataset])
        xlabel = "Input"
        ylabel = "Time (s)"  
        legend = (data["Parser"] for data in dataset) 
        formatted_dataset = []
        for data in dataset:
            formatted_dataset.append([data["X"], data["Time"]])
        plot = make_plot(formatted_dataset, plot_label, xlabel, ylabel, legend)
        save_plot(plot, file_path)
        plot.close()
        
    def table_data(self, dataset, directory = PARAMS["output_dir"]):
        """
        Stores to the specified directory a table-as-string based on the specified dataset.
        
        table_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be represented in table.
        @type directory: string
        @param directory: directory to store the computed table.
        """        
        max_input = dataset[0]["Max Input"]
        file_name = " ".join([data["Parser"] for data in dataset]) + " " + str(max_input) + ".txt"
        file_path = os.path.join(directory, str(file_name))
        plot_label = ", ".join([data["Parser"] for data in dataset])
        xlabel = "Dataset"
        ylabel = "Time (s)"
        legend = (data["Parser"] for data in dataset) 
        formatted_dataset = []
        for data in dataset:
            formatted_dataset.append([data["X"], data["Time"]])
        table = make_table(formatted_dataset, plot_label, xlabel, ylabel, legend)
        save_table(table, file_path)    

def __test(profiler, params):
    """
    Parser Profiler Test.
    
    __test(profiler, params) -> None
    
    @type profiler: ParserProfiler
    @param profiler: profiler instance.
    @type params: dictionary
    @param params: profiling parameters.
    """    
    if not isinstance(profiler, baseprofiler):
        raise TypeError("Expected type was Profiler.") 
    
    print "### iPATH TEST PROFILER"
    print "### Data Type: Profiler ({})".format(str(profiler.__class__.__bases__[0].__name__))
    print "### Implementation: {}".format(str(profiler.__class__.__name__))
    print "###"       
    print "### Parsers: {}".format(' '.join(PARSERS_NAME[parser] for parser in PARSERS))
    print "### Max Input: {}".format(str(params["max_input"]))
    print "### Adjacency: {}".format(str(params["adjacency"]))
    print "### Average Bound: {}".format(str(params["average_bound"]))
    print "### Output Directory: {}\n".format(str(params["output_dir"]))
    print "Profiling . . ."
    data = profiler.profile_all(params)
    print "Making Plot . . ."
    profiler.plot_data(data)
    print "Making Table . . .\n"
    profiler.table_data(data)
    
    print "\n### END OF TEST ###\n"

if __name__ == "__main__":
    profiler = ParserProfiler()
    params = PARAMS
    __test(profiler, params)