FROM gfourmis/flask-pandas:1.0
MAINTAINER Olga Canabal / Felipe Rojas
COPY mypandas.py /myhome/mypandas.py
COPY c6dm-udt9.csv /myhome/c6dm-udt9.csv
WORKDIR /myhome
ENTRYPOINT [ "python3" ]
CMD [ "/myhome/mypandas.py" ]
