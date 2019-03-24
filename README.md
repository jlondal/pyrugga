# Pyrugga

![](logo.png)

Pyrugga is a library to help analyse rugby matches using Opta's Super Scout files. Example notebooks can found are:

* [Getting Started](https://github.com/jlondal/pyrugga/blob/master/jupyter/tuts/Getting%20Started.ipynb)
* Predicting Results
* Benchmarking


If you have never used Python don't worry there is a step by step walk through on [Learning Python](Learning Python.md) section.



To install

```bash
pip install pyrugga
```

To install the development version

```bash
pip install -U git+https://github.com/jlondal/pyrugga.git
```

You will require Super Scout files from [Opta](https://www.youtube.com/watch?v=AVmqCoF5qeU) which can be download via [Prorugby](https://optaprorugby.com).


```python
import pyrugga as prg

df = pgr.Match('918053_walvfra_new.xml')

#print summary of match
df.summary

#list all actions in a matches
df.events

#time line of a match
df.timeline
```

# License

See [LICENSE](LICENSE)
