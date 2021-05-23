FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
EXPOSE 8000
COPY . /usr/src/app/
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
COPY . .
RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
