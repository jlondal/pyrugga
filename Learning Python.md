# Learning Python

To help you get up to speed as quickly as possible we have included a Docker container with everything you need to use Python and Pyrugga.

Docker is tool to run mini-virtual machines, or micro services, and can be download for [Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) and [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows) from Dockers website.

Once Docker is installed you will either need to open up your Terminal (Mac/Linux) or Command Line (Windows) to start your virtual machine.

## Mac

Open your Terminal. If you do not know how to do that [watch](https://www.youtube.com/watch?v=zw7Nd67_aFw). Then navigate to the folder you have downloaded Pyrugga to. For example if you have downloaded Pyrugga to your Downloads folder then you would need to type something like.

```bash
cd /Users/henry_honeyball/Downloads/pyrugga
```

Obviously if your user name is not henry_honeyball change it to whatever your user name is. A tutorial on how to use the Terminal can be found [here](https://www.youtube.com/watch?v=oxuRxtrO2Ag).

To launch the Docker containers type

```bash
docker-compose down && docker-compose up
```

then navigate to the Jupyter [server](http://127.0.0.1) were you will find a collection of notebooks to guide you through getting started with Pyrugga

## Windows

Open the Command line. If you do not know how to do that watch the following [video](https://www.youtube.com/watch?v=MBBWVgE0ewk).

Then navigate (via the Command Line) to the folder you have downloaded Pyrugga to and type

```bash
docker-compose down
docker-compose up
```

then navigate to the [Jupyter server](http://127.0.0.1) where you will find a collection of notebooks to guide you through getting started with Pyrugga


# License

See [LICENSE](LICENSE)
