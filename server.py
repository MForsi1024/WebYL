from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get_test():
    word = request.args.get('word')
    return jsonify({'word': word})


@app.route('/post', methods=['POST'])
def post_test():
    data = request.get_json()
    return jsonify({'user': data})

if __name__ == '__main__':
    app.run(port=6767)
