from pymongo import MongoClient

mc = MongoClient()
db = mc.test


CLO_PATH_PARSE = 'answer/%s/closeness.txt'
DEG_PATH_PARSE = 'answer/%s/degree.txt'

def write_answer_into_mongo(graph_name):
    collection = db[graph_name]
    with open(CLO_PATH_PARSE % graph_name) as clo:
        for line_id, line in enumerate(clo.readlines()):
            id_, clo = line.strip().split(' ')
            c = collection.find_one({'node_id': id_})
            if not c:
                c = {'node_id': id_, 'closeness': clo, 'order': line_id+1}
            else:
                c['closeness'] = clo
                c['order'] = line_id + 1
            collection.save(c)

    with open(DEG_PATH_PARSE % graph_name) as deg:
        for line in deg.readlines():
            id_, deg = line.strip().split(' ')
            c = collection.find_one({'node_id': id_})
            if not c:
                c = {'node_id': id_, 'degree': deg}
            else:
                c['degree'] = deg
            collection.save(c)


if __name__ == '__main__':
    import os
    graphs = os.listdir('answer')
    for g in graphs:
        write_answer_into_mongo(g)
        print "======%s has writed ======" % g
