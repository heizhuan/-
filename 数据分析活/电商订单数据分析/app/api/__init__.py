"""API模块

提供RESTful API接口，用于数据访问和系统交互。
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__) 