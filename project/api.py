from datetime import datetime, timedelta
import flask
from flask import request, jsonify
from werkzeug.exceptions import HTTPException
import pandas as pd


app = flask.Flask(__name__)


def to_milliseconds(dt):
    """Convert datetime object to timestamp in millisecond format"""
    return int(datetime.timestamp(dt)*1000.)


def prepare_request(time_range_start, time_range_end):
    """Convert datetime time range to  timestamp in millisecond format"""
    datetime_start = datetime.strptime(time_range_start, '%Y-%m-%d %H:%M:%S')
    datetime_end = datetime.strptime(time_range_end, '%Y-%m-%d %H:%M:%S')
    datetime_start_code = to_milliseconds(datetime_start)
    datetime_end_code = to_milliseconds(datetime_end)
    return datetime_start_code, datetime_end_code


@app.route('/', methods=['GET'])
def home():
    return "<h1>Junior Data Scientist/Data Engineer Test Task</h1>"


@app.errorhandler(Exception)
def handle_error(e):
    """Generic exception handler"""
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


@app.errorhandler(404)
def page_not_found(e):
    """Handle cases with empty query parameter"""
    code = 404
    return jsonify(error=str(e), code=code)


@app.errorhandler(400)
def handle_bad_request(e):
    """Handle cases with wrong query parameter"""
    code = 400
    return jsonify(error=str(e), code=code), code


@app.route('/api/v1/queries/avg_elapsed_time', methods=['GET'])
def avg_elapsed_time():
    """Returns an average elapsed time for all queries on certain date"""
    query_parameters = request.args
    date = query_parameters.get('date')
    if not date:
        return page_not_found('No date provided')

    data = pd.read_csv('queries.tsv', sep='\t')
    try:
        date_start = datetime.strptime(date, '%Y-%m-%d')
    except ValueError as e:
        return handle_bad_request(e)
    date_end = date_start + timedelta(days=1, milliseconds=-1)
    date_start_code = to_milliseconds(date_start)
    date_end_code = to_milliseconds(date_end)

    day_data = data[data['time'].between(date_start_code, date_end_code)]
    if day_data.shape[0] == 0:
        return handle_bad_request('Date is out of range')

    day_pivot = day_data.pivot(index='query_id', columns='status', values='time')
    not_closed_within_day = day_pivot.isnull().values.any(1).nonzero()[0]  # if not empty returns indexes

    if not_closed_within_day.shape[0] > 0:
        day_pivot.drop(day_pivot.index[not_closed_within_day], inplace=True)

    day_pivot['elapsed_time'] = (day_pivot[1] - day_pivot[0]) / 1000

    avg_time = day_pivot['elapsed_time'].mean()

    return jsonify({'Average elapsed time, sec': avg_time})


@app.route('/api/v1/queries/avg_rows_per_sec', methods=['GET'])
def avg_rows_per_sec():
    """Returns an average per second number of rows returned from all queries during certain time range"""
    query_parameters = request.args
    time_range_start = query_parameters.get('start')
    time_range_end = query_parameters.get('end')
    if not time_range_start or not time_range_end:
        return page_not_found('No time range provided')

    try:
        datetime_start_code, datetime_end_code = prepare_request(time_range_start, time_range_end)
    except ValueError as e:
        return handle_bad_request(e)

    data = pd.read_csv('queries.tsv', sep='\t')

    time_range_data = data[data['time'].between(datetime_start_code, datetime_end_code)]
    if time_range_data.shape[0] == 0:
        return handle_bad_request(400)

    time_range_pivot = time_range_data.pivot(index='query_id', columns='status', values=['time', 'rows'])

    not_closed_within_range = time_range_pivot.isnull().values.any(1).nonzero()[0]  # if not empty returns indexes

    if not_closed_within_range.shape[0] > 0:
        time_range_pivot.drop(time_range_pivot.index[not_closed_within_range], inplace=True)

    time_range_pivot['elapsed_time'] = (time_range_pivot['time'][1] - time_range_pivot['time'][0]) / 1000

    avg_rows = time_range_pivot['rows'][1].sum() / time_range_pivot['elapsed_time'].sum()
    return jsonify({'Average rows per sec': avg_rows})


