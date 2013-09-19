from control.profile.base.baseprofiler import baseprofiler
from test.__init__ import TEST_SOURCE_REAL_ROME as TEST
from output.__init__ import OUTPUT_DIR
from exception.exceptions import UnsupportedAlgorithmError
from control.shortestpath.dijkstra_sc import *
from control.shortestpath.dijkstra_mc import *
from control.plot.plotter_controller import make_plot, save_plot, make_table, save_table
from utils.math_utils import average
import os
from time import clock

#Parser Import
from control.parse.c_element_tree import cElementTreeParser as parser

DIJKSTRA_SC_0 = 0
DIJKSTRA_SC_1 = 1
DIJKSTRA_SC_2 = 2
DIJKSTRA_SC_3 = 3

DIJKSTRA_MC_0 = 4
DIJKSTRA_MC_1 = 5
DIJKSTRA_MC_2 = 6
DIJKSTRA_MC_3 = 7

ALGORITHMS = [#DIJKSTRA_SC_0, 
              DIJKSTRA_SC_1, 
              DIJKSTRA_SC_2]#, 
              #DIJKSTRA_SC_3],
              #DIJKSTRA_MC_0,
              #DIJKSTRA_MC_1,
              #DIJKSTRA_MC_2],
              #DIJKSTRA_MC_3]

ALGORITHMS_FUNCTION = {DIJKSTRA_SC_0: dijkstra_sc_0,
                        DIJKSTRA_SC_1: dijkstra_sc_1,
                        DIJKSTRA_SC_2: dijkstra_sc_2,
                        DIJKSTRA_SC_3: dijkstra_sc_3,
                        DIJKSTRA_MC_0: dijkstra_mc_0,
                        DIJKSTRA_MC_1: dijkstra_mc_1,
                        DIJKSTRA_MC_2: dijkstra_mc_2,
                        DIJKSTRA_MC_3: dijkstra_mc_3}

ALGORITHMS_NAME = {DIJKSTRA_SC_0: "SC0",
                    DIJKSTRA_SC_1: "SC1",
                    DIJKSTRA_SC_2: "SC2",
                    DIJKSTRA_SC_3: "SC3",
                    DIJKSTRA_MC_0: "MC0",
                    DIJKSTRA_MC_1: "MC1",
                    DIJKSTRA_MC_2: "MC2",
                    DIJKSTRA_MC_3: "MC3"}

PROFILE_TYPE_VAR_NUM_NODES = 0
PROFILE_TYPE_VAR_DISTANCE = 1
PROFILE_TYPES = [PROFILE_TYPE_VAR_NUM_NODES, 
                 PROFILE_TYPE_VAR_DISTANCE]
PROFILE_TYPES_NAME = {PROFILE_TYPE_VAR_NUM_NODES: "Var Num Nodes", 
                       PROFILE_TYPE_VAR_DISTANCE: "Var Distance"}

PARAMS = {"source": TEST,
          "algorithm": DIJKSTRA_SC_0, 
          "profile_type": PROFILE_TYPE_VAR_NUM_NODES,
          "values": [100, 200, 500],
          "const":  100,
          "average_bound": 5, 
          "output_dir": OUTPUT_DIR}

