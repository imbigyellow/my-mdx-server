from flask import Flask, send_from_directory, jsonify
from mdict_query.mdict_query import IndexBuilder
import os

# 词典文件放在 /data 目录；如果你想挂卷，就改成环境变量读取
DICT_PATH = "/data/longman6.mdx"

idx = IndexBuilder(DICT_PATH)   # 初始化索引，容器启动时一次性加载到内存

app = Flask(__name__, static_folder="static")

@app.route("/<word>")
def lookup_html(word):
    """返回原始 HTML（最简单直接）"""
    html = "".join(idx.mdx_lookup(word))
    return html or f"<h3>‘{word}’ not found.</h3>"

@app.route("/api/<word>")
def lookup_json(word):
    """给脚本 / 前端调用的 JSON 版本"""
    html = "".join(idx.mdx_lookup(word))
    return jsonify({"word": word, "html": html})

# 可选：让浏览器能加载静态 CSS/JS（/static/...）
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    # host=0.0.0.0 让容器外部能访问，端口随意（Dockerfile 暴露同一个）
    app.run(host="0.0.0.0", port=8000)
