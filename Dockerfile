FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    apt-get install make

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir /app
WORKDIR /app

RUN python3 -m pip install --upgrade cython
RUN pip3 install multidict
RUN pip3 install typing-extensions
RUN pip3 install attr
RUN pip3 install yarl
RUN pip3 install async_timeout
RUN pip3 install idna_ssl
RUN pip3 install -U kb-manager
RUN pip3 install charset_normalizer
RUN pip3 install aiosignal



COPY luci/requirements/common.txt .

RUN pip3 install -r common.txt
RUN python3 -m spacy download pt

COPY . .
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV NAME luci