#name: Tan Wah Yang
#student id = 32772246
import collections # use as linked list for breadth first search
class ford_fulkerson_adt:
    """
      prevent passing parameter again and again between functions therefore class is used
    """
    
    def __init__(self, connections, maxIn, maxOut, origin, targets):
        """
        function description : takes in all argument as the example in the question, and do pre-processing 

        approach description (pre processing step) :
        first step: call update_connection by using all arguments in the question, which will makes the graph three times larger and max-in and max-out will become
        edge with capacity , new target id and new origin id will be established , so this function will update the graph and make sure that new origin is a new integer and 
        new target is only one integer
        second step: call initialize_reverse_adj_list using new_target and updated graph(from step one) as arguments, it will return a graph that has the same dimension 
        as the updated graph and the edges are reversed 
        third step: self.max_size = self.new_target + 1 , self.max_size will be use as variable by other functions so no need to be passed anywhere, this value denotes the 
        new maximum size of the graph in terms of vertex
        fourth step: call combined_graph by using updated graph(from step one) and graph returned by step two as argument. it will return a graph that combine edges of two graphs
        together , so the resulting graph will have twice edges as the updated graph and same amount of vertex as the updated graph.
        pre-processing done

        Input :
            connections : a list of tuples , in each tuple contains three numbers, first number is where the edge comes from ,
            second number is where the edge goes to , and the third number is the capacity of the flow
            example :  [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]

            maxIn: a list of integers which represent the capacity that a vertex can accept
            example :  [5000, 3000, 3000, 3000, 2000]

            maxOut: a list of integers which represent the capacity that a vertex can send
            example : [5000, 3000, 3000, 2500, 1500]

            origin: an integer that represents the vertex id that is going to send the data for backup
            example : 0

            targets: a list of integer that represents the vertex id that is going to receive data
            example : [4, 2]

        Output :
            an object ready to be used outside the class

        Time Complexity:
        Best: O(D+C) 
        Worst: O(D+C) 

        Aux space complexity: O(D+C)

        """
        self.new_origin, self.new_target, connections = self.update_connections(connections, origin, targets, maxIn, maxOut)
        twod_backward = self.initialize_reverse_adj_list(self.new_target, connections)
        self.max_size = self.new_target + 1
        self.final_graph = self.combined_graph(connections, twod_backward)


    def get_answer(self):
        """
        function description : get the final answer

        approach description : call ford-fulkerson by using instance variable self.new_origin and self.new_target

        Input :
            nothing

        Output :
            a number that represents the maximum data that can be sent from the origin to the targets
            example : 4500

        Time Complexity:
        best and worst : O(1) just retrieving the answer

        Aux space complexity: O(1)

        """
        return self.ford_fulkerson(self.new_origin, self.new_target)



    def find_max_vertex(self, connections):
        """
        function description : an auxilary function that is used by update_connections function

        approach description : loop through every tuple of connections and compare the first element and the second element of the tuple and record down the largest

        Input :
            connections: a list of tuples , in each tuple contains three numbers, first number is where the edge comes from ,
            second number is where the edge goes to , and the third number is the capacity of the flow 
            example :  [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]

        Output :
            an integer that represents the largest vertex id
            example : 4

        Time Complexity:
        Best and Worst: O(C)

        Aux space complexity: O(1)

        """
        largest = max(connections[0][0],connections[0][1])
        for i in connections:
            if max(i[0], i[1]) > largest:
                largest = max(i[0], i[1])
        return largest


    def initialize_adj_list(self, max_vertex, connections):
        """
        function description : an auxilary function that is used by update_connections function

        approach description : initialize a list of lists that has the same dimension as connections and loop through connections
        since each tuple in connections represent an edge therefore append the edge to the respective position in the list of lists

        Input :
            connections: a list of tuples , in each tuple contains three numbers, first number is where the edge comes from ,
            second number is where the edge goes to , and the third number is the capacity of the flow 
            example :  [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]

            max_vertex: an integer that represents the largest vertex id
            example :  4

        Output :
            an list of lists , an adjacency list representation of the graph
            [[[1, 3000],[3,2000]], [[2, 2000],[3, 1000]],[], [[4,2000],[2,1000]],[]]

        Time Complexity: 
        best and worst case : O(D+C) C is for looping each tuple in the list and D + C is the time used to create the empty adjacency list

        Aux space complexity: O(D+C)

        """
        twod_list = [[] for i in range(max_vertex+1)]
        for i in connections:
            twod_list[i[0]].append([i[1],i[2]])
        return twod_list


    def update_connections(self, connections, origin, targets, maxIn, maxOut):
        """
        function description : a function that is called in def__init__ , it can create a graph that has only one target and transform all maxin and maxout into edges and update new origin
        for each vertex it will create two more vertex for example vertex A will have incoming vertex A and outgoing vertex A , incoming vertex A will have only one outgoing edge with a capacity 
        equals to the maxIn value of vertex A connects to vertex A and incoming Vertex A has all incoming edges same as vertex A, Outgoing vertex A will only have an incoming edge with a capacity 
        equals to the maxOut value of vertex A and the edge comes from vertex A, and the original vertex A will have an outgoing edge and an incoming edge only.
        for each target vertex, it will have an extra edge with capacity equal to the maxin value that points from the original vertex of the target vertex to the new target vertex

        approach description : 
        first step: calculate max vertex id using find_max_vertex function (explained above)
        second step: calculate new target id using a formula and max_vertex id returned in step one
        third step: initialize a list of lists that has the same length as new_target
        fourth step: initialize adjacency list by calling initialize_adj_list(explained above)
        fifth step: use the adjacency list returned in fourth step and loop through each edge of each vertex, if the vertex index is equal to origin
        calculate the new origin using the formula and index, and take the ougoing edge of the vertex append to outgoing vertex and the edge points to incoming vertex of another vertex
        before looping each edges of the next vertex use maxin as an edge capacity and connect it from the incoming vertex to the vertex, and use maxout as an edge capacity and connect it 
        from the vertex to its outgoing vertex,so that each original vertex only has one incoming edge and one outgoing edge which have maxin and maxout capcacity respectively
        sixth step: loop through each target id, for each target appends an edge with capacity equals to maxin of that vertex and connect to the new target at the target position

        Input :
            connections: a list of tuples , in each tuple contains three numbers, first number is where the edge comes from ,
            second number is where the edge goes to , and the third number is the capacity of the flow 
            example :  [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]

            maxIn: a list of integers which represent the capacity that a vertex can accept
            example :  [5000, 3000, 3000, 3000, 2000]

            maxOut: a list of integers which represent the capacity that a vertex can send
            example : [5000, 3000, 3000, 2500, 1500]
            
            origin: an integer that represents the vertex id that is going to send the data for backup
            example : 0

            targets: a list of integer that represents the vertex id that is going to receive data
            example : [4 , 2]

        Output :
            new_connections : an list of lists , an adjacency list representation of the graph
            [[[1, 5000]], [[2, 5000]], [[3, 3000], [9, 2000]], [[4, 3000]], [[5, 3000]], [[6, 2000], [9, 1000]], [[7, 3000]], [[8, 3000]], [[15, 3000]], [[10, 3000]], [[11, 2500]], [[12, 2000], [6, 1000]], [[13, 2000]], [[14, 1500]], [[15, 1500]], []]

            new_target : an integer
            example : 15

            new_origin: an integer
            example : 1


        Time Complexity: 
        Best and Worst Case : O(D+C)

        Aux space complexity: O(D+C)

        """
        # update connections as follow
        # every maxin maxout
        max_vertex = self.find_max_vertex(connections)
        new_target = ((max_vertex + 1) * 3)
        new_connections = [[] for i in range(new_target + 1)]
        twod_list = self.initialize_adj_list(max_vertex, connections)
        new_origin = (origin * 3) + 1
        x = 0
        for i in twod_list:
            for j in i:
                new_connections[(x * 3) + 1 + 1].append([(j[0] * 3) + 1 - 1, j[1]])
            new_connections[(x * 3) + 1].append([(x * 3) + 1 + 1, maxOut[x]])
            new_connections[(x * 3) + 1 - 1].append([(x * 3) + 1, maxIn[x]])
            x += 1
        #pre process new target
        # for each target
        # connect to new target
        for i in targets:
            if max_vertex >= i:
                new_connections[(i * 3) + 1 ].append([new_target, maxIn[i]])
        return new_origin, new_target, new_connections


    #backup
    def initialize_reverse_adj_list(self, max_vertex, connections):
        """
        function description : an function that takes in an adjacency list represenation of a graph and return a new graph that has the same amount of vertex and edges
        but the edges are in opposite direction.

        approach description : 
        first step: initialize a list of lists that has the same dimension as connections
        second step: loop through each edges of each vertex and append it oppositely to the newly created list of lists, with weight of 0 , beacuse all backward edges have
        0 capacity before ford-fulkerson starts

        Input :
            connections: a list of lists , in each list contains two numbers, first number is where the edge points to ,
            and the second number is the capacity of the flow , the index of the list corresponds to the vertex id 
            [[[1, 5000]], [[2, 5000]], [[3, 3000], [9, 2000]], [[4, 3000]], [[5, 3000]], [[6, 2000], [9, 1000]], [[7, 3000]], [[8, 3000]], [[15, 3000]], [[10, 3000]], [[11, 2500]], [[12, 2000], [6, 1000]], [[13, 2000]], [[14, 1500]], [[15, 1500]], []]

            max_vertex: an integer that represents the largest vertex id
            example : 15

        Output :
            twod_list: an list of lists , an adjacency list representation of the graph
            example : [[], [[0, 0]], [[1, 0]], [[2, 0]], [[3, 0]], [[4, 0]], [[5, 0], [11, 0]], [[6, 0]], [[7, 0]], [[2, 0], [5, 0]], [[9, 0]], [[10, 0]], [[11, 0]], [[12, 0]], [[13, 0]], [[8, 0], [14, 0]]]

        Time Complexity:
        Best Case and Worst Case : O(D+C)

        Aux space complexity: O(D+C)

        """
        twod_list = [[] for i in range(max_vertex + 1)]

        x = 0
        for i in connections:
            for j in i:
                twod_list[j[0]].append([x, 0])
            x += 1
        return twod_list


    def combined_graph(self, twod_list, twod_backward):
        """
        function description : an function that takes in two adjacency list represenation of two graphs and return a new graph that has the same amount of vertex and has
        all edges of the two graphs , the number of edges are equals to the total number of edges of the two input graph

        approach description : 
        loop through every edge of every vertex of the second input graph and append the edges to the correct position in the first graph

        Input :
            twod_list: a list of lists , an adjacency list representation of the graph
            example : [[[1, 5000]], [[2, 5000]], [[3, 3000], [9, 2000]], [[4, 3000]], [[5, 3000]], [[6, 2000], [9, 1000]], [[7, 3000]], [[8, 3000]], [[15, 3000]], [[10, 3000]], [[11, 2500]], [[12, 2000], [6, 1000]], [[13, 2000]], [[14, 1500]], [[15, 1500]], []]

            twod_backward:  a list of lists , an adjacency list representation of the graph
            example : [[], [[0, 0]], [[1, 0]], [[2, 0]], [[3, 0]], [[4, 0]], [[5, 0], [11, 0]], [[6, 0]], [[7, 0]], [[2, 0], [5, 0]], [[9, 0]], [[10, 0]], [[11, 0]], [[12, 0]], [[13, 0]], [[8, 0], [14, 0]]]

        Output :
            a list of lists , an adjacency list representation of the graph
            example : [[[1, 5000]], [[2, 5000], [0, 0]], [[3, 3000], [9, 2000], [1, 0]], [[4, 3000], [2, 0]], [[5, 3000], [3, 0]], [[6, 2000], [9, 1000], [4, 0]], [[7, 3000], [5, 0], [11, 0]], [[8, 3000], [6, 0]], [[15, 3000], [7, 0]], [[10, 3000], [2, 0], [5, 0]], [[11, 2500], [9, 0]], [[12, 2000], [6, 1000], [10, 0]], [[13, 2000], [11, 0]], [[14, 1500], [12, 0]], [[15, 1500], [13, 0]], [[8, 0], [14, 0]]]

        Time Complexity: 
        Best and Worst Case : O(D+C)

        Aux space complexity: O(D+C)

        """
        x = 0
        for i in twod_backward:
            for j in i:
                twod_list[x].append(j)
            x += 1
        return twod_list


    def breath_first_search(self, start_vertex, end_vertex, backtrack):
        """
        function description : an function that find a path from start vertex to end vertex, use collection and deque library since popleft() will have complexity of O(1)

        approach description : 
        First step: initialize a visited array with a dimension same as instance variable self.max_size and value are initialised to False(means haven't visited yet)
        Second step: initialize a built-in linked list and use it as a queue
        third step: add the start vertex into the queue and switch the visited position of start_vertex to True(start vertex is the first to be visited always)
        fourth step:check if the queue is empty if not continue to loop
        inside the loop pop the first element of the queue which is the vertex id 
        for each edge of the popped vertex check if the vertex that the edge is pointing to is not visited and the capacity is larger than 0 or not
        if yes append the new vertex to the queue and switch the new vertex position in the visited array to True and put the current vertex value in the positon of the 
        new vertex in the backtrack array. Before looping the next edge check if the new vertex is the end_vertex if yes then return True and the backtrack array 
        this means ending the bfs earlier.(since already found a path from start to end)
        if after running the while loop True and backtrack is not returned then it means end_vertex is not visited it will return False and None(end stage of ford_fulkerson)
        
        Input :
            start_vertex: an integer representing the vertex id where the bfs should start to traverse from
            example : 1

            end_vertex: an integer representing the vertex id where the bfs should end and return the result
            example: 15

            backtrack: a list of integer
            example: [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

        Output :
            boolean value :True if there is a path from start to end and Flase if there dont exist a path from start to end
            or 
            backtrack or None: None when the boolean value is false, backtrack when the boolean value is true

            example: 
            True, [None, None, 1, 2, 3, 4, 11, 6, 7, 2, 9, 10, 11, 12, 13, 14]
            False, None

        Time Complexity: 
        Best and Worst case: O(D+C)

        Aux space complexity: O(D) creating backtrack array

        """
        Visited = [False] * (self.max_size)
        #Queue = []
        Queue = collections.deque()
        Queue.append(start_vertex)
        Visited[start_vertex] = True
        while Queue:
            #visiting = Queue.pop(0)
            visiting = Queue.popleft()
            for edge in self.final_graph[visiting]:
                if Visited[edge[0]] == False and edge[1] > 0:
                    Queue.append(edge[0])
                    Visited[edge[0]] = True
                    backtrack[edge[0]] = visiting
                    if edge[0] == end_vertex:
                        return True, backtrack
        return False, None


    def ford_fulkerson(self, start, end):
        """
        function description : an function that given a graph with positive value weight and two vertex id one start and one end, it will find the largest flow 
        from start to end (a standard ford-fulkerson algorithm)
        
        approach description : 
        First step: initialize maximum_flow as 0 , initialize backtrack array 
        second step: run breath_first_search using start_vertex and end_vertex as argument
        third step: if breath_first_search return true then use the backtrack array to find the bottleneck capacity 
        fourth step: add the bottleneck capacity to the maximum flow
        fifth step: decrease the flow for all foward edge along the path by the bottleneck capacity and increase the flow for all backward edge along the path by the bottleneck capacity
        sixth step: initialize the backtrack array and run breath_first_search again before going to the next loop
        it will continously run bfs until end_vertex can't be found then it will return the maximum_flow value

        
        Input :
            start_vertex: an integer representing the vertex id where the bfs should start to traverse from
            example: 1

            end_vertex: an integer representing the vertex id where the bfs should end and return the result
            example : 15

        Output :
            maximum_flow : a number
            example: 4500

        Time Complexity: 
        Best and Worst Case: O(f(D+C)) where f is the flow and (D+C) is the augment complexity and also BFS complexity
        since D is at most C + 1 (because the graph must be connected) so complexity becomes O(fC) in order to eliminate f,
        need to rule out how many times bfs will run given a graph with V vertices and E edges. Since BFS always gives the
        shortest path from start to end in term of number of edges, and the number of unique path from start to end vertex
        given a graph with v vertices and e edges is at most V times E , therefore the complexity eventually becomes O(DC^2)

        Aux space complexity: O(D) because of backtrack array

        """
        backtrack = [None] * (self.max_size)
        maximum_flow = 0
        flag, backtrack = self.breath_first_search(start, end, backtrack)
        while flag:
            Path_flow = float("Inf")
            path = end
            while (path != start):
                for i in self.final_graph[backtrack[path]]:
                    if i[0] == path:
                        weight = i[1]
                Path_flow = min(Path_flow, weight)
                path = backtrack[path]
            maximum_flow += Path_flow
            vertex = end
            while (vertex != start):
                comes_from = backtrack[vertex]

                for i in self.final_graph[comes_from]:
                    if i[0] == vertex:
                        i[1] -= Path_flow

                for i in self.final_graph[vertex]:
                    if i[0] == comes_from:
                        i[1] += Path_flow

                vertex = backtrack[vertex]
            backtrack = [None] * (self.max_size)
            flag, backtrack = self.breath_first_search(start, end, backtrack)
        return maximum_flow


