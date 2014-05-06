import json
from flask import Flask, request
app = Flask(__name__)

@app.route('/search')
def search():
    expression = request.args.get('expression', None)
    if expression is not None:
        with open("casts.json", "r") as infile:
            candidates = json.loads(infile.read())
            return json.dumps({
                k: v
                for k, v in candidates.items()
                if expression.lower() in k.lower()
                or expression.lower() in v['description'].lower()
            })
    else:
        return json.dumps({})

@app.route('/get')
def get():
    name = request.args.get('name', None)
    if name is not None:
        with open("casts.json") as infile:
            try:
                cast = json.loads(infile.read())[name]
            except KeyError:
                return json.dumps({})
            else:
                return json.dumps(cast)
    else:
        return json.dumps({})


if __name__=='__main__':
    app.run()