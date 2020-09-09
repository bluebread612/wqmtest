from py2neo import Graph
import json
graph = Graph(password='123456')


def search_action(number, action_type, limit=3):
    data = []

    if action_type == 'communicate':
        data = search_communicate_action(number, limit)
    elif action_type == 'travel':
        data = search_travel_action(number, limit)
    elif action_type == 'lodging':
        data = search_lodging_action(number, limit)
    elif action_type == 'other':
        data = search_other_action(number, limit)
    else:
        pass

    return json.dumps(data, ensure_ascii=False, indent=1)


def search_communicate_action(number, limit=3):
    cql = f'match p=(:Number {{number:"{number}"}})-[:CALL]->()-[]->() \
                return p limit {limit*2}'
    res = []
    records = graph.run(cql)
    # print(records)
    i = 0
    for record in records:
        if i % 2 == 0:
            res.append({'source': record[0].nodes[0]['number'],
                        'target': record[0].nodes[1]['time'],
                        'type': 'licensing'})
        if record[0].nodes[2]['number'] is not None:
            res.append({'source': record[0].nodes[1]['time'],
                        'target': record[0].nodes[2]['number'],
                        'type': 'suit'})
        else:
            print(record[0].nodes[2])
            res.append({'source': record[0].nodes[1]['time'],
                        'target': record[0].nodes[2]['address'],
                        'type': 'resolved'})
        i += 1

    return res


def search_travel_action(number, limit=3):
    cql = f'match p=(:Number {{number:"{number}"}})-[:TRAVEL]->() \
                return p limit {limit*2}'
    res = []
    records = graph.run(cql)
    for record in records:
        print(record)
        res.append({'source': record[0].nodes[0]['number'],
                    'target': record[0].nodes[1]['endTime'],
                    'type': 'licensing'})
        res.append({'source': record[0].nodes[1]['endTime'],
                    'target': "起点：" + record[0].nodes[1]['startPlace'],
                    'type': 'suit'})
        res.append({'source': record[0].nodes[1]['endTime'],
                    'target': "终点：" + record[0].nodes[1]['endPlace'],
                    'type': 'suit'})
        res.append({'source': record[0].nodes[1]['endTime'],
                    'target': "方式：" + record[0].nodes[1]['vehicle'],
                    'type': 'suit'})

    return res


def search_lodging_action(number, limit=3):
    cql = f'match p=(:Number {{number:"{number}"}})-[:LODGING]->()-[]->() \
                return p limit {limit*2}'
    res = []
    records = graph.run(cql)
    for record in records:
        print(record)
        res.append({'source': record[0].nodes[0]['number'],
                    'target': record[0].nodes[1]['time'],
                    'type': 'licensing'})
        res.append({'source': record[0].nodes[1]['time'],
                    'target': record[0].nodes[1]['hotel'],
                    'type': 'suit'})
        res.append({'source': record[0].nodes[1]['time'],
                    'target': record[0].nodes[2]['address'],
                    'type': 'suit'})

    return res


def search_other_action(number, limit=3):
    cql = f'match p=(:Number {{number:"{number}"}})-[:OTHER]->()-[]->() \
                return p limit {limit}'
    res = []
    records = graph.run(cql)
    for record in records:
        print(record)
        res.append({'source': record[0].nodes[0]['number'],
                    'target': record[0].nodes[1]['time'],
                    'type': 'licensing'})
        res.append({'source': record[0].nodes[1]['time'],
                    'target': record[0].nodes[2]['address'],
                    'type': 'suit'})

    return res


if __name__ == '__main__':
    # data = search_lodging_action("13501854608", 3)
    # file_path = './json_data/lodging.json'
    # file = open(file_path, 'w', encoding='UTF-8')
    # print(json.dumps(data, ensure_ascii=False, indent=1))
    # file.write(json.dumps(data, ensure_ascii=False, indent=1))
    json_data = search_action("13501854608", 'other', 3)
    # print(len(json_data))
    print(json_data)
