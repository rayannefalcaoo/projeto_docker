from flask import Flask, request, jsonify, abort, Response
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://user-service:8001"
ORDER_SERVICE_URL = "http://order-service:8002"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):

    if path.startswith('users'):
        target_url = USER_SERVICE_URL + '/' + path
    
    elif path.startswith('orders'):
        target_url = ORDER_SERVICE_URL + '/' + path
    
    else:
        return jsonify({"message": "Rota desconhecida pelo Gateway."}), 404

    print(f"Proxying request to: {target_url}")
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)

    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Não foi possível conectar ao backend em {target_url}"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)