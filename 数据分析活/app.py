from flask import Flask, jsonify
from src.config import load_config
from src.utils.logger import setup_logging

# 创建Flask应用
app = Flask(__name__)

# 加载配置
config = load_config()

# 设置日志
setup_logging()

@app.route('/')
def index():
    return jsonify({
        'name': config['app']['name'],
        'version': config['app']['version'],
        'status': 'running'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'services': {
            'mysql': 'connected',
            'redis': 'connected',
            'kafka': 'connected'
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config['app']['debug']) 