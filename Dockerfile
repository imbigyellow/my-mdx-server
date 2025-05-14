FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝代码
COPY . /app

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["python", "mdx_server.py"]
