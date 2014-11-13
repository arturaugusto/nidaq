nidaq
=====

Python lib to communicate with NIDAQmx driver from National Instrument.

I created this lib for learning purpose, based on example found in http://wiki.scipy.org/Cookbook/Data_Acquisition_with_NIDAQmx

Sample usage
=====

```python
from nidaq import *
board = DAQmx("Dev2")
task = board.create_task()
task.add_channel("1")
task.add_channel("3")
task.config_sampling(3, 1000)
task.start()
print task.get_volt_samples() # sample output: [-0.04225668 -0.10703132 -0.13892543 -0.00082721  0.00015921  0.00048801]
# First 3 samples are from channel 1 and last 3 from channel 3
task.end()
```

MIT license
