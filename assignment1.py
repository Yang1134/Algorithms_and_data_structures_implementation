#name: Tan Wah Yang
#srudent id: 32772246


#Question 1
def optimalRoute(start, end, passengers, roads):
    """
    
    Description : takes four parameters and returns a list that represents a path. Find the shortest
    path weight from start to end , and able to determine whether to pick up passenger to make the path weight shorter
    from start to end.

    Approach :
    First step: find maximum vertex using roads by calling find_max_vertex
    second step: use the maximum vertex value and roads to initialize an answer list (vertex in order) by calling
    initialize_answer_list ( stores weight of normal lane only)
    third step: call dijkstra using start vertex, max number of vertex, and the answer list as parameters
    fourth step :use the maximum vertex value and roads to initialize an answer list (vertex in order) by calling
    initialise_reverse_pool_graph ( stores weight of car pool lane only)
    fifth step: call dijkstra using start vertex, max number of vertex, and the answer list(returned by
    initialise_reverse_pool_graph)
    last step: call find_shortest using the array and answer returned by dijkstra in third step ,
    array and answer returned by dijkstra in fifth step , passenger list , start and end

    main idea : run dijkstra using normal lane from start to end , then run dijkstra using carpool lane from end to
    start (reverse graph), if vertex A has passenger then check whether the weight of starting from start to end using
    normal lane is larger than the weight of starting from start to vertex A using normal lane + the weight of starting from end
    to vertex A using car pool lane. If larger, then the answer will be updated to the path of starting from start
    to vertex A using normal lane + the path of starting from end to vertex A using car pool lane and continue to
    compare next location with passenger with the updated answer until no passenger left.
    If no passenger exists, the answer is simply the path starting from start to end using normal lane
    After all the comparison it will recreate the path

    input : start (an integer), end(an integer), passengers(a list of integers), roads(a list of lists,
    the inner list contains four integers)
    start : 0
    end : 4
    passengers : [1,2,3,5]
    roads : [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
         (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20), (0, 5, 12, 9)]

    output : a list of integer begins with the start number and ends with the end number, representing a path
    return : [0, 1, 2, 3, 4]

    time complexity :
    Best: O(|R|Log|L|) no passenger
    Worst: O(|R|Log|L|)
    Space complexity: 
    Input: O(|L|+|R|)
    aux space complexity: O(|L|+|R|)



    """

    def find_max_vertex(roads):
        """

        Description: find_max_vertex using roads as parameter

        Approach : loop through each of the roads and return the largest vertex number.

        input : roads(a list of lists)
        roads : [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
         (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20), (0, 5, 12, 9)]

        Return:
        output : an integer
        5

        time complexity :
        Best: O(|R|) still loop through everything
        Worst: O(|R|)

        Space complexity:
        Input:  O(|R|)
        aux space complexity: O(1)


        """
        max_vertex = max(roads[0][0], roads[0][1])
        for i in roads:
            if max(i[0], i[1]) > max_vertex:
                max_vertex = max(i[0], i[1])
        return max_vertex

    def initialize_answer_list(max_vertex, roads):
        """

        Description: create a 2D array, so can it can be used by dijkstra

        Approach : initialize a list of lists , the inner list is ["undefined", i, []] where i is from 0 to max_vertex
        ,for each road append the weight of normal lane and the location the edge goes to the location in the list,
        where the edge comes from.

        input : roads(a list of lists) and max_vertex (an integer)
        5, [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
         (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20), (0, 5, 12, 9)]

        output : an 2D list  with three columns( first column is used to store
        predecessor(initialize to undefined), second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight(normal lane) for each vertex and also which vertex the edge goes to)
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective index in heap and respective edges
        Return:
        answer: [["undefined", 1, [[3, 5],[5, 12]]],["undefined", 2, [[1, 10],[4, 30]]],["undefined", 3, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []]

        time complexity :
        Best:O(|L|+|R|) always create adjancency list
        Worst:O(|L|+|R|) always create adjancency list

        Space complexity:
        Input: O(|R|) always create adjancency list
        aux space complexity: O(|L|+|R|) always create adjancency list

        """
        answer = [["undefined", i, []] for i in range(max_vertex+1)]
        for i in roads:
            answer[i[0]][2].append([i[1],i[2]])
        for i in answer:
            i[1] = i[1] + 1
        return answer

    def initialise_reverse_pool_graph(max_vertex, roads):
        """

        Description: create a 2D array, so can it can be used by dijkstra

        Approach : initialize a list of lists , the inner list is ["undefined", i, []] where i is from 0 to max_vertex
        ,for each road append the weight of car pool lane and the location the edge comes from to the location in the
        list, where the edge goes to.

        input : roads(a list of lists) and max_vertex (an integer)
        5, [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
         (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20), (0, 5, 12, 9)]

        output : an 2D list  with three columns( first column is used to store
        predecessor(initialize to undefined), second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight(car pool lane) for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.
        return
        answer: [["undefined", 1, [[4,10],[2,2]]],["undefined", 2, [[0,10]]],["undefined", 3, [[3,2]]]
        ,["undefined", 4, [[0,3]]],["undefined", 5, [[3,15],[2,25],[1,20]]],["undefined", 6, [[0,9]]]


        time complexity :
        Best: O(|L|+|R|) always create adjancency list
        Worst : O(|L|+|R|) always create adjancency list
        Space complexity:
        Input: O(|R|) always create adjancency list
        aux space complexity: O(|L|+|R|) always create adjancency list

        """
        answer = [["undefined", i, []] for i in range(max_vertex+1)]
        for i in roads:
            answer[i[1]][2].append([i[0], i[3]])
        for i in answer:
            i[1] = i[1] + 1
        return answer

    def serve(heaparray, answer, length):
        """

        Description: swap the element of the top of the min heap (which is the smallest, located at index 1 of the
        array) with the end of the heap(located at the end of the array), and shorten the length of list by size of 1
        update the answer array at the same time.

        Approach : swapping element using temporary variable

        input : length (an integer), heaparray (a list of lists, inner list is of type [vertex id, weight]),
         an 2D list with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.
        output : an 2D list  with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges. New length of the array and updated heap array
        [[None],[0,0],[1,float('inf')],[2, float('inf')],[3,float('inf')],[4,float('inf')],[5,float('inf')]],
         [["undefined", 1, [[3, 5],[5, 12]]],["undefined", 2, [[1, 10],[4, 30]]],["undefined", 3, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []], 6

        return
        answer: [["undefined", 6, [[4,10],[2,2]]],["undefined", 2, [[0,10]]],["undefined", 3, [[3,2]]]
        ,["undefined", 4, [[0,3]]],["undefined", 5, [[3,15],[2,25],[1,20]]],["undefined", 1, [[0,9]]]
        [[None],[5,float('inf')],[1,float('inf')],[2, float('inf')],[3,float('inf')],[4,float('inf')],[0,0]]

        time complexity :
        Best: O(1)
        Worst : O(1)

        Space complexity:
        input : O(|L|+|R|)
        aux space complexity: O(1) only doing operation within the input

        """

        temp = heaparray[length - 1]
        answer[temp[0]][1] = 1
        heaparray[length - 1] = heaparray[1]
        answer[heaparray[1][0]][1] = length - 1
        heaparray[1] = temp
        # make heaparray smaller by 1
        #answerheaparray.insert(0, heaparray.pop())
        return heaparray, answer, length -1

    def rise(heaparray, index, answer):
        """
        Description: arrange the element at index position of the heap array to the correct position

        Approach :  compare the weight of element at index position with its parent , if smaller than
        its parent, then swap with that parent until that element is larger than its parent

        input : heaparray (a list of lists, inner list is of type [vertex id, weight]),index(integer),
         an 2D list with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.
        output : an 2D list  with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.  Updated heap array
        Input: [[None],[0,float('inf')],[1,float('inf')],[2, 0],[3,float('inf')],[4,float('inf')],[5,float('inf')]], 3,
         [["undefined", 1, [[3, 5],[5, 12]]],["undefined", 2, [[1, 10],[4, 30]]],["undefined", 3, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []]

        Return: [[None],[2,0],[1,float('inf')],[0,float('inf')],[3,float('inf')],[4,float('inf')],[5,float('inf')]],
         [["undefined", 3, [[3, 5],[5, 12]]],["undefined", 2, [[1, 10],[4, 30]]],["undefined", 1, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []]

        Time complexity:
        Best: O(1) position in heap array doesnt move foward when the weight is decreased
        Worst: O(log|L|)

        Space complexity:
        Input:  O(|L|+|R|)
        aux space complexity: O(1) only doing operation within the input

        """
        parent = index // 2
        while parent >= 1:
            if heaparray[parent][1] > heaparray[index][1]:
                temp = answer[heaparray[parent][0]][1]
                answer[heaparray[parent][0]][1] = answer[heaparray[index][0]][1]
                answer[heaparray[index][0]][1] = temp

                temp = heaparray[parent]
                heaparray[parent] = heaparray[index]
                heaparray[index] = temp

                index = parent
                parent = parent // 2
            else:
                break
        return heaparray, answer

    def fall(heaparray, index, answer, length):
        """
        Description: arrange the element at index position of the heap array to the correct position

        Approach :  compare the weight of element at index position with its child , if smaller than one of its child,
        then swap with that child, if smaller than both child , then compare two child, find the smallest child to
        swap with element at index. Swap until element is smaller than both of its child

        input : length (an integer), heaparray (a list of lists, inner list is of type [vertex id, weight]),index(integer)
        an 2D list with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.
        output : an 2D list  with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to,
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective position in heap and respective edges.  Updated heap array
         Input: [[None],[2,100],[1,1)],[0,2],[3,float('inf')],[4,float('inf')],[5,float('inf')]], 1,
         [["undefined", 3, [[3, 5],[5, 12]]],["undefined", 2, [[1, 10],[4, 30]]],["undefined", 1, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []], 6

        Return: [[None],[1,1],[2,100],[0,2],[3,float('inf')],[4,float('inf')],[5,float('inf')]],
         [["undefined", 3, [[3, 5],[5, 12]]],["undefined", 1, [[1, 10],[4, 30]]],["undefined", 2, [[4, 30],[ 0, 2]]]
        ,["undefined", 4, [[4, 35],[2, 2]]],["undefined", 5, [[0, 15]]],["undefined", 6, []]


        time complexity
        Best:O(1)position in heap array doesnt move backward when the weight is increased
        Worst: O(log|L|)

        Space complexity:
        Input:  O(|L|+|R|)
        aux space complexity: O(1) only doing operation within the input

        """
        child = 2 * index
        while child <= length - 1:
            if child < length - 1 and heaparray[child + 1][1] < heaparray[child][1]:
                child += 1
            if heaparray[index][1] > heaparray[child][1]:
                temp = answer[heaparray[child][0]][1]
                answer[heaparray[child][0]][1] = answer[heaparray[index][0]][1]
                answer[heaparray[index][0]][1] = temp

                temp = heaparray[child]
                heaparray[child] = heaparray[index]
                heaparray[index] = temp
                index = child
                child = 2 * index
            else:
                break
        return heaparray, answer

    def dijkstra(start, max_vertex, answer):

        """

        Description: calculate shortest path , starting from start vertex

        Approach : max_vertex used to initialize the heap array and to stop the main loop of dijkstra, start is to
        let dijkstra knows that the start vertex have 0 weight and no predecessor. The heap array stores the weight
        of each vertex and also the position of each vertex in the answer list, initially all are infinity.
        Answer list is the mapping table to the position of each vertex in the heap. start using start vertex,
        serve the heap (update the answer at the same time), then sink the heap (update the answer at the same time),
        In the inner loop for each edges in the currently visiting edge check for smaller weight to reach, if exists
        relax the edge and rise the heap (update the answer at the same time).

        input : start(an integer), max_vertex (an integer), answer (a list with length max_vertex,
        their respective edges, respective predecessor and respective position in the heap  )
        output : an 2D list  with three columns( first column is used to store
        predecessor(initialize to undefined), second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to)
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective index in heap and respective edges and a heap with final weight of each vertex.
        start: 0
        max_vertex: 4
        answer: [['undefined', 1, [[3, 5], [1, 10]]], ['undefined', 2, [[4, 30]]], ['undefined', 3, [[4, 30], [0, 2]]], ['undefined', 4, [[4, 35], [2, 2]]], ['undefined', 5, [[0, 15]]]]

        Return:
        heaparray: [None, [4, 37], [1, 10], [2, 7], [3, 5], [0, 0]]
        answer: [['undefined', 5, [[3, 5], [1, 10]]], [0, 2, [[4, 30]]], [3, 3, [[4, 30], [0, 2]]], [0, 4, [[4, 35], [2, 2]]], [2, 1, [[0, 15]]]]

        Time complexity:
        Best: O(|R|Log|L|)
        Worst: O(|R|Log|L|)

        Space complexity:
        Input: O(|R|+|L|)
        Aux: O(|L|)


        """
        heaparray = [[0, float('inf')] for i in range(max_vertex + 2)]
        heaparray[0] = None
        for i in range(len(answer)):
            heaparray[answer[i][1]][0] = i

        temp = answer[start][1]
        answer[start][1] = 1
        answer[0][1] = temp
        heaparray[start + 1][1] = 0
        heaparray[start + 1], heaparray[1] = heaparray[1], heaparray[start + 1]

        length = len(heaparray)

        for i in range(max_vertex + 1):
            # record length
            length1 = length
            # serve #update
            heaparray, answer, length = serve(heaparray, answer, length)
            # sink #update
            heaparray, answer = fall(heaparray, 1, answer, length)
            # vertex's edges to examine
            for edges in answer[heaparray[length1 - 1][0]][2]:
                # relax routine #update pred
                if heaparray[answer[edges[0]][1]][1] > edges[1] + heaparray[length1 - 1][1]:
                    heaparray[answer[edges[0]][1]][1] = edges[1] + heaparray[length1 - 1][1]
                    # update pred
                    answer[edges[0]][0] = heaparray[length1 - 1][0]
                    # rise #update
                    heaparray, answer = rise(heaparray, answer[edges[0]][1], answer)

        return heaparray, answer

    def find_shortest(answer, answer2, finalheap, finalheap2, passenger, start, end):

        """
        description: if pooling really reduce the path find which location is the best location to pick up passenger
        else just go all the way alone.

        approach: assume that the shortest weight is normal lane(assign to shortest weight),set pool to false,
        loop the passenger list,
        for each passenger check if the weight of using normal lane from start to the location of that passenger
        + the weight of using carpool lane from end to the location of that passenger is smaller than
        from start to end using normal lane , if smaller then set pool to true and assign the location of that
        passenger to the shortest and update the shortest weight to the weight of using normal lane from start to the
        location of that passenger + the weight of using carpool lane from end to the location of that passenger
        , repeat the comparing process until no passenger left. After the comparison shortest will be the smallest
        combination of weight of all passengers. Last, if pool true, the final answer will be the path from start to
        the smallest using normal lane then carpool lane from smallest to the end. If pool false, then the path is
        just from start to end using normal lane.
        Use recreate path function to get the correct path.

        input : start(an integer), end(an integer) ,passenger(a list of integer), two heap array()
        , two 2D list  with three columns, first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective index in heap and respective edges

        answer: [['undefined', 5, [[3, 5], [1, 10]]], [0, 2, [[4, 30]]], [3, 3, [[4, 30], [0, 2]]], [0, 4, [[4, 35], [2, 2]]], [2, 1, [[0, 15]]]] [[3, 3, [[4, 10], [2, 2]]], [4, 2, [[0, 10]]], [0, 1, [[3, 2]]], [4, 4, [[0, 3]]]
        answer2: ['undefined', 5, [[3, 15], [2, 25], [1, 20]]]]
        finalheap:[None, [4, 37], [1, 10], [2, 7], [3, 5], [0, 0]]
        finalheap2:[None, [2, 20], [1, 20], [0, 18], [3, 15], [4, 0]] [2, 1]
        start:0
        end:4

        output: a list of integer begins with the start number and ends with the end number, representing a path
        [0,3,2,0,3,4]

        time complexity :
        Best:O(|L|) no passenger
        Worst:O(|L|)
        Space complexity:
        Input: O(|L|+|R|)
        aux space complexity: O(|L|)
        """
        finalanswerwithoutpool = finalheap[answer[end][1]][1]

        pool = False
        for i in passenger:
            if finalheap[answer[i][1]][1] + finalheap2[answer2[i][1]][1] < finalanswerwithoutpool:
                pool = True
                shortest = i
                finalanswerwithoutpool = finalheap[answer[i][1]][1] + finalheap2[answer2[i][1]][1]
        print(finalanswerwithoutpool)
        if pool:
            final = recreate_path(answer2, end, shortest)
            final.reverse()
            final.pop(0)
            return recreate_path(answer, start, shortest) + final
        else:
            return recreate_path(answer, start, end)

    def recreate_path(answer, start, end):
        """
        description: create a path using the answer list starting from start to end

        approach:initialize an empty list , go into a while loop if start not equal to end, then append it to the
        list and find the predecessor of end. When end is equal to start then exit loop and append the start vertex.
        But the path is in reverse order so use built-in function reverse() to reverse the list and this will be the
        answer.

        input : start(an integer), end(an integer) , an 2D list  with three columns( first column is used to store
        predecessor, second is used to store the index of where it is located in the heap ,
        third is used to store the edges weight for each vertex and also which vertex the edge goes to)
        and max vertex number of row with each row represent a vertex and also their respective predecessor,
        respective index in heap and respective edges
        answer:[['undefined', 5, [[3, 5], [1, 10]]], [0, 2, [[4, 30]]], [3, 3, [[4, 30], [0, 2]]], [0, 4, [[4, 35], [2, 2]]], [2, 1, [[0, 15]]]]
        start:0
        end:2

        output: a list of integer begins with the start number and ends with the end number, representing a path
        [0, 3, 2, 0, 3, 4]

        Time complexity:
        Best: O(1) when start is end
        Worst:O(|L|)
        Space complexity:
        Input: O(|L|)
        aux space complexity: O(|L|)
        """

        path = []
        while end != start:
            path.append(end)
            end = answer[end][0]
        path.append(start)
        path.reverse()
        return path

    max_vertex_count = find_max_vertex(roads)
    answer1 = initialize_answer_list(max_vertex_count, roads)
    finalheap, answer1 = dijkstra(start, max_vertex_count, answer1)
    answer3 = initialise_reverse_pool_graph(max_vertex_count, roads)
    finalheap2, answer21 = dijkstra(end, max_vertex_count, answer3)

    return find_shortest(answer1, answer21, finalheap, finalheap2, passengers, start, end)


