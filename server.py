from flask import Flask, request, jsonify
import numpy as np

app = Flask(name)

@app.route('/compute', methods=['POST'])
def compute():
    try:
        data = request.get_json()
        if 'a' not in data or 'b' not in data:
            return jsonify({'error': 'Invalid input data'}), 400

        a = np.array(data['a'], dtype=np.int32)
        b = np.array(data['b'], dtype=np.int32)
        c = a + b

        return jsonify({'result': c.tolist()})
    except Exception as e:
        print(f"Error during computation: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if name == 'main':
    print("Starting server...")
    app.run(host='0.0.0.0', port=80)