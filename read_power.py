##
# File: read_power.py
# Authors: ERSP Group
# Description: Takes readings from a power meter connected to four different 
#              machines, then uses the data to generate an graph plotting 
#              watts in relation to time
##

# Import necessary packages
import vxi11, sched, time, random, string
import numpy as numpy
import pandas as pd

# Using Agg instead of Xwindows or run ssh -X 
# (Configured for pipenv)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Define instrument
instr = vxi11.Instrument("172.19.222.92","gpib0,12") # Use IP address and interface info
print(instr.ask("*IDN?")) # Prints out device model

# Generate session id and create output file in /data
session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
f = open("data/session-"+session_id+".txt", "w") # Creates file 
print("Beginning read session: "+session_id)

# Define scheduler and collect user input for timeframe
s = sched.scheduler(time.time, time.sleep)
secs = float(raw_input("Enter number of seconds: ")) # Asks for user input
end = time.time() + secs # End time is (system time) + (number of seconds)

##
# Schedules next power meter reading and also takes measurements from each
# of the four machines and writes the data to the file in ./data delimited
# by commas
#
# @param sc is the scheduler used to manage function calls
##
def read_power(sc):
  if time.time() < end: # Schedule another reading in 1 sec if time is valid
    s.enter(1, 1, read_power, (sc,))
  power = instr.ask("measure:scalar:power:real? 0") # Ask for readings on 4 channels
  f.write(power+",") # Writes data to file
  f.flush() # Flushes buffer so data written immediately

# Schedule execution over user-inputted timeframe
s.enter(0, 1, read_power, (s,)) # First measurement scheduled immediately
s.run() # Run scheduler

# Read delimited session string from file
f = open('data/session-'+session_id+'.txt', 'r') # Opens data file
data = f.read().split(",") # Delimits data using commas
del data[-1] # Deletes extra comma at the end

# Coverts data to 2D array
data = [float(i) for i in data]
frames = [data[i*4:(i+1)*4] for i in range(len(data)//4)]

# Generate plot and save to /figures
df = pd.DataFrame(frames, columns=['c09-13', 'c09-14', 'c09-15', 'c09-16']) # Categorizes based on server names

plt.figure()
df.plot(x='Machines',y='Power (W)')
plt.savefig('figures/'+session_id+'.png') # Saves graph in figures dir