#question  2

def select_sections(occupancy_probability):
    """

    Description: find a path from bottom to top ,one block from each row,for each adjacent row the chosen block must
    be adjacent vertically or diagonally, and the total occupancy of the path must be the smallest in the whole
    occupancy_probability list

    Approach : initialize a backtrack array same dimension with occupancy_probability, and for each position , store
    the coordinate.
    Starting from the last second row of occupancy_probability, the optimal substructure is the smallest
    of below the current position and below left and below right . Add the value at that position with the smallest,
    and record in the backtrack where it comes from. After the occupancy_probability is filled with new values, the
    value of the smallest occupancy is the smallest value at the first row. The coordinate value can be retrieved
    using the backtrack array starting from top row. The first column value in the backtrack to start with
    is same as the column value that has the smallest value in the first row of smallest occupancy. Backtrack starts
    from top row until the last row. For each row append the coordinate as a tuple to the list that is located in the
    second position of the answer array.

    input : 2D array [
    [31, 54, 94, 34, 12],
    [26, 25, 24, 16, 87],
    [39, 74, 50, 13, 82],
    [42, 20, 81, 21, 52],
    [30, 43, 19, 5, 47],
    [37, 59, 70, 28, 15],
    [ 2, 16, 14, 57, 49],
    [22, 38, 9, 19, 99]]

    output : a list, first position is an integer , and second position is a list of tuple
    represents the coordinate in the occupancy_probability from top to bottom.
    [118, [(0, 4), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 2), (7, 2)]]

    time complexity :
    Best: O(MN)
    Worst:O(MN)
    Space complexity:
    Input: O(MN)
    aux space complexity: O(MN)

    """
    backtrack = [[[j,i] for i in range(len(occupancy_probability[0]))] for j in range(len(occupancy_probability))]
    for i in range(len(occupancy_probability)-2,-1,-1):
        for j in range(len(occupancy_probability[i])):
            if j ==0 and j == len(occupancy_probability[i]) - 1:
                occupancy_probability[i][j] += occupancy_probability[i+1][j]
                backtrack[i][j].append(2)
            elif j == 0:
                occupancy_probability[i][j] += min(occupancy_probability[i+1][j],occupancy_probability[i+1][j+1])
                if occupancy_probability[i+1][j] > occupancy_probability[i+1][j+1]:
                    backtrack[i][j].append(3)
                else:
                    backtrack[i][j].append(2)
            elif j == len(occupancy_probability[i]) - 1:
                occupancy_probability[i][j] += min(occupancy_probability[i+1][j],occupancy_probability[i+1][j-1])
                if occupancy_probability[i+1][j] > occupancy_probability[i+1][j-1]:
                    backtrack[i][j].append(1)
                else:
                    backtrack[i][j].append(2)
            else:
                occupancy_probability[i][j] += min(occupancy_probability[i+1][j],occupancy_probability[i+1][j-1],occupancy_probability[i+1][j+1])
                if occupancy_probability[i+1][j] > occupancy_probability[i+1][j-1] and occupancy_probability[i+1][j+1] > occupancy_probability[i+1][j-1]:
                    backtrack[i][j].append(1)
                elif occupancy_probability[i+1][j] > occupancy_probability[i+1][j+1] and occupancy_probability[i+1][j-1] > occupancy_probability[i+1][j+1]:
                    backtrack[i][j].append(3)
                elif occupancy_probability[i+1][j+1] > occupancy_probability[i+1][j] and occupancy_probability[i+1][j-1] > occupancy_probability[i+1][j]:
                    backtrack[i][j].append(2)
                elif occupancy_probability[i+1][j+1] == occupancy_probability[i+1][j] or occupancy_probability[i+1][j-1] == occupancy_probability[i+1][j]:
                    backtrack[i][j].append(2)
                elif occupancy_probability[i+1][j+1] == occupancy_probability[i+1][j]:
                    backtrack[i][j].append(1)
    answer = [0,[]]
    smallest = [occupancy_probability[0][0], 0]
    for i in range(len(occupancy_probability[0])):
        if occupancy_probability[0][i] < smallest[0]:
            smallest[0] = occupancy_probability[0][i]
            smallest[1] = i
    answer[0] = smallest[0]
    answer[1].append((backtrack[0][smallest[1]][0], backtrack[0][smallest[1]][1]))
    direction = backtrack[0][smallest[1]][2]
    column = backtrack[0][smallest[1]][1]
    for i in range(1,len(backtrack)-1):
        if direction == 1:
            answer[1].append((i,backtrack[i][column-1][1]))
            direction = backtrack[i][column-1][2]
            column = backtrack[i][column-1][1]
        elif direction == 2:
            answer[1].append((i,backtrack[i][column][1]))
            direction = backtrack[i][column][2]
            column = backtrack[i][column][1]
        elif direction == 3:
            answer[1].append((i,backtrack[i][column+1][1]))
            direction = backtrack[i][column+1][2]
            column = backtrack[i][column+1][1]
    if direction == 1:
        answer[1].append((len(backtrack)-1, backtrack[len(backtrack)-1][column - 1][1]))
    elif direction == 2:
        answer[1].append((len(backtrack) - 1, backtrack[len(backtrack) - 1][column ][1]))
    elif direction == 3:
        answer[1].append((len(backtrack) - 1, backtrack[len(backtrack) - 1][column + 1][1]))
    return answer



