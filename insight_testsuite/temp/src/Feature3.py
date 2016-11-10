import collections
import pickle
import csv

# Load payment graph
graph = pickle.load(open('/users/kevin/documents/New Insight Challenge/digital-wallet/payment_graph.p', 'rb'))

# Check new payments for existing match pairs
with open('../paymo_input/stream_payment.csv', 'rU') as f:
    read = csv.reader(f)
    count = 0
    for row in read:
        try:
            time = row[0].strip()
            id1 = row[1].strip()
            id2 = row[2].strip()
            amnt = row[3].strip()
            msg = row[4].strip()


            with open('../paymo_output/output3.txt', 'a') as output:
                for key in graph[id1]:

                    if ((id2 in graph[id1] or id1 in graph[id2]) or (id2 in graph[key] or key in graph[id2])) or (id2 in graph[graph.keys()[0]] or graph.keys()[0] in graph[id2]) and count != 0:
                        output.write('trusted')
                        output.write('\n')
                        break
                    else:
                        output.write('unverified')
                        output.write('\n')
                        break


        except IndexError:
            pass
        count += 1



# Other attempts using these functions had equally slow runtimes:
def search(id1, id2, graph, depth):
    if depth == 0:
        return False
    if (id2 in graph[id1]):
        return True
    if (id2 not in graph[id1]):
        keys = graph[id1]
        for key in keys:
            redo = search(key, id2, graph, depth-1)
            if redo == True:
                return redo
    return False



# Making a cache to store keys already looked at should have sped the process up in theory
cache = {}
def search(id1, id2, graph, depth, visited = []):
    if depth == 0:
        return False
    if id1 in visited:
        return False
    visited.append(id1)
    if (id2 in graph[id1] or id1 in graph[id2]):
        return True
    if (id2 not in graph[id1] or id1 not in graph[id2]):
        keys = graph[id1]
        for key in keys:
            ck = id1+":"+key
            cache[ck] = depth

            tk = key+":"+id2
            if tk in cache and cache[tk] - depth > 0:
                return True
            else:
                redo = search(key, id2, graph, depth-1, visited)
                if redo == True:
                    ck = key+":"+id2
                    cache[ck] = depth
                    return redo
    visited.remove(id1)
    return False



# Attempting to use the Breath-First Search algorithm did not speed the runtime up.
def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))
