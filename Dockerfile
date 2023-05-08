# syntax=docker/dockerfile:1.4
FROM python:3.11

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN <<EOF
    set -eu

    apt-get update
    apt-get install -y \
        gosu
    apt-get clean
    rm -rf /var/lib/apt/lists/*
EOF

RUN <<EOF
    set -eu
    useradd -o -u 1000 -m user
EOF

ADD ./requirements.txt /
RUN <<EOF
    set -eu
    gosu user pip3 install --no-cache-dir -r /requirements.txt
EOF

ADD ./harmonica_l12_node /code/harmonica_l12_node
ENTRYPOINT [ "gosu", "user", "python3", "/code/harmonica_l12_node/main.py" ]
CMD [ "run" ]
