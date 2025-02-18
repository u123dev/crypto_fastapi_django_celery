FROM python:3.10.5

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/src

WORKDIR /src

RUN apt update \
    && apt install -y --no-install-recommends less \
    dos2unix

RUN pip install poetry\
    && poetry config virtualenvs.in-project true

## Ensure Unix-style line endings for scripts
#RUN dos2unix ./scripts/*.sh
#
## Add execute bit to commands files
#RUN chmod +x ./scripts/*.sh
