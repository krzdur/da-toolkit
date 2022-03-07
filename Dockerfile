FROM python:3.9-buster

WORKDIR /workdir

COPY dist /workdir/dist
COPY service_account.json /workdir
COPY da_toolkit/test/test_abtest_analysis.py /workdir/tests/
COPY da_toolkit/test/test_query_bigquery.py /workdir/tests/

RUN pip install dist/da-toolkit-0.2.1.tar.gz
RUN pip install pytest