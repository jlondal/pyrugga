# Pyrugga

Pyrugga is a module to help analyse rugby matches using Super Scout files from [Opta](https://www.youtube.com/watch?v=AVmqCoF5qeU). You will require Super Scout XML files from Opta which can be download from [Prorugby](https://optaprorugby.com).

To help you get up to speed with Pyrugga faster we have included a collection of Docker containers with all the decencies taken care for you.  There is a Jupyter server which can be accessed via (http://127.0.0.1) as well as a Postgres database. The password for the Jupyter server is **HenryHoneyBall**.

**PLEASE NOTE**

 Pyrugga is designed to run on a laptop or desktop and not on a public facing website

# Quick Start

If you have never used Python before or have limited experience with it then we recommend you follow the **Never Python** track leveraging the Docker containers. If on the other hand you already have setup you environment just how you like it then install Pyrugga from via pip as follows.

```bash
pip install ...
``

## Never Python

You will need to install Docker before you can run Pyrugga. Docker is tool to build mini virtual machines and can be download for [Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) and [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows) from Dockers website.

Once Docker is installed you will either need to open up your Terminal (Mac/Linux) or Command line prompt (Windows).

### Mac

Open your Terminal. If you do not know how to do that watch the follow [video](https://www.youtube.com/watch?v=zw7Nd67_aFw). Then navigate to the director you have downloaded Pyrugga to. For example if you have downloaded Pyrugga to your Downloads folder then you would need to type something like.

```bash
cd /Users/james_londal/Downloads/pyrugga
```

obviously if your user name is not james_londal change it to whatever your user name is. A tutorial on how to use the Terminal can be found [here](https://www.youtube.com/watch?v=oxuRxtrO2Ag).

To launch the Docker containers type


```bash
docker-compose up
```

then navigate to the Jupyter [server](http://127.0.0.1) where you will find a collection of notebooks to guide you through getting started with Pyrugga

### Windows

Open the Command line . If you do not know how to do that watch the following [video](https://www.youtube.com/watch?v=MBBWVgE0ewk).

Then navigate (via the Command Line) to the folder you have downloaded Pyrugga to and type

```bash
docker-compose up
```

then navigate to the Jupyter [server](http://127.0.0.1) where you will find a collection of notebooks to guide you through getting started with Pyrugga
