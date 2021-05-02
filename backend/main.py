"""
project: apiAutoTestWeb
file: main.py
author: zy7y
date: 2021/4/17
"""

from api import create_app

# uvicorn main:app --reload 启动
app = create_app()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
