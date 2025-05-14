# 选 slim 体积小、启动快
FROM python:3.11-slim

WORKDIR /app

# 系统级依赖（mdict-query 需要 lxml、python-magic）
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential libmagic1 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY server.py .
COPY static ./static        # 没用到可删
COPY data   /data

EXPOSE 8000
CMD ["python", "server.py"]
