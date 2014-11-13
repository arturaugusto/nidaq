nidaq
=====

Python lib to communicate with NIDAQmx driver from National Instrument.

I created this lib for learning purpose, based on example found in http://wiki.scipy.org/Cookbook/Data_Acquisition_with_NIDAQmx

Sample usage
=====

```python
from nidaq import *
board = DAQmx("Dev1")
task = board.create_task()
task.add_channel("1")
task.config_sampling(10, 1000)
task.start()
print task.get_volt_samples_average()
task.end()
```
