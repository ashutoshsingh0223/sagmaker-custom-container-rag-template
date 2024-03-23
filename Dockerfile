FROM python:3.10.11

RUN ln -s /usr/bin/python3 /usr/bin/python & \
    ln -s /usr/bin/pip3 /usr/bin/pip

WORKDIR /src


ADD requirements.txt /src/requirements.txt

RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r /src/requirements.txt

RUN pip install unstructured[local-inference]==0.10.26 elasticsearch==7.13.0 jq==1.6.0
RUN pip install python-dotenv boto3

ENV PATH="/src:${PATH}"

COPY src /src
RUN chmod 755 /src

RUN mkdir -p /opt/ml/model
RUN chmod 755 /opt/ml/model

EXPOSE 8080
ENTRYPOINT ["python3", "endpoint.py"]
