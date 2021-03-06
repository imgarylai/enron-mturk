import elit

filename = "tsv/maildir/arnold-j/deleted_items/176./2.tsv"
reader = elit.TSVReader(1, 2, 3, 4, 5, 6, 7, 8)
reader.open(filename)


def group(graphs):
    start = None
    result = []
    for i, graph in enumerate(graphs):
        if graph.nament.startswith('O'):
            if start is not None:
                nament = graph.nament.split("-")[1]
                word = " ".join([g.word for g in graphs.nodes[start:i+2]])
                result.append((word, False, nament))
                result.append((graph.word, graph.pos.startswith('PRP'),graph.nament))
                start = None
            else:
                result.append((graph.word, graph.pos.startswith('PRP'), graph.nament))
        elif graph.nament.startswith('B'):
            start = i+1
        elif graph.nament.startswith('U'):
            nament = graph.nament.split("-")[1]
            word = graph.word
            result.append((word, False, nament))
            if start is not None:
                result.append((graph.word, graph.pos.startswith('PRP'), graph.nament))
                start = None
        elif graph.nament.startswith('L'):
            nament = graph.nament.split("-")[1]
            word = " ".join([g.word for g in graphs.nodes[start:i+2]])
            result.append((word, False, nament))
            start = None
        else:
            continue
    return result


if __name__ == '__main__':
    arr = []
    for nodes in reader.next_all:
        arr.extend(group(nodes))

    print(arr)