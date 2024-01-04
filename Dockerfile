FROM acidrain/python-poetry:3.9-slim
USER root
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/haphan/telebot-tldr.git .

RUN poetry install -vvv && chmod +x run.sh

ENTRYPOINT ["./run.sh"]