@app.route('/api/v1/queries/avg_rows_per_thread', methods=['GET'])
def avg_rows_per_thread():
    """Returns an average per thread number of rows returned from all queries during certain time range"""
    query_parameters = request.args
    time_range_start = query_parameters.get('start')
    time_range_end = query_parameters.get('end')
    if not time_range_start or not time_range_end:
        return page_not_found('No time range provided')

    try:
        datetime_start_code, datetime_end_code = prepare_request(time_range_start, time_range_end)
    except ValueError as e:
        return handle_bad_request(e)

    data = pd.read_csv('queries.tsv', sep='\t')

    time_range_data = data[data['time'].between(datetime_start_code, datetime_end_code) & data['status'] == 1]
    if time_range_data.shape[0] == 0:
        return handle_bad_request(400)

    time_range_data['n_threads'] = time_range_data.threads.str.count(',') + 1

    avg_rows = time_range_data['rows'].sum() / time_range_data['n_threads'].sum()
    return jsonify({'Average rows per thread': avg_rows})


@app.route('/api/v1/queries/avg_thread_per_sec', methods=['GET'])
def avg_thread_per_sec():
    """Returns an average per second number of threads executing at the same time during certain time range"""
    query_parameters = request.args
    time_range_start = query_parameters.get('start')
    time_range_end = query_parameters.get('end')
    if not time_range_start or not time_range_end:
        return page_not_found('No time range provided')

    try:
        datetime_start_code, datetime_end_code = prepare_request(time_range_start, time_range_end)
    except ValueError as e:
        return handle_bad_request(e)

    data = pd.read_csv('queries.tsv', sep='\t')

    time_range_data = data[data['time'].between(datetime_start_code, datetime_end_code)]

    time_range_data['time'] = round(time_range_data['time'] / 1000)  # ms tos
    time_range_data['time'] = time_range_data['time'].astype('int64')
    time_range_data['query_id'] = time_range_data['query_id'].astype('str')

    time_range_pivot = time_range_data.pivot(index='query_id', columns='status', values=['time', 'threads'])

    zipped = zip(time_range_pivot.index, time_range_pivot['time'][0], time_range_pivot['time'][1])
    # each second of query
    time_range_df = pd.DataFrame([(i, y) for i, s, e in zipped for y in range(s, e + 1)],
                                 columns=['query_id', 'sec'])
    # merging queries id's that that have common seconds
    time_range_df = pd.merge(time_range_df, time_range_df, on='sec', how='inner')
    time_range_df = time_range_df[time_range_df['query_id_x'] != time_range_df['query_id_y']]

    time_range_df['id'] = time_range_df[['query_id_x', 'query_id_y']].apply(lambda x: ' '.join(x), axis=1)
    time_range_df['id'] = time_range_df['id'].apply(lambda x: tuple(sorted(x.split(' '))))
    time_range_df.drop_duplicates(['sec', 'id'], keep='first', inplace=True)
    time_range_df['common_seconds'] = time_range_df.groupby('id')['id'].transform('count')

    same_time_queries = time_range_df[['query_id_x', 'query_id_y', 'common_seconds']].copy()
    same_time_queries.drop_duplicates(['query_id_x', 'query_id_y'], keep='first', inplace=True)

    same_time_queries = pd.merge(same_time_queries,
                                 time_range_data.loc[time_range_data['status'] == 1, ['query_id', 'threads']],
                                 left_on='query_id_x', right_on='query_id', how='left', left_index=False)
    same_time_queries = pd.merge(same_time_queries,
                                 time_range_data.loc[time_range_data['status'] == 1, ['query_id', 'threads']],
                                 left_on='query_id_y', right_on='query_id', how='left')
    same_time_queries['threads_x'] = same_time_queries['threads_x'].apply(lambda x: set(x.split(',')))
    same_time_queries['threads_y'] = same_time_queries['threads_y'].apply(lambda x: set(x.split(',')))
    same_time_queries['common_threads'] = [len(set(a).intersection(b)) for a, b in
                                           zip(same_time_queries.threads_x, same_time_queries.threads_y)]

    avg_rows = same_time_queries[same_time_queries['common_threads'] != 0]['common_threads'].sum() / \
               same_time_queries[same_time_queries['common_threads'] != 0]['common_seconds'].sum()

    return jsonify({'Average threads per sec': avg_rows})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