def maxThroughput(connections, maxIn, maxOut, origin, targets):
    """
    function description : follow assignment specs exactly

    approach description : create ford_fulkerson_adt object with all the parameters that are received by maxThroughput,
    and call get_answer function located inside the class to get the answer

    Input :
            connections : a list of tuples , in each tuple contains three numbers, first number is where the edge comes from ,
            second number is where the edge goes to , and the third number is the capacity of the flow
            example :  [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]

            maxIn: a list of integers which represent the capacity that a vertex can accept
            example :  [5000, 3000, 3000, 3000, 2000]

            maxOut: a list of integers which represent the capacity that a vertex can send
            example : [5000, 3000, 3000, 2500, 1500]

            origin: an integer that represents the vertex id that is going to send the data for backup
            example : 0

            targets: a list of integer that represents the vertex id that is going to receive data
            example : [4, 2]

    output:
        number : returned by get_answer
        example: 4500

    Time Complexity: 
    Best case and worst case: O(1)

    Aux space complexity: O(1)

    """
    return ford_fulkerson_adt(connections, maxIn, maxOut, origin, targets).get_answer()


connections = [(0, 1, 4), (2, 4, 12), (0, 4, 5), (2, 1, 11), (3, 4, 10), (2, 0, 7), (3, 2, 15)]
maxIn = [1, 9, 11, 5, 15]
maxOut = [8, 8, 9, 11, 13]
origin = 1
targets = [2, 3]
print(maxThroughput(connections, maxIn, maxOut, origin, targets))
class node:

    """
    Trie has nodes, and need several payloads to meet the assignment spec
    """
    def __init__(self, value):
        """

        function description : takes in value and assign it to self.value 

        approach description :
        initialize as follow
        child as a list of none , a newly created node will not have any child initially
        number(denote the largest frequency that passed by ) as 0
        is_end(denote that it doesn't have any child) as false 
        unique number(denote how many words end at this node) as 0

        Input :
            value: lowercase a-z only 

        Output :
            an object ready to be used outside the class

        Time Complexity: O(1)

        Aux space complexity: O(1)

        """
        self.child = [None for i in range(26)]
        self.value = value
        self.number = 0
        self.is_end = False
        self.unique_number = 0

