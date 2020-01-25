import pytest
import requests
from math import isclose

url = 'http://127.0.0.1:5000'


def test_index_page():
    r = requests.get(url+'/')
    assert r.status_code == 200


def test_avg_elapsed_time():
    r = requests.get(url+'/api/v1/queries/avg_elapsed_time?date=2019-10-18')
    data = r.json()
    assert r.status_code == 200
    assert isclose(data['Average elapsed time, sec'], 34.27, rel_tol=1e-02)


def test_avg_rows_per_sec():
    r = requests.get(url+'/api/v1/queries/avg_rows_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03')
    data = r.json()
    assert r.status_code == 200
    assert isclose(data['Average rows per sec'], 5417456.25, rel_tol=1e-02)


def test_avg_rows_per_thread():
    r = requests.get(url+'/api/v1/queries/avg_rows_per_thread?start=2018-10-18+10:12:03&end=2019-10-18+10:28:03')
    data = r.json()
    assert r.status_code == 200
    assert isclose(data['Average rows per thread'], 28148733.99, rel_tol=1e-02)


def test_avg_thread_per_sec():
    r = requests.get(url+'/api/v1/queries/avg_thread_per_sec?start=2018-10-18+10:12:03&end=2019-10-18+10:28:03')
    data = r.json()
    assert r.status_code == 200
    assert isclose(data['Average threads per sec'], 0.0316, rel_tol=1e-02)