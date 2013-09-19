from control.profile.base.baseprofiler import baseprofiler
from output.__init__ import OUTPUT_DIR
from exception.exceptions import UnsupportedDataStructureError
from model.base.baselinkedlist import baselinkedlist
from model.base.basequeue import basequeue
from model.base.basestack import basestack
from model.base.basetree import basetree
from model.base.basepriorityqueue import basepriorityqueue
from model.base.basegraph import basegraph
from model.linkedlist import SimpleLinkedList, DoubleLinkedList
from model.queue import QueueLinkedList, QueueDeque
from model.stack import StackLinkedList, StackArrayList, StackDeque
from model.tree import RelationTree, DictTree, TreeArrayList
from model.graph import GraphIncidenceList, GraphIncidenceSet
from model.priority_queue import DHeap
from utils.math_utils import average
from control.plot.plotter_controller import make_plot, save_plot, make_table, save_table
import os, random
from time import clock as time

LINKED_LIST = 0
QUEUE = 1
STACK = 2
TREE = 3
PRIORITY_QUEUE = 4
GRAPH = 5
STRUCTURES = [LINKED_LIST, QUEUE, STACK, TREE, PRIORITY_QUEUE, GRAPH]

STRUCTURES_NAME = {LINKED_LIST: "LinkedList",
                                  QUEUE: "Queue",
                                  STACK: "Stack",
                                  TREE: "Tree",
                                  PRIORITY_QUEUE: "PriorityQueue",
                                  GRAPH: "Graph"}

STRUCTURES_INSTANCE = {LINKED_LIST: {"Implementations": {"SimpleLinkedList": SimpleLinkedList, 
                                                           "DoubleLinkedList": DoubleLinkedList},
                                       "Operations": {"add_as_first": baselinkedlist.add_as_first,
                                                      "add_as_last": baselinkedlist.add_as_last,
                                                      "pop_first": baselinkedlist.pop_first,
                                                      "pop_last": baselinkedlist.pop_last,
                                                      "delete_record": baselinkedlist.delete_record}}, 
                        QUEUE: {"Implementations": {"QueueLinkedList": QueueLinkedList, 
                                                      "QueueDeque": QueueDeque}, 
                                  "Operations": {"enqueue": basequeue.enqueue,
                                                 "get_first": basequeue.get_first,
                                                 "dequeue": basequeue.dequeue}},
                        STACK: {"Implementations": {"StackLinkedList": StackLinkedList, 
                                                      "StackArrayList": StackArrayList, 
                                                      "StackDeque": StackDeque}, 
                                  "Operations": {"push": basestack.push,
                                                 "top": basestack.top,
                                                 "pop": basestack.pop}},
                        TREE: {"Implementations": {"RelationTree": RelationTree,
                                                   "DictTree": DictTree,
                                                   "TreeArrayList": TreeArrayList},
                                 "Operations": {"insert": basetree.insert,
                                                "make_son": basetree.make_son,
                                                "get_path_to": basetree.get_path_to}},
                        PRIORITY_QUEUE: {"Implementations": {"2Heap": DHeap,
                                                              "4Heap": DHeap},
                                                              #"8Heap": DHeap},,
                                                              #"16Heap": DHeap,
                                                              #"32Heap": DHeap,
                                                              #"64Heap": DHeap},
                                          "Operations": {"insert": basepriorityqueue.insert,
                                                         "delete_min": basepriorityqueue.delete_min,
                                                         "decrease_key": basepriorityqueue.decrease_key}},
                        GRAPH: {"Implementations": {"IncidenceList": GraphIncidenceList,
                                                    "IncidenceSet": GraphIncidenceSet},
                                    "Operations": {"add_node": basegraph.add_node,
                                                   "add_arc": basegraph.add_arc,
                                                   "get_incident_arcs": basegraph.get_incident_arcs,
                                                   "set_arc_status": basegraph.set_arc_status}}}

PARAMS = {"structure": LINKED_LIST,
          "operation": "add_as_first",
          "max_input": 20000,
          "average_bound": 10,
          "output_dir": OUTPUT_DIR}