class CatsTrie:
    """
    required class for the assignment spec
    """

    def __init__(self, sentences):
        """
        function description :store node object and has a root node

        approach description : initialize self.root as a node object with value ""
        loop through each string in sentences and insert each string into the trie using insert_into_trie function

        Input :
            sentences: list of strings
            example: ["abc", "abazacy", "dbcef", "xzz", "gdbc", "abazacy", "xyz", "abazacy", "dbcef", "xyz", "xxx", "xzz"]

        Output :
            an object ready to be used outside the class

        Time Complexity:
        Best and Worst Case: O(NM) M is the longest string in sentences and N is the number of string

        Aux space complexity: O(NM) M is the longest string in sentences and N is the number of string

        """
        self.root = node("")
        for i in sentences:
            self.insert_into_trie(i, self.root, 0)


    def insert_into_trie(self, string, root, index):
        """
        function description : recursive function that store words into the trie by storing one character at easch recursion level all the way until the last character
        of the string and recurse back with latest frequency value and record down and assign the largest frequency into number instance variable (node object).
        Also it will switch the boolean value is_end to the correct value and update the unique_number at the base case. All nodes in the trie are linked using node child
        list which always contains 26 elements and elements are all node objects.

        approach description : 
        
        starting from the first character of the string to be inserted
        
        calculate the position in the child to insert the character , 

        if the position is None (means the node doesnt exist) then create a new node with the character as value and put it in the correct position of the root's child list
        and traverse to the new child node.
        
        If the index is same as the length of string -1 means base case is reached switch the newly created node is_end from false to true
        and unique number is added by one. unique number denote the number of word that ends here and return the largest number among root.number and child.number.
        
        if the position is not None means a node already exists, then traverse to the node check if the existing node is end and the index is not pointing to the last string or not
        if both conditions is satisfied this means the string to be inserted is longer than the deepest node at the current path so need to switch is_end from true to false
        
        if the index is pointing to the last character of the string means the base case is reached, increase the unique_number by 1  
        (if the node already exits then need to check if the current node number is smaller than the current unique_number or not if yes then assign unique number to current node number)
        and return the largest number among root.number and child.number.
        
        if base case is not reached, enter next recursion level by using the same string and using the child node and index+1 as argument(new index is points to the next character 
        to be inserted) and assign the result of largest value among the root.number and the value returned by the function( since it will return number after the base case is reached)

        recurse back will choose the largest among number among the parent node or the child node and assign it to the parent node and return parent node number to the upper recursion


        Input :
            string: a string with at least one character
            example: "hello"

            root: the node to insert the character
            example: node object

            index: denote the position of character in string that is to be added
            example: 0 , 1, 2 , 3 ....len(string) - 1
            (start form 0 at the first recursion level and increase by 1 before moving to subsequent recursion level until base case is reach )

        Output :
            Nothing

        Time Complexity:
        Best case: O(1) when string is one character only
        worst case: O(M) when the string is longer than the deepest node of the entire trie

        Aux space complexity: O(M)

        """ 
        if root.child[ord(string[index]) - 97] == None:
            root.child[ord(string[index]) - 97] = node(string[index])
            child = root.child[ord(string[index]) - 97]
            if len(string) -1 == index: # base case
                child.is_end = True
                child.unique_number += 1
                child.number += 1
                root.number = max(root.number, child.number)
                return root.number
        else:
            child = root.child[ord(string[index]) - 97]
            if len(string) - 1 - index >= 1 and child.is_end:
                child.is_end = False
            if len(string) -1 == index:  #base case
                child.unique_number += 1
                if child.unique_number > child.number:
                    child.number = child.unique_number
                root.number = max(root.number, child.number)
                return root.number
        root.number = max(root.number, self.insert_into_trie(string, child, index + 1))
        return root.number


    def find_suggestion(self, node):
        """
        function description : an auxillary function ,given a node as starting point find suggestion, suggestion is the string 
        that is lexicographically smallest among all largest frequencies(equally large frequency)

        approach description :

        check if the node is_end if yes this means that it can return the suggestion by joining it into string (which means it 
        is lexicographically smallest among all largest frequencies(equally large frequency) ), 

        if not, initialize as follow 
        largest to 0 (use to compare frequency), 
        largest index(index in the child list that is lexicographically smallest among all largest frequencies(equally large frequency))to None
        x = 0 (use as counter)

        loop through every child of this node if it's not None means node exists, then check if the number of the node is larger
        than largest if yes then update largest with the child number and record the index, increment x by one and enter the 
        next loop. 

        if the child position is None then increment x by 1 and nenter next loop
        
        After inspecting all children's number, largest should have the largest number of the children node
        largest index will have index in the child list that has largest number and also lexicographically smallest value.

        Now check if the node unique number is at least equal to largest or not 
        if it is means can return since children node
        will be deeper than the current node , which means lexicographically larger , and node's unique number is at least largest means
        this word exists in the trie for at least largest amount of time so no need to go any deeper.

        else need to traverse deeper by using the largest index to get node child and assign it to node and append the value of current node
        to suggestion list and enter the next loop.

        Input :
            node: the node to start from(node object)
    
        Output :
            a string
            example: "hello"

        Time Complexity: 
        Best Case : O(1) when the node is already is_end
        Worst Case : O(Y) when the suggestion is the longest string in the entire trie and the input of this function has a value of
        node.value == "" which means it needs to start from the root node and traverse all the way until the deepest node of the entire trie.
        (Output-sensitive) 
        

        Aux space complexity: O(Y) because of all_suggestion list

        """
        all_suggestion = []
        while not node.is_end:
            x = 0
            largest = 0
            largest_index = None
            for i in node.child:
                if i != None:
                    if i.number > largest:
                        largest = i.number
                        largest_index = x
                x += 1
            if node.unique_number >= largest:
                return "".join(all_suggestion)
            else:
                node = node.child[largest_index]
                all_suggestion.append(node.value)
        return "".join(all_suggestion)


    def autoComplete(self, string):
        """
        function description : given a string find whether it exists in trie or not, if not return none, else if it exists
        return lexicographically smallest among all largest frequencies(equally large frequency)suggestion is found by 
        using find_suggestion function , autoComplete is just traverse to the correct node and pass it to find_suggestion
        
        if the input string is "" just simply return the string that is lexicographically smallest among all largest 
        frequencies (equally large frequency) by passing root node to find_suggestion

        if the string doesnt exist at all in the trie then return none
        
        approach description : 
        initialize as follow
        x to 0 
        current node to be root node
        string_exits to false
        if string is "" then call find_suggestion using root node(explained above)
        else two cases 
        first case: string doesnt exist at all in the trie , current_node.child[ord(i) - 97] will be equal to None , 
        so it will exit the for loop string_exists will be false and return None at the end , if not None then continue to 
        traverse by assigning current node with the correct child of the previous node
        second case: string exists in trie therefore suggestion exists, in this case loop will continue until the last 
        character of the string and current node's child node value is the last character the call find_suggestion using this
        child node.
        
        finally check if string_exists, if no means the string doesnt exists in trie therefore return none
        else the final answer will be string + all suggestion where all suggestion is the string returned by find_suggestion
        
        Input :
            a string
            example:"hello"
    
        Output :
            a string 
            example: "helloabzacy"

        Time Complexity:
        Best Case: O(X)
        when the string exists in the trie and it is the end or it is lexicographically smallest among all largest frequencies(equally large frequency)
        when the string doesn't exist in the trie at all

        Worst Case: O(X + Y) when the answer is the longest string stored in the entire trie

        Aux space complexity: O(X + Y) because of string + all_suggestion

        """
        x = 0
        current_node = self.root
        string_exists = False
        if string == "":
            return self.find_suggestion(current_node)
        else:
            for i in string:
                if current_node.child[ord(i) - 97] != None:
                    if current_node.child[ord(i) - 97].value == i and x != len(string) - 1:
                        current_node = current_node.child[ord(i) - 97]
                    elif current_node.child[ord(i) - 97].value == i and x == len(string) - 1:   # at least one suggestion exists
                        all_suggestion = self.find_suggestion(current_node.child[ord(i) - 97])
                        string_exists = True
                        break
                else:
                    break
                x += 1
            if string_exists:
                return string + all_suggestion
            else:
                return None