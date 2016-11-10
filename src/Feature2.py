import collections
import pickle
import csv

# Load payment graph
graph = pickle.load(open('../payment_graph.p', 'rb'))

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



            with open('../paymo_output/output2.txt', 'a') as output:

                for key in graph[id1]:
                    if ((id2 in graph[id1] or id1 in graph[id2]) or (id2 in graph[key] or key in graph[id2])) and count != 0:
                        output.write('trusted')
                        output.write('\n')
                        break
                    if ((id2 not in graph[id1] or id1 not in graph[id2]) or (id2 not in graph[key] or key not in graph[id2])) and count != 0:
                        output.write('unverified')
                        output.write('\n')
                        break


        except IndexError:
            pass
        count += 1
