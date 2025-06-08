import os
import yaml
import logging
from flask import Flask, jsonify
from app.api import api_bp
from app.services import (
    DataCollectionService,
    DataStorageService,
    BatchProcessingService,
    StreamProcessingService,
    ComplexAnalysisService,
    VisualizationService,
    OptimizationService,
    IntegrationService,
    MLAnalysisService
)

# 加载配置
def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# 配置日志
def setup_logging(config):
    logging.basicConfig(
        level=config['logging']['level'],
        format=config['logging']['format'],
        filename=config['logging']['file']
    )
    return logging.getLogger(__name__)

# 初始化服务
def init_services(config):
    return {
        'data_collection': DataCollectionService(config),
        'data_storage': DataStorageService(config),
        'batch_processing': BatchProcessingService(config),
        'stream_processing': StreamProcessingService(config),
        'complex_analysis': ComplexAnalysisService(config),
        'visualization': VisualizationService(config),
        'optimization': OptimizationService(config),
        'integration': IntegrationService(config),
        'ml_analysis': MLAnalysisService(config)
    }

# 创建Flask应用
def create_app(config):
    app = Flask(__name__)
    app.config.from_mapping(config)
    
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

def main():
    # 加载配置
    config = load_config()
    
    # 设置日志
    logger = setup_logging(config)
    logger.info("Starting application...")
    
    try:
        # 初始化服务
        services = init_services(config)
        logger.info("Services initialized successfully")
        
        # 创建应用
        app = create_app(config)
        logger.info("Flask application created")
        
        # 启动应用
        host = config['api']['host']
        port = config['api']['port']
        debug = config['api']['debug']
        
        logger.info(f"Starting server on {host}:{port}")
        app.run(host=host, port=port, debug=debug)
        
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise

if __name__ == '__main__':
    main() 