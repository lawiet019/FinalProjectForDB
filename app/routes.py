#从app模块中即从__init__.py中导入创建的app应用
from app import app

#build the routers
@app.route('/')
@app.route('/index')
def index():
    return "Hello,World!"
