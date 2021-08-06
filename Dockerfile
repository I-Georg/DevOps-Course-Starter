FROM python:3.7.9-slim-buster as base

ARG FLASK_ENV

ENV FLASK_ENV=${FLASK_ENV} \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.6


RUN pip install "poetry==$POETRY_VERSION"

#production
FROM base as production
# Copy only requirements to cache them in docker layer
WORKDIR /todo_app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
RUN poetry add gunicorn
RUN chmod +x "./gunicorn.sh"

# Creating folders, and files for a project:
COPY . /todo_app 

#EXPOSE 5001
ENTRYPOINT ["./gunicorn.sh"]

#development
FROM base as development
WORKDIR /todo_app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false --local && poetry install --no-root


# Creating folders, and files for a project:
COPY . /todo_app ./


EXPOSE 5001

ENTRYPOINT ["poetry", "run","flask", "run", "--host", "0.0.0.0"]

# testing stage
FROM base as test
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false --local && poetry install --no-dev --no-root
COPY . /todo_app 
COPY  . /.env.test
WORKDIR /todo_app

# install geckodriver and firefox

RUN apt-get update -y \
    && apt-get install --no-install-recommends --no-install-suggests -y tzdata ca-certificates bzip2 curl wget libc-dev libxt6 \
    && apt-get install --no-install-recommends --no-install-suggests -y `apt-cache depends firefox-esr | awk '/Depends:/{print$2}'` \
    && update-ca-certificates \
    # Cleanup unnecessary stuff
    && apt-get purge -y --auto-remove \
                  -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /tmp/*

# install geckodriver
RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
# install firefox
RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP


#RUN pip3 install selenium
#RUN pip3 install Selenium-Screenshot

ENTRYPOINT ["poetry", "run", "pytest"]