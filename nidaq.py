# Adaptado por Artur Augusto - arturaugusto@gmail.com
# This is a near-verbatim translation of the example program
# C:\Program Files\National Instruments\NI-DAQ\Examples\DAQmx ANSI C\Analog In\Measure Voltage\Acq-Int Clk\Acq-IntClk.c
import ctypes
import numpy
import time
class DAQmx:
	##############################
	# Setup some typedefs and constants
	# to correspond with values in
	# C:\Program Files\National Instruments\NI-DAQ\DAQmx ANSI C Dev\include\NIDAQmx.h
	##############################
	nidaq = ctypes.windll.nicaiu # load the DLL
	physicalChannel = ""
	# the constants
	DAQmx_Val_Volts = 10348
	DAQmx_Val_Rising = 10280
	DAQmx_Val_FiniteSamps = 10178
	
	int32 = ctypes.c_long
	DAQmx_Val_Cfg_Default = int32(-1)
	DAQmx_Val_RSE               = 10083
	DAQmx_Val_NRSE              = 10078
	DAQmx_Val_Diff              = 10106
	DAQmx_Val_PseudoDiff        = 12529

	terminalConfig = DAQmx_Val_Cfg_Default
	def __init__(self, physicalChannel):
		DAQmx.physicalChannel = physicalChannel

	def create_task(self):
		return self.DAQmxTask()

	class DAQmxTask:
		def __init__(self):
			self.nidaq = DAQmx.nidaq
			self.int32 = ctypes.c_long
			self.uInt32 = ctypes.c_ulong
			self.uInt64 = ctypes.c_ulonglong
			self.float64 = ctypes.c_double
			self.TaskHandle = self.uInt32

			# initialize variables
			self.taskHandle = self.TaskHandle(0)
			self.CHK(self.nidaq.DAQmxCreateTask("",ctypes.byref(self.taskHandle)))

			# list of channels
			self.__channels = []

		def CHK(self, err):
			"""a simple error checking routine"""
			if err < 0:
				buf_size = 100
				buf = ctypes.create_string_buffer('\000' * buf_size)
				self.nidaq.DAQmxGetErrorString(err,ctypes.byref(buf),buf_size)
				raise RuntimeError('nidaq call failed with error %d: %s'%(err,repr(buf.value)))

		def add_channel(self, channel):
			self.__channels.append(channel)
			self.__create_voltage_channel(channel)
			self.n_ch = len(self.__channels)
		

		def config_sampling(self, samples, rate):
			self.num_samples = samples
			self.rate = rate
			self.CHK(self.nidaq.DAQmxCfgSampClkTiming(self.taskHandle,"",self.float64(self.rate),
									DAQmx.DAQmx_Val_Rising,DAQmx.DAQmx_Val_FiniteSamps,
									self.uInt64(self.num_samples*self.n_ch)));

		def __create_voltage_channel(self, channel):
			self.CHK(
				self.nidaq.DAQmxCreateAIVoltageChan(
					self.taskHandle,
					DAQmx.physicalChannel + "/ai" + channel,"",
					DAQmx.DAQmx_Val_Cfg_Default,
					self.float64(-10.0),
					self.float64(10.0),
					DAQmx.DAQmx_Val_Volts,
					None
				)
			)
		
		def start(self):
			self.CHK(self.nidaq.DAQmxStartTask(self.taskHandle))
			
		def end(self):
			if self.taskHandle.value != 0:
				self.nidaq.DAQmxStopTask(self.taskHandle)
				self.nidaq.DAQmxClearTask(self.taskHandle)

		def get_volt_samples(self):
			self.data = numpy.zeros((self.num_samples*self.n_ch,),dtype=numpy.float64)
			read = self.int32()
			self.CHK(
				self.nidaq.DAQmxReadAnalogF64(
					self.taskHandle, #taskHandle TaskHandle
					self.num_samples, #numSampsPerChan int32
					self.float64(10.0), #timeout float64
					0, #fillMode bool32
					self.data.ctypes.data, #arraySizeInSamps uInt32
					self.num_samples*self.n_ch,
					ctypes.byref(read),
					None
				)
			)
			return self.data
