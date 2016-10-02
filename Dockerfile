FROM python:3.5-onbuild

RUN pip install gunicorn
WORKDIR /tessera

CMD [ "./run.sh" ]
