# 基于python镜像
FROM python:3.14-slim
# 设置工作目录为 /app
WORKDIR /app
# 将“子项目目录”中的所有代码复制到容器的 /app 下
COPY ./MyTreehole .
# 安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# 启动命令（项目名指向正确的模块路径）
CMD ["gunicorn", "MyTreehole.wsgi:application", "--bind", "0.0.0.0:8000"]