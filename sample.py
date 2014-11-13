from nidaq import *
board = DAQmx("Dev2")
task = board.create_task()
task.add_channel("1")
task.add_channel("3")
task.config_sampling(3, 1000)
task.start()
print task.get_volt_samples()
task.end()

raw_input()
