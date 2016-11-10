import collections
import pickle
import csv


graph = collections.defaultdict(list)
# Initialize graph
with open('../paymo_input/batch_payment.csv', 'rU') as f:
    read = csv.reader(f)

    for row in read:   # go through each row and assign the items of each row as these names

        try:
            time = row[0].strip()
            id1 = row[1].strip()
            id2 = row[2].strip()
            amnt = row[3].strip()
            msg = row[4].strip()

            if id2 not in graph[id1]:  # this is to avoid addind duplicate keys
                graph[id1].append(id2)
                graph[id2].append(id1) # now adding the reverse to double link keys
            else:
                pass

        except IndexError:

            pass

# Save payment history graph to be loaded later. This way it doesn't have to be recreated each time.
pickle.dump(graph, open('../payment_graph.p', 'wb'))

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


            # write results to output file
            with open('../paymo_output/output1.txt', 'a') as output:

                if (id2 in graph[id1] ) and count !=0:
                    output.write('trusted')
                    output.write('\n')
                if (id2 not in graph[id1] ) and count !=0:
                    output.write('unverified')
                    output.write('\n')


        except IndexError:
            pass
        count += 1
