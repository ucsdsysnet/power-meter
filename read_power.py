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


##
# Schedules next power meter reading and also takes measurements from each
# of the four machines and writes the data to the file in ./data delimited
# by commas
#
# @param sc is the scheduler used to manage function calls
##
def read_power(sc):
  if time.time() < end: # Schedule another reading in 1 sec if time is valid
    s.enter(timeInt, 1, read_power, (sc,))
  power = instr.ask("measure:scalar:power:real? 0") # Ask for readings on 4 channels
  f.write(power+",") # Writes data to file
  f.flush() # Flushes buffer so data written immediately

# Define scheduler and collect user input for timeframe
s = sched.scheduler(time.time, time.sleep)
dur = float(raw_input("Enter number of seconds: ")) # Asks for user input
timeInt = float(raw_input("Enter time interval in seconds: ")) # Asks for interval
end = time.time() + dur # End time is (system time) + (number of seconds)

# Schedule execution over user-inputted timeframe
s.enter(0, 1, read_power, (s,)) # First measurement scheduled immediately
s.run() # Run scheduler

# Read delimited session string from file
f = open('data/session-'+session_id+'.txt', 'r') # Opens data file
data = f.read().split(",") # Delimits data using commas
del data[-1] # Deletes extra comma at the end

# Coverts data to array format
data = [float(i) for i in data] # Puts data into array format

# Creates array for the x-axis second intervals
secs = []
count = 0
while (count <= dur): # Appends time to arrary, increments by timeInt
  secs.append(count)
  count = count + timeInt

# Arrays for the y-axis power readings
c1 = [] # c09-13
c2 = [] # c09-14
c3 = [] # c09-15
c4 = [] # c09-16
i = 0
while (i < len(data)): # Places data into server-appropriate array
  if (i % 4 == 0): # First reading for c09-13
    c1.append(data[i])
  elif (i % 4 == 1): # Second reading for c09-14
    c2.append(data[i])
  elif (i % 4 == 2): # Third reading for c09-15
    c3.append(data[i])
  elif (i % 4 == 3): # Fourth reading for c09-16
    c4.append(data[i])
  i = i + 1

# Plots lines for the four servers
plt.ylim(85, 150)
plt.plot(secs, c1, color = 'g', label = 'c09-13')
plt.plot(secs, c2, color = 'r', label = 'c09-14')
plt.plot(secs, c3, color = 'orange', label = 'c09-15')
plt.plot(secs, c4, color = 'b', label = 'c09-16')

# Labels axes and adds graph title
plt.xlabel('Time (sec)')
plt.ylabel('Power (W)')
plt.title('Server Power Usage Over Time (timeInt = ' + str(timeInt) + ' secs)')

plt.legend(loc = 'upper right') # Adds legend
plt.margins(x = 0) # Decreases margins

plt.savefig('figures/'+session_id+'.png') # Saves graph in figures dir
