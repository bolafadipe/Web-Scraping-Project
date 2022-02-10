 #install google chrome
# FROM python:latest
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# RUN apt-get -y update
# RUN apt-get install -y google-chrome-stable

# #install chromedriver
# RUN apt-get install -yqq unzip
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# #set display port to avoid crash
# ENV DISPLAY=:99

# COPY . /tour_scraper
# WORKDIR /tour_scraper

# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt

# CMD ["python", "./tours_scraper.py"]

# FROM selenium/standalone-chrome
# USER root
# RUN wget https://bootstrap.pypa.io/get-pip.py
# RUN python3 get-pip.py
# COPY . /tour_scraper
# WORKDIR /tour_scraper

# #RUN pip install --upgrade pip

# RUN pip install -r requirements.txt

# CMD ["python", "./tours_scraper.py"]
# RUN python3 get-pip.py
# RUN python3 -m pip install selenium

# FROM joyzoursky/python-chromedriver:3.9

# RUN mkdir packages
# ADD requirements.txt packages
# RUN python -m pip install --upgrade pip
# RUN pip install -r packages/requirements.txt
# CMD ["python", "./tours_scraper.py"]

FROM python:3.8


 


# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +x /usr/bin/chromedriver
# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --no-cache-dir --upgrade pip
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /Tours
COPY src/tours /Tours
COPY src/run_in_docker.sh /Flights/run_in_docker.sh

RUN mkdir /tmp/.X11-unix/

RUN useradd User \
    && chown -R User /Flights \
    && chmod -R u+x /Flights \
    && chmod -R 1777 /tmp/.X11-unix/
USER User

CMD ["bash", "run_in_docker.sh"]