<h1> Test task service API </h1>

<h3> REST API version </h3>
The most recent version of the API is v1.

<h2> Running Docker image <i>(Linux)</i></h2>

In order to run this container you'll need docker [installed](https://docs.docker.com/install/)

In the `project` directory run

```shell
$ docker build -t queries_api:latest .
$ docker run -d --rm -p 5000:5000 -v $(pwd)/data/:/app/data/ queries_api:latest
```

Check if container is running by going to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<h2> Running tests </h2>

In the `project` directory run

```shell
$ pip install pytest
$ pytest test_endpoints.py
```

<h2> Available endpoints and how to use them </h2>

<h3> Method 1: Get an average elapsed time for all queries on certain date </h3>

<b>Description:</b> This endpoint returns an average elapsed time for all queries on certain date

<b>Request URL:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_elapsed_time?date=[:date]

<b>Request Values:</b> date in %Y-%m-%d format

<b>Return Values:</b> Average elapsed time, sec

<b>Example Request:</b> GET  http://127.0.0.1:5000/api/v1/queries/avg_elapsed_time?date=2019-10-18

```shell
{
  "Average elapsed time, sec": 35.599660105287256
}
```

<i> Estimated RAM usage:</i> 80MB

<h3> Method 2: Get an average per second number of rows returned from all queries during
certain time range </h3>

<b>Description:</b> This endpoint returns an average per second number of rows returned from all queries during
certain time range

<b>Request URL:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_rows_per_sec?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average rows per sec

<b>Example Request:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_rows_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

```shell
{
  "Average rows per sec": 5467092.93808785
}
```

<i> Estimated RAM usage:</i> 90MB

<h3> Method 3: Get an average per thread number of rows returned from all queries during
certain time range </h3>

<b>Description:</b> This endpoint returns an average per thread number of rows returned from all queries during
certain time range

<b>Request URL:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_rows_per_thread?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average rows per thread

<b>Example Request:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_rows_per_thread?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

```shell
{
  "Average rows per thread": 27602662.091584157
}
```

<i> Estimated RAM usage:</i> 80MB

<h3> Method 4: Get an average per second number of threads executing at the same time during
certain time range? </h3>

<b>Description:</b> This endpoint returns an average per second number of threads executing at the same time during
certain time range

<b>Request URL:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_thread_per_sec?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average threads per sec

<b>Example Request:</b> GET http://127.0.0.1:5000/api/v1/queries/avg_thread_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

```shell
{
  "Average threads per sec": 0.033582089552238806
}
```

<h2> Request time and response time estimation </h2>

In `project` directory run

```shell
$ curl -w "@curl-format.txt" -o /dev/null -s "[request]"
```

<b> Example</b>

Run

```shell
$ curl -w "@curl-format.txt" -o /dev/null -s http://127.0.0.1:5000/api/v1/queries/avg_rows_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03
```

Result

```shell
    time_namelookup:  0.000120
       time_connect:  0.000483
    time_appconnect:  0.000000
   time_pretransfer:  0.000633
      time_redirect:  0.000000
 time_starttransfer:  0.006627
                    ----------
         time_total:  0.007150
```