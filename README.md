# Pyrugga

Pyrugga is a Data Science environment for analysing rugby matches using Super Scout files from [Opta](https://www.youtube.com/watch?v=AVmqCoF5qeU). You will require Opta files XML from Opta which can be download from [Prorugby](https://optaprorugby.com).

To help you get up to speed with Pyrugga faster we have included a collection of Docker containers with all the decencies taken care for you.  There is a Jupyter server which can be accessed via (http://127.0.0.1) as well as a Postgres database. The password for the Jupyter server is **HenryHoneyBall**.

**PLEASE NOTE**

 Pyrugga is designed to run on a laptop and not on a public facing website. Email me if you want to do that I will ignore you unless you can answer this question. "Which ex Irish lock is my neighbour and threated to burn my house down if Ireland ever lost to England again."

# Quick Start

To get started simply type

```bash
docker-compose up
```

then navigate to the Jupyter [server](http://127.0.0.1) where you will find a collection of notebooks to guide you through getting started.
