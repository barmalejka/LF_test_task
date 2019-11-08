<h1> Test task service API </h1>

<h3> REST API version </h3>
The most recent version of the API is v1.

<h2> Running Docker image <i>(Linux)</i></h2>

In order to run this container you'll need docker [installed](https://docs.docker.com/install/)

In the `project` directory run

```shell
$ sudo docker build -t my_docker_flask:latest .
$ sudo docker run -d -p 5000:5000 my_docker_flask:latest
```

Check if container is running by going to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<h2> Available endpoints and how to use them </h2>

<h3> Method 1: Get an average elapsed time for all queries on certain date </h3>

<b>Description:</b> This endpoint returns an average elapsed time for all queries on certain date 

<b>Request URL:</b> http://127.0.0.1:5000/api/v1/queries/avg_elapsed_time?date=[:date]

<b>Request Values:</b> date in %Y-%m-%d format

<b>Return Values:</b> Average elapsed time, sec

<b>Example Request:</b> http://127.0.0.1:5000/api/v1/queries/avg_elapsed_time?date=2019-10-18

<i> Estimated time:</i> 0.1 sec

<i> Estimated RAM usage:</i> 80MB

<h3> Method 2: Get an average per second number of rows returned from all queries during
certain time range </h3>

<b>Description:</b> This endpoint returns an average per second number of rows returned from all queries during
certain time range

<b>Request URL:</b> http://127.0.0.1:5000/api/v1/queries/avg_rows_per_sec?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average rows per sec

<b>Example Request:</b> http://127.0.0.1:5000/api/v1/queries/avg_rows_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

<i> Estimated time:</i> 0.1 sec

<i> Estimated RAM usage:</i> 90MB

<h3> Method 3: Get an average per thread number of rows returned from all queries during
certain time range </h3>

<b>Description:</b> This endpoint returns an average per thread number of rows returned from all queries during
certain time range

<b>Request URL:</b> http://127.0.0.1:5000/api/v1/queries/avg_rows_per_thread?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average rows per thread

<b>Example Request:</b> http://127.0.0.1:5000/api/v1/queries/avg_rows_per_thread?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

<i> Estimated time:</i> 0.1 sec

<i> Estimated RAM usage:</i> 80MB

<h3> Method 4: Get an average per second number of threads executing at the same time during
certain time range? </h3>

<b>Description:</b> This endpoint returns an average per second number of threads executing at the same time during
certain time range

<b>Request URL:</b> http://127.0.0.1:5000/api/v1/queries/avg_thread_per_sec?start=[:datetime]&end=[:datetime]

<b>Request Values:</b> start and end of timerange in %Y-%m-%d+%H:%M:%S format

<b>Return Values:</b> Average threads per sec

<b>Example Request:</b> http://127.0.0.1:5000/api/v1/queries/avg_thread_per_sec?start=2019-10-18+10:12:03&end=2019-10-18+10:28:03

<i> Estimated time:</i> 20 sec
