FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install pandas
RUN pip install -U selenium
RUN pip install fuzzywuzzy

RUN mkdir -p /Users/docker_test
WORKDIR /Users/docker_test

ADD msedgedriver.exe .
ADD 00_scrape_data.py .
ADD 01_clean_match_compare.py .

CMD python3 /Users/docker_test/00_scrape_data.py
CMD python3 /Users/docker_test/01_clean_match_compare.py