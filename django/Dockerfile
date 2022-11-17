FROM nginx:1.21.1

RUN apt-get update -q
RUN apt-get install -qy python3-pip python3-venv python3-dev
RUN apt-get install -y nano curl libpq-dev apt-utils gettext git libffi-dev
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv poetry==1.1.13

# Configure poetry
ENV PATH="$PATH:/root/.poetry/bin"

RUN mkdir -p /webapps

WORKDIR /opt
RUN virtualenv venv

WORKDIR /tmp

COPY ./poetry.lock ./
COPY ./pyproject.toml ./

# RUN sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' ~/.poetry/bin/poetry
RUN poetry lock --no-update
RUN poetry export -n --without-hashes -f requirements.txt -o /tmp/requirements.txt --dev
RUN bash -c "source /opt/venv/bin/activate && pip3 install -r /tmp/requirements.txt --no-cache-dir"


RUN mkdir -p /var/log/cforemoto/
RUN touch /var/log/cforemoto/cforemoto.log
RUN chmod 766 /var/log/cforemoto/cforemoto.log

COPY ./scripts/* /usr/local/bin/
RUN bash -c "chmod 755 -R /usr/local/bin"

COPY ./ /webapps/cforemoto
WORKDIR /webapps/cforemoto
EXPOSE 7010 7001 7002

CMD ["/bin/bash"]