class StructProfiler(baseprofiler):    
    
    def __init__(self):
        pass
    
    def profile(self, params = {}):
        """
        Profiles a single Data-Structure, basing analysis upon the specified profiling parameters.
        
        profile(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """
        
        params = dict(PARAMS.items() + params.items())        
        structure = params["structure"]
        operation = params["operation"]
        max_input = params["max_input"]
        average_bound = params["average_bound"]
        
        if structure not in STRUCTURES_INSTANCE or operation not in STRUCTURES_INSTANCE[structure]["Operations"]:
            raise UnsupportedDataStructureError()   
           
        if structure is LINKED_LIST:
            dataset = self._profile_linked_list(operation, max_input, average_bound)
        elif structure is QUEUE:
            dataset = self._profile_queue(operation, max_input, average_bound)
        elif structure is STACK:
            dataset = self._profile_stack(operation, max_input, average_bound)
        elif structure is TREE:
            dataset = self._profile_tree(operation, max_input, average_bound)
        elif structure is PRIORITY_QUEUE:
            dataset = self._profile_priority_queue(operation, max_input, average_bound)
        elif structure is GRAPH:
            dataset = self._profile_graph(operation, max_input, average_bound)            
        return dataset
    
    def profile_all(self, params):
        """
        Profiles all Data-Structure's Operations, basing analysis upon the specified profiling parameters.
        
        profile_all(params = {}) -> data
        
        @type params: dictionary
        @param params: parameters for the analysis.
        
        @rtype: list of dictionaries
        @return: profiling results.
        """
        
        params = dict(PARAMS.items() + params.items())        
        dataset = []
        structure = params["structure"]
        for operation in STRUCTURES_INSTANCE[structure]["Operations"].iterkeys():
            params["operation"] = operation
            print "\tProfiling {} . . .".format(str(operation))
            data = self.profile(params)
            dataset.append(data)
        return dataset            
    
    def _profile_linked_list(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"].iterkeys():
            data = {"Structure": LINKED_LIST, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_linked_list(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)
        return dataset
    
    def _profile_queue(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[QUEUE]["Implementations"]:
            data = {"Structure": QUEUE, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_queue(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)
        return dataset
    
    def _profile_stack(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[STACK]["Implementations"]:
            data = {"Structure": STACK, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_stack(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)            
        return dataset
    
    def _profile_tree(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[TREE]["Implementations"]:
            data = {"Structure": TREE, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_tree(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)            
        return dataset
    
    def _profile_priority_queue(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"]:
            data = {"Structure": PRIORITY_QUEUE, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_priority_queue(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)
        return dataset
    
    def _profile_graph(self, operation, max_input, average_bound):
        dataset = []
        for implementation in STRUCTURES_INSTANCE[GRAPH]["Implementations"]:
            data = {"Structure": GRAPH, "Implementation": implementation, "Operation": str(operation), "Max Input": max_input, "X": [], "time": []}
            interval = max_input / 10
            for x in range(0, max_input + 1, interval):
                averageTime = self._get_time_graph(implementation, operation, x, average_bound)
                data["X"].append(x)
                data["time"].append(averageTime)                
            dataset.append(data)            
        return dataset
    
    def _get_time_linked_list(self, implementation, operation, iteration, average_bound):
        rawTimes = []        
        if operation == "add_as_first":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"][implementation]()
                start = time()
                for j in range(iteration):
                    instance.add_as_first(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "add_as_last":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"][implementation]()
                start = time()
                for j in range(iteration):
                    instance.add_as_last(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "pop_first":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.add_as_first(r)
                start = time()
                for j in range(iteration):
                    instance.pop_first()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "pop_last":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.add_as_first(r)
                start = time()
                for j in range(iteration):
                    instance.pop_last()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "delete_record":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[LINKED_LIST]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.add_as_first(r)
                record = instance.get_first_record()
                start = time()
                for j in range(iteration):
                    instance.delete_record(record)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
                    
        averageTime = average(rawTimes)
        return averageTime
    
    def _get_time_queue(self, implementation, operation, iteration, average_bound):
        rawTimes = []
        if operation == "enqueue":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[QUEUE]["Implementations"][implementation]()
                start = time()
                for j in range(iteration):
                    instance.enqueue(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "get_first":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[QUEUE]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.enqueue(r)
                start = time()
                for j in range(iteration):
                    instance.get_first()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "dequeue":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[QUEUE]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.enqueue(r)
                start = time()
                for j in range(iteration):
                    instance.dequeue()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
                    
        averageTime = average(rawTimes)
        return averageTime
    
    def _get_time_stack(self, implementation, operation, iteration, average_bound):
        rawTimes = []        
        if operation == "push":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[STACK]["Implementations"][implementation]()
                start = time()
                for j in range(iteration):
                    instance.push(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "top":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[STACK]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.push(r)
                start = time()
                for j in range(iteration):
                    instance.top()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "pop":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[STACK]["Implementations"][implementation]()
                for r in range(iteration):
                    instance.push(r)
                start = time()
                for j in range(iteration):
                    instance.pop()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
                    
        averageTime = average(rawTimes)
        return averageTime
    
    def _get_time_tree(self, implementation, operation, iteration, average_bound):
        rawTimes = []        
        if operation == "insert":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[TREE]["Implementations"][implementation](0)
                nodes = [0]
                start = time()
                for j in range(iteration):
                    instance.insert(random.choice(nodes), j)
                    nodes.append(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "make_son":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[TREE]["Implementations"][implementation](0)
                nodes = [0]
                for r in range(iteration):
                    instance.insert(random.choice(nodes), r)
                    nodes.append(r)
                start = time()
                for j in range(iteration):
                    instance.make_son(j, random.choice(nodes))
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "get_path_to":
            instance = STRUCTURES_INSTANCE[TREE]["Implementations"][implementation](0)
            nodes = [0]
            for r in range(1, iteration):
                instance.insert(random.choice(nodes), r)
                nodes.append(r)
            for i in range(average_bound):                
                start = time()
                for j in range(iteration):
                    instance.get_path_to(random.choice(nodes))
                end = time()
                rT = (end - start)
                rawTimes.append(rT)                    
        averageTime = average(rawTimes)
        return averageTime
    
    def _get_time_priority_queue(self, implementation, operation, iteration, average_bound):
        rawTimes = []            
        if operation == "insert":
            for i in range(average_bound):
                if implementation == "2Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](2)
                elif implementation == "4Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](4)
                elif implementation == "8Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](8)
                elif implementation == "16Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](16)
                elif implementation == "32Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](32)
                elif implementation == "64Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](64)
                start = time()
                for j in range(iteration):
                    instance.insert(j, j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "delete_min":
            for i in range(average_bound):
                if implementation == "2Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](2)
                elif implementation == "4Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](4)
                elif implementation == "8Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](8)
                elif implementation == "16Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](16)
                elif implementation == "32Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](32)
                elif implementation == "64Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](64)
                for r in range(iteration):
                    instance.insert(r, r)
                start = time()
                for j in range(iteration):
                    instance.delete_min()
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "decrease_key":
            for i in range(average_bound):
                if implementation == "2Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](2)
                elif implementation == "4Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](4)
                elif implementation == "8Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](8)
                elif implementation == "16Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](16)
                elif implementation == "32Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](32)
                elif implementation == "64Heap":
                    instance = STRUCTURES_INSTANCE[PRIORITY_QUEUE]["Implementations"][implementation](64)
                infos = []
                for r in range(iteration):
                    random_key = 1000
                    instance.insert(r, random_key)
                    infos.append(r)
                start = time()
                for j in range(iteration):
                    randomInfo = random.choice(infos)
                    new_key = 5
                    instance.decrease_key(randomInfo, new_key)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
                    
        averageTime = average(rawTimes)
        return averageTime
    
    def _get_time_graph(self, implementation, operation, iteration, average_bound):
        rawTimes = []        
        if operation == "add_node":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[GRAPH]["Implementations"][implementation]()
                start = time()
                for j in range(iteration):
                    instance.add_node(j)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "add_arc":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[GRAPH]["Implementations"][implementation]()
                nodes = []
                for r in range(iteration):
                    instance.add_node(r, r)
                    nodes.append(r)
                start = time()
                for j in range(iteration):
                    randomNodeAId = random.choice(nodes)
                    randomNodeBId = random.choice(nodes)
                    instance.add_arc(randomNodeAId, randomNodeBId)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "get_incident_arcs":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[GRAPH]["Implementations"][implementation]()
                nodes = []
                for r in range(iteration):
                    instance.add_node(r, r)
                    nodes.append(r)
                for r in range(iteration):
                    randomNodeAId = random.choice(nodes)
                    randomNodeBId = random.choice(nodes)
                    instance.add_arc(randomNodeAId, randomNodeBId)
                start = time()
                for j in range(iteration):
                    randomNodeId = random.choice(nodes)
                    instance.get_incident_arcs(randomNodeId)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
        elif operation == "set_arc_status":
            for i in range(average_bound):
                instance = STRUCTURES_INSTANCE[GRAPH]["Implementations"][implementation]()
                nodes = []
                for r in range(iteration):
                    instance.add_node(r, r)
                    nodes.append(r)
                for r in range(iteration):
                    randomNodeAId = random.choice(nodes)
                    randomNodeBId = random.choice(nodes)
                    instance.add_arc(randomNodeAId, randomNodeBId)
                start = time()
                for j in range(iteration):
                    randomNodeAId = random.choice(nodes)
                    randomNodeBId = random.choice(nodes)
                    instance.set_arc_status(randomNodeAId, randomNodeBId, None)
                end = time()
                rT = (end - start)
                rawTimes.append(rT)
                    
        averageTime = average(rawTimes)
        return averageTime
    
    def plot_data(self, dataset, directory = PARAMS["output_dir"]):
        """
        Stores to the specified directory a MathPlotLib plot based on the specified dataset.
        
        plot_data(dataset, directory) -> None
        
        @type dataset: list of dictionaries
        @param dataset: the dataset to be plotted.
        @type directory: string
        @param directory: directory to store the computed MatPlotLib plot.
        """
        
        for struct_data in dataset:       
            structure = struct_data[0]["Structure"]
            implementations = " ".join(STRUCTURES_INSTANCE[structure]["Implementations"].keys())
            operation = str(struct_data[0]["Operation"])
            interval = str(struct_data[0]["Max Input"])
            plotFileName = STRUCTURES_NAME[structure] + " " + implementations + " " + operation + " " +  interval
            plotFilePath = os.path.join(directory, str(plotFileName))
            plotLabel = STRUCTURES_NAME[structure] + ": " + operation
            xLabel = "Input"
            yLabel = "Time (s)"
            legend = STRUCTURES_INSTANCE[structure]["Implementations"].keys()
            formattedDataset = []
            for data in struct_data:
                formattedDataset.append([data["X"], data["time"]])
            plot = make_plot(formattedDataset, plotLabel, xLabel, yLabel, legend)
            save_plot(plot, plotFilePath)
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
        
        for struct_data in dataset:
            structure = struct_data[0]["Structure"]
            implementations = " ".join(STRUCTURES_INSTANCE[structure]["Implementations"].keys())
            operation = str(struct_data[0]["Operation"])
            interval = str(struct_data[0]["Max Input"])
            plotFileName = STRUCTURES_NAME[structure] + " " + implementations + " " + operation + " " +  interval + ".txt"
            plotFilePath = os.path.join(directory, str(plotFileName))
            plotLabel = STRUCTURES_NAME[structure] + ": " + operation
            xLabel = "Input"
            yLabel = "Time (s)"
            legend = STRUCTURES_INSTANCE[structure]["Implementations"].keys()
            formattedDataset = []
            for data in struct_data:
                formattedDataset.append([data["X"], data["time"]])
            table = make_table(formattedDataset, plotLabel, xLabel, yLabel, legend)
            save_table(table, plotFilePath) 

def __test(profiler, params):
    """
    Data Structures Profiler Test.
    
    __test(profiler, params) -> None
    
    @type profiler: StructProfiler
    @param profiler: profiler instance.
    @type params: dictionary
    @param params: profiling parameters.
    """    
    
    print "### iPATH TEST PROFILER"
    print "### Data Type: Profiler ({})".format(str(profiler.__class__.__bases__[0].__name__))
    print "### Implementation {}".format(str(profiler.__class__.__name__))
    print "###"
    print "### Data Structures: {}".format(' '.join(STRUCTURES_NAME[structure] for structure in STRUCTURES))
    print "### Max Input: {}".format(str(params["max_input"]))
    print "### Average Bound: {}".format(str(params["average_bound"]))  
    print "### Output Directory: {}\n".format(str(params["output_dir"]))
    for structure in [PRIORITY_QUEUE]:
        params["structure"] = structure
        print "Profiling {} . . .".format(str(STRUCTURES_NAME[structure]))
        data = profiler.profile_all(params)
        print "Making Plot . . ."
        profiler.plot_data(data)
        print "Making Table . . .\n"
        profiler.table_data(data)
    
    print "\n### END OF TEST ###\n"              
    
if __name__ == "__main__":
    profiler = StructProfiler()
    params = PARAMS
    __test(profiler, params)