import vxi11, sched, time, random, string

# Define instrument
instr = vxi11.Instrument("172.19.222.92","gpib0,12")
print(instr.ask("*IDN?"))

# Generate session id and create output file
session_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(10)])
f = open("data/session-"+session_id+".txt", "w")

# Store session id in a file
name = open("data/id.txt", "w")
name.write("%s" % session_id)
name.close()

print("Beginning read session: "+session_id)

# Read power over time interval (set to 1s)
s = sched.scheduler(time.time, time.sleep)
def read_power(sc):
    f.write(instr.ask("measure:scalar:power:real? 0")+",")
    f.flush()
    s.enter(1, 1, read_power, (sc,))

s.enter(1, 1, read_power, (s,))
s.run()
