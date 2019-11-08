# Pyrugga

![](logo.png)

Pyrugga is a library to help analyse rugby matches using [Opta's](https://www.youtube.com/watch?v=AVmqCoF5qeU) Super Scout files. To learn more have a look at [Getting Started](https://github.com/jlondal/pyrugga/blob/master/jupyter/tuts/Getting%20Started.ipynb) notebook.

## Why use Pyrugga

* Converts XML Super Scout files to three Pandas Dataframes providing: a summary of a match, a time line and list of all actions

* Heatmaps

![](heatmap.png)

* Player Summary

![](player_summary.png)

## Install

### Windows

If you are using Windows you need to use Docker environment rather than pip installing. To do this install docker https://docs.docker.com/docker-for-windows/ and then download the Pyrugga repo as a [zip file](https://github.com/jlondal/pyrugga/archive/master.zip). Unzip the file and then run the windows_start.bat to start and window_stop.bat to end. Once you start it will launch a juypter server which you can access via [http://127.0.0.1:8080/tree](http://127.0.0.1:8080/tree). 

If you dont know how to use Juypter read this [tutorial](https://www.codecademy.com/articles/how-to-use-jupyter-notebooks). Don't worry about setting up Juypter. Docker does that for you. 


### Everyone else (recommended)

```bash
pip install pyrugga
```

For the development version

```bash
!pip install --upgrade --force-reinstal --no-deps git+https://github.com/jlondal/pyrugga.git
```

## Quick Start

```python
import pyrugga as prg

df = pgr.Match('918053_walvfra_new.xml')

#print summary of match
df.summary

#list all actions in a matches
df.events

#time line of a match
df.timeline

#prints a heatmap
df.heat_map(event='Carry', event_type='One Out Drive', description='Crossed Gainline')

#prints a summary of each players actions normalise by phases while pitch
df.player_summary(norm='phases')

```
## License

See [LICENSE](LICENSE)
