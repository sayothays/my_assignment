FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install python-Levenshtein 
RUN pip3 install pandas
RUN pip3 install -U selenium
RUN pip3 install fuzzywuzzy

RUN mkdir -p /Users/docker_test
WORKDIR /Users/docker_test

ADD msedgedriver.exe .
ADD 00_scrape_data.py .
ADD 01_clean_match_compare.py .

CMD python3 00_scrape_data.py
CMD python3 01_clean_match_compare.py
