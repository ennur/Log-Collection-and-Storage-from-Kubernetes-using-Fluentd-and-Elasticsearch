from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from flask import Flask,jsonify

app=Flask(__name__)

es = Elasticsearch(host='192.168.2.27', port=9200)

def get_data_from_elastic(key,value):
    # query: The elasticsearch query.
    query = {
        "query": {
            "match": {
             key: value
            }
        }
    }

    rel = scan(client=es,             
               query=query,                                     
               scroll='1m',
               index='fluentd*',
               raise_on_error=True,
               preserve_order=False,
               clear_scroll=True)
    result = list(rel)
    temp = []
    for hit in result:
        temp.append(hit['_source'])

    return temp

@app.route("/<key>/<value>",methods=["GET","POST"])
def search(key,value):
  df = get_data_from_elastic(str(key),str(value))
  return jsonify(df)


if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")
#print(df.head())