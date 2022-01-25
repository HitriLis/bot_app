FROM python:3.8

COPY --chown=www-data:www-data app/backend/build/pip/ /var/app/build/pip/
RUN pip install -r /var/app/build/pip/dev_requirements.txt

VOLUME /var/app/
EXPOSE 8000
WORKDIR /var/app/src/

COPY --chown=www-data:www-data ci/dev/docker/backend/scripts/* /

CMD ["/entrypoint.sh"]
