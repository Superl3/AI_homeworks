fways = [[1,0], [0,1], [-1, 0], [0, -1]]
start = 3
end = 4
key = 6
path = 0
wall = 1

arr = []
visit = []
m = 0
n = 0
k = 0
def display(arr):
    for i in range(m):
        line = ''
        for j in arr[i]:
            if j >= 0:
                line += ' '
            line += str(j) + ' '
        print(line)
        #print('   '.join(str(e) for e in arr[i]))
    print()

def mod_result(target, dest):
    for i in range(m):
        for j in range(n):
            if dest[i][j] == 5:
                target[i][j] = 5
    return target

def findvalue(arr, value):
    for i in range(m):
        for j in range(n):
            if arr[i][j] == value:
                return i,j
    
def find_index(item, value):
    length = len(item)
    for i in range(length):
        if value <= item[i][2]:
            return i
    return length
    
def heuristic(x,y,end_x,end_y):
    return abs(end_x-x) + abs(end_y-y)

def backtrack(x,y,prev_data):
    data = prev_data
    depth = visit[x][y]
    path_check = False
    while not path_check:
        data[x][y] = 5
        path_check = False
        for i in range(4):
            X = x+fways[i][0]
            Y = y+fways[i][1]
            if X<0 or Y<0 or X>=m or Y>=n:
                continue
            if visit[X][Y] == depth-1:
                x = X
                y = Y
                depth -=1
                path_check = True
                break
    return data

def ids_search(depth, x, y, end_value, prev_data, depth_limit):
    global visit

    success = False
    data = prev_data
    if depth == depth_limit:
        if arr[x][y] != end_value:
            return False, []
        return True, backtrack(x,y,prev_data)
 
    for i in range(4):
        X = x+fways[i][0]
        Y = y+fways[i][1]
        if X>=m or X<0 or Y>=n or Y<0:
            continue
        
        if arr[X][Y] == wall:
            continue
        if visit[X][Y] > -5:
            continue

        visit[X][Y] = visit[x][y]+1
        success, data = ids_search(depth+1, X,Y, end_value, prev_data, depth_limit)
        if success == True:
            break
        visit[X][Y] = -5

    return success, data

def greedy_search(depth, x, y, end_x,end_y, prev_data):
    global visit

    success = False
    data = prev_data
    result = m*n

    item = []
    for i in range(4):
        X = x+fways[i][0]
        Y = y+fways[i][1]
        if X>=m or X<0 or Y>=n or Y<0:
            continue
        
        if arr[X][Y] == wall:
            continue
        if visit[X][Y] > -5:
            continue
        h = heuristic(X,Y,end_x,end_y)
        if h == 0:
            return True, backtrack(x,y,prev_data), depth

        item.insert(find_index(item,h),[X,Y,h])
        
    for X,Y,distance in item:
        visit[X][Y] = visit[x][y]+1
        success, data, result= greedy_search(depth+1, X,Y, end_x, end_y, prev_data)
        if success == True:
            break
        visit[X][Y] = -5
    return success, data, result

def ids():
    temp = [[-5]*n for i in range(m)]

    x,y = findvalue(arr,start)
    global visit
    visit = [[-5]*n for i in range(m)]
    visit[x][y] = 0
    found = False
    for length_key in range(1, n*m):
        found, result = ids_search(0,x,y,key,temp,length_key)
        if found == True: break
    temp = result
    x,y = findvalue(arr,key)
    visit = [[-5]*n for i in range(m)]
    visit[x][y] = length_key
    found = False
    for length_goal in range(1, n*m):
        found, result = ids_search(0,x,y,end,temp,length_goal)
        if found == True: break

    return mod_result(arr, result), length_goal+length_key

def greedy():
    global visit
    temp = [[-5]*n for i in range(m)]
    x,y = findvalue(arr,start)
    key_x,key_y = findvalue(arr,key)
    end_x,end_y = findvalue(arr,end)

    visit = [[-5]*n for i in range(m)]
    visit[x][y] = 0
    _, temp, length_key = greedy_search(0, x, y, key_x, key_y, temp)

    visit = [[-5]*n for i in range(m)]
    visit[x][y] = 0
    _, temp, length_end = greedy_search(0, key_x, key_y, end_x, end_y, temp)

    return mod_result(arr, temp), length_key + length_end

def bfs_search(start_x,start_y,end_x,end_y, prev_data, method):
    global visit
    visit = [[-5]*n for i in range(m)]
    visit[start_x][start_y] = 0

    queue = [[start_x,start_y,0]]
    while queue:
        x,y,_ = queue.pop(0)
        for i in range(4):
            X = x + fways[i][0]
            Y = y + fways[i][1]
            if X>=m or X<0 or Y>=n or Y<0:
                continue
            if arr[X][Y] == wall:
                continue
            if visit[X][Y] > -5:
                continue
            h = heuristic(X,Y, end_x, end_y)
            visit[X][Y] = visit[x][y] + 1
            if h == 0: # end of the line
                return backtrack(X, Y, prev_data), visit[X][Y]
            if method == 1:
                queue.append([X,Y,0])
            if method == 2: # astar
                distance = visit[X][Y] + h
                queue.insert(find_index(queue, distance),[X,Y,distance])
    return prev_data, -1 # failed
def do_bfs(method):
    start_x,start_y = findvalue(arr,start)
    key_x,key_y = findvalue(arr,key)
    end_x,end_y = findvalue(arr,end)

    temp = [[-5]*n for i in range(m)]
    temp, length_key = bfs_search(start_x,start_y,key_x,key_y,temp,method)
    temp, length_end = bfs_search(key_x,key_y,end_x,end_y,temp,method)
    return mod_result(arr, temp), length_key + length_end

def bfs():
    res, length = do_bfs(1)
    return res, length

def astar():
    res, length = do_bfs(2)
    return res, length

def input(path):
    arr = []
    file = open(path,'r')

    parameters = file.readline().split(' ')
    k = int(parameters[0])
    m = int(parameters[1])
    n = int(parameters[2])

    while True:
        line = file.readline()
        if line == '': break
        arr.append(list(map(int, line.split(' '))))
    return k,m,n,arr

k,m,n,arr = input('input.txt')
res, length = bfs()
print(length)
display(res)