class ShortestPathProfiler(baseprofiler):
    
    def __init__(self):
        pass
        
    def profile(self, params = {}):
        """
        Profiles a single Algorithm, basing analysis upon the specified profiling parameters.
        
        profile(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """        
        params = dict(PARAMS.items() + params.items()) 
                 
        source = params["source"]  
        algorithm = params["algorithm"]
        profileType = params["profile_type"]
        values = params["values"]
        const = params["const"]
        averageBound = params["average_bound"]
        
        graph = parser().parse_file(source)
            
        try:
            algorithmFunction = ALGORITHMS_FUNCTION[algorithm]
        except KeyError:
            raise UnsupportedAlgorithmError()
        
        data = {"Algorithm": ALGORITHMS_NAME[algorithm], "Profile Type": profileType, "Max Input": sorted(values)[-1], "Const": const, "X": [], "Time": []}
        
        if profileType == PROFILE_TYPE_VAR_NUM_NODES:  
                  
            for value in values: 
                           
                rawData = []            
                for r in range(averageBound):
                    print "\tInput: ({}, {}) : Iteration {} . . .".format(str(value), str(const), str(r))
                    start = clock()
                    algorithmFunction(graph, value, const)
                    stop = clock()
                    elapsedTime = (stop - start)
                    rawData.append(elapsedTime)         
                       
                averageElapsedTime = average(rawData)            
                data["X"].append(value)
                data["Time"].append(averageElapsedTime)
                
        elif profileType == PROFILE_TYPE_VAR_DISTANCE:
            
            for value in values:            
                rawData = []   
                         
                for r in range(averageBound):
                    print "\tInput: ({}, {}) : Iteration {} . . .".format(str(value), str(const), str(r))
                    start = clock()
                    algorithmFunction(graph, const, value)
                    stop = clock()
                    elapsedTime = (stop - start)
                    rawData.append(elapsedTime)  
                              
                averageElapsedTime = average(rawData)            
                data["X"].append(value)
                data["Time"].append(averageElapsedTime) 
                           
        return [data]        
            
    def profileAll(self, params = {}):
        """
        Profiles all Algorithm, basing analysis upon the specified profiling parameters.
        
        profile_all(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """                      
        params = dict(PARAMS.items() + params.items())
        dataset = []
        for algorithm in ALGORITHMS:
            print "Profiling {} . . .".format(str(ALGORITHMS_NAME[algorithm]))
            params["algorithm"] = algorithm
            dataset.append(self.profile(params)[0])        
        return dataset
    
    def plotData(self, dataset, directory = os.path.join(os.getcwd(), PARAMS["output_dir"])):
        """
        Stores to the specified directory a MathPlotLib plot based on the specified dataset.
        
        plot_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be plotted.
        @type directory: string
        @param directory: directory to store the computed MatPlotLib plot.
        """                
        plotFileName = "{}  {}  {}-{}".format(" ".join([data["Algorithm"] for data in dataset]), str(PROFILE_TYPES_NAME[dataset[0]["Profile Type"]]), str(dataset[0]["Max Input"]), str(dataset[0]["Const"]))
        plotFilePath = os.path.join(directory, str(plotFileName))
        plotLabel = ", ".join([data["Algorithm"] for data in dataset])
        xLabel = "Nodes" if dataset[0]["Profile Type"] == PROFILE_TYPE_VAR_NUM_NODES else "Distance"
        yLabel = "Time (s)"
        legend = (data["Algorithm"] for data in dataset)
        formattedDataset = []        
        for data in dataset:
            formattedDataset.append([data["X"], data["Time"]])
        plot = make_plot(formattedDataset, plotLabel, xLabel, yLabel, legend)
        save_plot(plot, plotFilePath)
        plot.close()
        
    def tableData(self, dataset, directory = os.path.join(os.getcwd(), PARAMS["output_dir"])):
        """
        Stores to the specified directory a table-as-string based on the specified dataset.
        
        table_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be represented in table.
        @type directory: string
        @param directory: directory to store the computed table.
        """        
        tableFileName = "{}  {}  {}-{}.txt".format(" ".join([data["Algorithm"] for data in dataset]), str(PROFILE_TYPES_NAME[dataset[0]["Profile Type"]]), str(dataset[0]["Max Input"]), str(dataset[0]["Const"]))
        tableFilePath = os.path.join(directory, str(tableFileName))
        plotLabel = ", ".join([data["Algorithm"] for data in dataset])
        xLabel = "Nodes" if dataset[0]["Profile Type"] == PROFILE_TYPE_VAR_NUM_NODES else "Distance"
        yLabel = "Time (s)"
        legend = (data["Algorithm"] for data in dataset)
        formattedDataset = []
        for data in dataset:
            formattedDataset.append([data["X"], data["Time"]])
        table = make_table(formattedDataset, plotLabel, xLabel, yLabel, legend)
        save_table(table, tableFilePath)    

def __test(profiler, params):
    """
    SP-Solvers Algorithms Profiler Test.
    
    __test(profiler, params) -> None
    
    @type profiler: ShortestPathProfiler
    @param profiler: profiler instance.
    @type params: dictionary
    @param params: profiling parameters.
    """        
    print "### iPATH TEST PROFILER"
    print "### Data Type: Profiler ({})".format(str(profiler.__class__.__bases__[0].__name__))
    print "### Implementation {}".format(str(profiler.__class__.__name__))
    print "###"
    print "### Algorithms: {}".format(' '.join(ALGORITHMS_NAME[algorithm] for algorithm in ALGORITHMS))
    print "### Source: {}".format(str(params["source"]))
    print "### Profile Type: {}".format(str(PROFILE_TYPES_NAME[params["profile_type"]]))
    print "### Variables: {}".format(str(params["values"]))
    print "### Constant: {}".format(str(params["const"]))
    print "### Average Bound: {}".format(str(params["average_bound"]))  
    print "### Output Directory: {}\n".format(str(params["output_dir"]))
    print "Profiling . . ."
    data = profiler.profileAll(params)
    print "Making Plot . . ."
    profiler.plotData(data)
    print "Making Table . . .\n"
    profiler.tableData(data)
    
    print "\n### END OF TEST ###\n"

if __name__ == "__main__":
    profiler = ShortestPathProfiler()
    params = PARAMS
    __test(profiler, params)