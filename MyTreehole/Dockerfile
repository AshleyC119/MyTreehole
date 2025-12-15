FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
# 注意：这里的 MyTreehole 指的就是与 manage.py 同级的那个文件夹名
CMD ["gunicorn", "MyTreehole.wsgi:application", "--bind", "0.0.0.0:8000"]