if __name__ == "__main__":
    # Example
    start = 0
    end = 4
    # The locations where there are potential passengers
    passengers = [2, 1]
    # The roads represented as a list of tuple
    roads = [(0, 3, 5, 3), (3, 4, 35, 15), (3, 2, 2, 2), (4, 0, 15, 10),
    (2, 4, 30, 25), (2, 0, 2, 2), (0, 1, 10, 10), (1, 4, 30, 20)]
    # Your function should return the optimal route (which takes 27 minutes).
    print(optimalRoute(start, end, passengers, roads))
    print(optimalRoute(0, 4, [3, 5, 11],
                       [(6, 4, 6, 1), (0, 1, 1, 1), (1, 2, 1, 1), (1, 6, 1, 1), (2, 3, 1, 1), (3, 7, 1, 1),
                        (0, 5, 1, 1), (7, 8, 1, 1), (8, 1, 1, 1), (1, 9, 1, 1), (9, 11, 1, 1), (11, 10, 1, 1),
                        (10, 1, 1, 1)]))
    print(optimalRoute(0, 4, [], [(6, 4, 6, 1), (0, 1, 1, 1), (1, 2, 1, 1), (1, 6, 1, 1), (2, 3, 1, 1), (3, 7, 1, 1),
                                  (0, 5, 1, 1), (7, 8, 1, 1), (8, 1, 1, 1), (1, 9, 1, 1), (9, 11, 1, 1), (11, 10, 1, 1),
                                  (10, 1, 1, 1)]))
    print(optimalRoute(0, 4, [3, 5, 11],
                       [(6, 4, 4, 1), (0, 1, 1, 1), (1, 2, 1, 1), (1, 6, 1, 1), (2, 3, 1, 1), (3, 7, 1, 1),
                        (0, 5, 1, 1), (7, 8, 1, 1), (8, 1, 1, 1), (1, 9, 1, 1), (9, 11, 1, 1), (11, 10, 1, 1),
                        (10, 1, 1, 1)]))

    # Example
    occupancy_probability = [
    [31, 54, 94, 34, 12],
    [26, 25, 24, 16, 87],
    [39, 74, 50, 13, 82],
    [42, 20, 81, 21, 52],
    [30, 43, 19, 5, 47],
    [37, 59, 70, 28, 15],
    [ 2, 16, 14, 57, 49],
    [22, 38, 9, 19, 99]]
    print(select_sections(occupancy_probability))

    start = 0
    end = 3
    passengers = [1]
    roads = [
        (0, 1, 1, 1),
        (0, 2, 2, 1),
        (1, 2, 1, 1),
        (2, 0, 2, 1),
        (0, 3, 1000, 500)
    ]
    print(optimalRoute(start, end, passengers, roads))

    start = 0
    end = 4
    passengers = [1, 3]
    roads = [
        (0, 1, 6, 5),
        (0, 2, 5, 1),
        (0, 4, 20, 18),
        (1, 4, 4, 4),
        (2, 3, 2, 2),
        (3, 4, 20, 2)
    ]

    print(optimalRoute(start, end, passengers, roads))

    occupancy_probability = [
        [0, 76, 38, 2],
        [1, 94, 54, 1],
        [2, 86, 86, 99],
        [3, 0, 0, 0],
        [99, 99, 99, 0]
    ]

    print(select_sections(occupancy_probability))

    start = 2
    end = 6
    passengers = [0, 3, 5]
    roads = [
        (0, 1, 10, 8),
        (2, 6, 5, 5),
        (1, 2, 11, 9),
        (2, 3, 12, 10),
        (3, 4, 15, 12),
        (4, 5, 18, 10),
        (5, 6, 20, 13),
        (6, 7, 30, 15)
    ]

    print(optimalRoute(start, end, passengers, roads))

    occupancy_probability = [
        [19, 76, 38, 22, 0],
        [56, 20, 54, 0, 34],
        [71, 86, 0, 99, 89],
        [81, 0, 82, 22, 45],
        [0, 22, 22, 93, 23]
    ]
    expected = [0, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]]
    print(select_sections(occupancy_probability))

    occupancy_probability = [
        [19, 76, 38, 22],
        [56, 20, 54, 68],
        [71, 86, 15, 99],
        [81, 82, 82, 22],
        [36, 22, 22, 93]
    ]
    expected = [98, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 2)]]
    print(select_sections(occupancy_probability))

    start = 0
    end = 5
    passengers = [3, 4, 2]
    roads = [
        (0, 1, 100, 95),
        (0, 2, 2, 2),
        (0, 3, 1, 1),
        (0, 4, 3, 3),
        (1, 5, 5, 3),
        (2, 5, 1000, 955),
        (3, 5, 1000, 955),
        (4, 5, 1000, 955),
    ]

    print(optimalRoute(start, end, passengers, roads))

    occupancy_probability = [
                        [57, 76, 38, 22],
                        [56, 94, 54, 68],
                        [71, 86, 86, 99],
                        [81,  0,  0, 60],
                        [36, 22, 43, 93]
                        ]
    # Getting one of the following results should be fine
    expec_res_1 = [184, [(0, 3), (1, 2), (2, 1), (3, 1), (4, 1)]]
    expec_res_2 = [184, [(0, 3), (1, 2), (2, 2), (3, 2), (4, 1)]]
    expec_res_3 = [184, [(0, 3), (1, 2), (2, 1), (3, 2), (4, 1)]]
    expec_res_4 = [184, [(0, 3), (1, 2), (2, 2), (3, 1), (4, 1)]]
    print(select_sections(occupancy_probability))

    start = 54
    end = 62
    passengers = [29, 63, 22, 18, 2, 23, 48, 41, 15, 31, 13, 4, 24, 16, 27, 17, 50, 67, 37, 58, 28, 64, 35, 10, 68, 38,
                  59, 26, 69, 43, 44, 30, 46, 7]
    roads = [
        (31, 45, 23, 12), (48, 3, 14, 7), (58, 50, 25, 10),
        (5, 3, 26, 23), (12, 32, 29, 3), (65, 4, 16, 16),
        (13, 46, 14, 13), (63, 29, 10, 2), (19, 56, 30, 19),
        (52, 47, 19, 12), (47, 52, 12, 8), (30, 42, 22, 19),
        (46, 60, 17, 17), (54, 22, 8, 7), (19, 8, 23, 10),
        (33, 51, 22, 5), (12, 17, 20, 5), (64, 62, 22, 18),
        (66, 25, 28, 10), (48, 19, 23, 8), (36, 13, 22, 19),
        (26, 48, 6, 3), (31, 30, 26, 9), (24, 29, 22, 11),
        (23, 36, 27, 11), (59, 37, 16, 10), (60, 44, 12, 8),
        (40, 7, 18, 1), (22, 3, 13, 12), (36, 35, 15, 15),
        (43, 2, 23, 6), (29, 27, 27, 6), (34, 0, 17, 4),
        (52, 50, 13, 4), (27, 23, 15, 1), (15, 10, 7, 6),
        (36, 65, 23, 1), (41, 64, 27, 8), (45, 34, 12, 1),
        (51, 24, 12, 10), (16, 12, 29, 7), (9, 67, 25, 24),
        (49, 38, 16, 4), (38, 7, 10, 1), (50, 13, 23, 16),
        (5, 33, 27, 10), (23, 42, 29, 15), (9, 2, 13, 7),
        (59, 52, 23, 17), (59, 54, 8, 6), (1, 8, 10, 8),
        (33, 30, 15, 2), (6, 26, 18, 6), (39, 57, 13, 12),
        (54, 26, 13, 9), (57, 41, 4, 4), (37, 66, 16, 12),
        (36, 9, 12, 5), (2, 68, 7, 3), (69, 28, 18, 2),
        (44, 1, 14, 3), (48, 9, 6, 4), (17, 38, 13, 1),
        (61, 49, 4, 4), (9, 10, 6, 3), (46, 37, 21, 8),
        (23, 53, 21, 8), (7, 24, 28, 26), (62, 20, 22, 7),
        (1, 18, 10, 1), (7, 41, 9, 1), (13, 18, 6, 4),
        (25, 21, 21, 3), (1, 61, 21, 16), (49, 40, 13, 5),
        (19, 25, 11, 10), (62, 50, 5, 5), (33, 46, 10, 9),
        (28, 25, 14, 6), (56, 51, 6, 4), (18, 19, 15, 1),
        (30, 9, 23, 13), (60, 21, 23, 7), (52, 37, 16, 6),
        (50, 42, 11, 4)
    ]
    # Optimal route is 198 mins
    result = [54, 26, 48, 19, 56, 51, 24, 29, 27, 23, 36, 13, 46, 60, 44, 1, 61, 49, 38, 7, 41, 64, 62]
    print(optimalRoute(start, end, passengers, roads))

    start = 4
    end = 0
    passengers = []
    roads = [
        (0, 1, 28, 22),
        (3, 2, 21, 10),
        (4, 1, 26, 20),
        (1, 3, 5, 3),
        (0, 4, 24, 13),
        (2, 1, 26, 15),
        (2, 0, 26, 26)
    ]
    result = [4, 1, 3, 2, 0]  # Optimal route is 78 mins

    print(optimalRoute(start, end, passengers, roads))

    start = 1
    end = 2
    passengers = []
    roads = [
        (3, 4, 24, 10),
        (4, 1, 16, 6),
        (0, 2, 28, 14),
        (1, 3, 27, 12),
        (4, 0, 5, 4),
        (2, 4, 15, 9)
    ]
    result = [1, 3, 4, 0, 2]

    print(optimalRoute(start, end, passengers, roads))

    start = 4
    end = 9
    passengers = [2, 6, 0]
    roads = [
        (4, 6, 30, 18),
        (3, 1, 8, 1),
        (9, 1, 9, 5),
        (1, 9, 30, 2),
        (8, 5, 12, 12),
        (8, 9, 8, 6),
        (1, 8, 25, 2),
        (2, 4, 4, 2),
        (6, 0, 25, 5),
        (4, 3, 6, 6),
        (1, 2, 15, 7)
    ]
    result = [4, 3, 1, 2, 4, 3, 1, 9]

    print(optimalRoute(start, end, passengers, roads))

    start = 2
    end = 5
    passengers = [3]
    roads = [
        (6, 2, 22, 6),
        (3, 6, 4, 3),
        (0, 7, 8, 3),
        (5, 0, 9, 6),
        (5, 4, 6, 5),
        (4, 3, 24, 2),
        (1, 2, 26, 23),
        (7, 4, 26, 8),
        (7, 3, 12, 5),
        (4, 5, 10, 3),
        (2, 0, 14, 1),
        (5, 7, 6, 6)
    ]
    res_1 = [2, 0, 7, 3, 6, 2, 0, 7, 4, 5]  # Both results should yield 58 mins
    res_2 = [2, 0, 7, 4, 5]

    print(optimalRoute(start, end, passengers, roads))

    occupancy_probability = [[57, 11, 14, 19, 63, 50, 61, 50, 40, 0, 46],
                             [2, 42, 98, 84, 56, 5, 33, 87, 60, 19, 91],
                             [84, 23, 37, 36, 38, 89, 72, 13, 48, 88, 46],
                             [36, 91, 11, 1, 5, 3, 38, 58, 37, 24, 39],
                             [52, 74, 67, 41, 76, 29, 38, 61, 74, 42, 10],
                             [46, 25, 38, 16, 50, 7, 99, 34, 79, 83, 19],
                             [76, 68, 74, 48, 38, 11, 46, 25, 31, 10, 73],
                             [99, 4, 65, 22, 12, 47, 18, 45, 63, 85, 17],
                             [35, 86, 91, 69, 50, 20, 72, 34, 24, 69, 100],
                             [20, 7, 63, 92, 33, 81, 22, 79, 85, 39, 21],
                             [98, 22, 37, 54, 28, 89, 50, 95, 59, 17, 88],
                             [13, 86, 98, 26, 30, 3, 93, 97, 59, 1, 23],
                             [39, 62, 48, 37, 35, 84, 87, 91, 63, 66, 21]]
    expected = [273, [(0, 1), (1, 0), (2, 1), (3, 2), (4, 3), (5, 3), (6, 4), (7, 4), (8, 5), (9, 4), (10, 4), (11, 5),
                      (12, 4)]]
    print(select_sections(occupancy_probability))

    occupancy_probability = [[15], [84], [82], [79], [77], [55], [69], [13], [21], [33], [85], [100], [67], [93], [3],
                             [26], [29], [89], [36], [100], [68], [34], [87], [55], [47], [44], [64], [84], [41], [97]]
    expected = [1777, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0),
                       (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0),
                       (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0)]]

    print(select_sections(occupancy_probability))

    occupancy_probability = [[66], [66]]
    expected = [132, [(0, 0), (1, 0)]]

    print(select_sections(occupancy_probability))

    occupancy_probability = [[32, 86, 95, 15, 68, 90],
                             [91, 88, 96, 51, 64, 66],
                             [17, 70, 13, 9, 90, 17],
                             [17, 15, 38, 12, 53, 17],
                             [29, 6, 18, 27, 66, 48],
                             [74, 43, 76, 44, 3, 1],
                             [89, 1, 8, 24, 45, 62],
                             [3, 98, 99, 89, 6, 66]]
    expected_1 = [147, [(0, 3), (1, 3), (2, 2), (3, 1), (4, 1), (5, 1), (6, 1), (7, 0)]]
    expected_2 = [147, [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 4), (6, 3), (7, 4)]]

    print(select_sections(occupancy_probability))

    start = 6
    end = 7
    passengers = [4, 2, 9]
    roads = [
        (9, 0, 7, 4),
        (7, 4, 3, 1),
        (8, 7, 6, 1),
        (3, 5, 1, 1),
        (2, 9, 6, 4),
        (6, 4, 5, 4),
        (2, 4, 6, 2),
        (7, 3, 8, 7),
        (0, 9, 1, 1),
        (2, 3, 5, 5),
        (5, 3, 6, 6),
        (1, 9, 6, 5),
        (0, 7, 5, 5),
        (1, 8, 2, 1),
        (6, 9, 6, 5),
        (2, 1, 2, 2)
    ]
    result = [6, 9, 0, 7]

    print(optimalRoute(start, end, passengers, roads))
    start = 0
    end = 5
    passengers = [2, 1]
    roads = [
        (4, 5, 200, 2),
        (0, 2, 2, 2),
        (1, 3, 10, 5),
        (3, 5, 50, 50),
        (2, 4, 10, 10),
        (0, 1, 1, 1)
    ]
    result = [0, 2, 4, 5]

    print(optimalRoute(start, end, passengers, roads))

    start = 0
    end = 4
    passengers = [2, 1]
    roads = [
        (0, 4, 30, 5),
        (0, 1, 5, 4),
        (1, 3, 3, 2),
        (3, 2, 2, 1),
        (2, 0, 1, 1)]
    result = [0, 1, 3, 2, 0, 4]

    print(optimalRoute(start, end, passengers, roads))

