FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get install graphviz -y \
    && apt-get install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra -y \
    && apt-get clean

RUN pip install ast-visualizer-marvel1337

RUN apt-get install texlive-lang-cyrillic -y

COPY . /app/