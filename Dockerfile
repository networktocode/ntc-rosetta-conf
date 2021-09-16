ARG PYTHON

FROM python:${PYTHON}-stretch

RUN apt-get update && apt-get install -y pandoc jq

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python && \
    /root/.poetry/bin/poetry config virtualenvs.create false && ln -sf /root/.poetry/bin/poetry /usr/local/bin/poetry

ADD poetry.lock /tmp
ADD pyproject.toml /tmp
RUN cd /tmp && poetry install
RUN python -m bash_kernel.install

ADD docs/requirements.txt /tmp/requirements-docs.txt
RUN pip install -r /tmp/requirements-docs.txt

ADD . /ntc-rosetta-conf

WORKDIR "/ntc-rosetta-conf"

RUN poetry install
