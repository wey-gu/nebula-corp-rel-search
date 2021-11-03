import os

from flask import Flask, jsonify, request
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config


app = Flask(__name__)


@app.route("/")
def root():
    return "Hey There?"


@app.route("/api", methods=["POST"])
def api():
    request_data = request.get_json()
    entity = request_data.get("entity", "")
    if entity:
        resp = query_shareholding(entity)
        data = make_graph_response(resp)
    else:
        data = dict() # tbd
    return jsonify(data)


def parse_nebula_graphd_endpoint():
    ng_endpoints_str = os.environ.get(
        'NG_ENDPOINTS', '127.0.0.1:9669,').split(",")
    ng_endpoints = []
    for endpoint in ng_endpoints_str:
        if endpoint:
            parts = endpoint.split(":")  # we dont consider IPv6 now
            ng_endpoints.append((parts[0], int(parts[1])))
    return ng_endpoints

def query_shareholding(entity):
    query_string = (
        f"USE shareholding; "
        f"MATCH p=(v)-[e:hold_share|:is_branch_of|:reletive_with|:role_as*1..3]-(v2) "
        f"WHERE id(v) IN ['{ entity }'] RETURN p LIMIT 100"
    )
    session = connection_pool.get_session('root', 'nebula')
    resp = session.execute(query_string)
    return resp


def make_graph_response(resp) -> dict:
    nodes, relationships = list(), list()
    for row_index in range(resp.row_size()):
        path = resp.row_values(row_index)[0].as_path()
        _nodes = [
            {
                "id": node.get_id().as_string(), "tag": node.tags()[0],
                "name": str(node.properties(node.tags()[0]).get("name", ""))
                }
                for node in path.nodes()
        ]
        nodes.extend(_nodes)
        _relationships = [
            {
                "source": rel.start_vertex_id().as_string(),
                "target": rel.end_vertex_id().as_string(),
                "properties": str(rel.properties()),
                "edge": rel.edge_name()
                }
                for rel in path.relationships()
        ]
        relationships.extend(_relationships)
    return {"nodes": nodes, "relationships": relationships}


ng_config = Config()
ng_config.max_connection_pool_size = int(
    os.environ.get('NG_MAX_CONN_POOL_SIZE', 10))
ng_endpoints = parse_nebula_graphd_endpoint()
connection_pool = ConnectionPool()

if __name__ == "__main__":
    connection_pool.init(ng_endpoints, ng_config)
    try:
        app.run(host="0.0.0.0", port=5001)
    finally:
        connection_pool.close()
else:
    connection_pool.init(ng_endpoints, ng_config)
