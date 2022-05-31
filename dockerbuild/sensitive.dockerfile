# 基于一个python3.7基础镜像
FROM python:3.7-slim

# 安装pip包
RUN /usr/local/python3/bin/python3.7 -m pip install --upgrade pip \
	&& cd /root \
	&& pip install -r requirements.txt

WORKDIR /root/sensitive_data_analyzer_service
COPY . /root/sensitive_data_analyzer_service

ENTRYPOINT ["python3", "u", "/root/sensitive_data_analyzer_service/sensitive_data_analyzer_server.py"]