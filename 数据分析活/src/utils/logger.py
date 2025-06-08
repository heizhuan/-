import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from src.config import load_config

def setup_logging():
    """
    配置日志系统
    """
    config = load_config()
    log_config = config['logging']
    
    # 创建日志目录
    log_dir = os.path.dirname(log_config['file'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志处理器
    file_handler = RotatingFileHandler(
        log_config['file'],
        maxBytes=log_config['max_size'],
        backupCount=log_config['backup_count']
    )
    
    # 创建JSON格式化器
    formatter = jsonlogger.JsonFormatter(log_config['format'])
    file_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_config['level'])
    root_logger.addHandler(file_handler)
    
    # 配置控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler) 