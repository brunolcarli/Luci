FROM python:3.7-alpine

RUN mkdir /luci
WORKDIR /luci

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk update


RUN apk add --no-cache --virtual .build-deps \
    python3-dev \
    build-base \
    linux-headers \
    gcc \
    libstdc++ \
    g++ \
    libc-dev \
    openssl-dev \
    libffi-dev \
    libxml2-dev \
    libwebp-dev \
    libgfortran \
    freetype

RUN apk add --no-cache jpeg-dev zlib-dev

RUN apk add --no-cache \
    build-base cairo-dev cairo cairo-tools \
    # pillow dependencies
    freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN apk add py2-numpy@community py2-scipy@community

RUN pip install cython===0.29.14

COPY luci/requirements/common.txt .

RUN python3 -m pip install -r common.txt

# Instala pacotes de linguagem para o NLTK
RUN python -c "import nltk;nltk.download('punkt')"
RUN python -c "import nltk;nltk.download('stopwords')"

# Instala pacotes de linguagem para o Spacy
RUN python -m spacy download en
RUN python -m spacy download pt
RUN python -m spacy download en_core_web_md


COPY . .

ENV NAME LUCI
