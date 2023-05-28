FROM python:3.10.9 as base

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt update && apt -qy install python3-dev gcc musl-dev

RUN useradd -rms /bin/bash welbex_admin && chmod 777 /opt /run

WORKDIR /welbex_project

RUN mkdir /welbex_project/static && mkdir /welbex_project/media && chown -R welbex_admin:welbex_admin /welbex_project && chmod 777 /welbex_project

COPY --chown=welbex_admin:welbex_admin . .

RUN pip install -r requirements.txt

USER welbex_admin

CMD ["python3 manage.py runserver 0.0.0.0:8000"]