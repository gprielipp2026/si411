#!/usr/bin/env python3
# vmSim.py
import sys
import math

# Constants for the various algorithsm we may use
FIFO  = 10
LRU   = 11
AGING = 12

NUM_AGE_BITS = 10   # For AGING, how many bits should each counter hold?


# A 'MemOp' represents a single load or store memory operation (one line of the trace file)
class MemOp:

    def __init__ (self, isStore, addressInHex, instsBetween):
        self.isStore      = int(isStore)
        self.virtAddress  = int(addressInHex, 16)  # assumes is base-16 (hex)
        self.instsBetween = int(instsBetween)
	
    def __str__(self):
        return "%d %08x %d" % (self.isStore, self.virtAddress, self.instsBetween)


# A 'Frame' represents a single physical frame of memory
class Frame:
    def __init__ (self, isValid, vpn):
        self.isValid     = isValid
        self.vpn         = vpn    # vpn set to -1 when frame is not valid
        self.tolu        = 0
        self.counter     = 0
        self.referenced  = 0
        

# Process command line arguments and return (filename, numFrames, alg, debug)
#  [where 'alg' is one of the constants listed above]
# You should NOT need to change this function
def processArguments():
    # Get arguments
    if len(sys.argv) != 5:
        print ("usage: python3 vmSim.py <filename> <numFrames> <algName=FIFO|LRU|AGING> <debug=0|1|2>")
        sys.exit(-1)
    filename  = sys.argv[1]
    numFrames = int(sys.argv[2])
    algName   = sys.argv[3]
    debug     = int(sys.argv[4])

    if not (numFrames > 1):
        print ("Invalid numFrames", numFrames)
        sys.exit(-1)
        
    if algName == "FIFO":
        alg = FIFO
    elif algName == "LRU":
        alg = LRU
    elif algName == "AGING":
        alg = AGING
    else:
        print ("Invalid algName", algName)
        sys.exit(-1)
        
    if not (debug == 0 or debug == 1 or debug == 2 or debug == 3):
        print ("Invalid debug argument ",debug)
        sys.exit(-1)

    print ("Running vmSim on file",filename,"numFrames",numFrames,"alg",algName,"debug",debug)
        
    return (filename, numFrames, alg, debug)

def replFIFO(prevEvicted, frames, vpn, clock):
    idx = (prevEvicted + 1) % len(frames)
    evicted = frames[idx]
    frames[idx] = Frame(isValid=True, vpn=vpn)
    return idx, evicted

def replLRU(prevEvicted, frames, vpn, clock):
    # find next evict
    idx = 0
    for i in range(len(frames)):
        if not frames[i].isValid: # get the first empty slot
            idx = i
            break
        if frames[i].tolu < frames[idx].tolu:# or the least recently used
            idx = i

    replaced = frames[idx]
    
    frames[idx] = Frame(isValid=True, vpn=vpn)
    frames[idx].tolu = clock

    return idx, replaced

def replAging(prevEvicted, frames, vpn, clock):
    idx = 0
    for i in range(len(frames)):
        if not frames[i].isValid: # empty slot
            idx = i
            break
        elif frames[i].counter < frames[idx].counter: 
            idx = i 

    replaced = frames[idx]

    frames[idx] = Frame(isValid=True, vpn=vpn)
    frames[idx].referenced = 1
    frames[idx].counter = 1 << 9

    return idx, replaced

def updateFIFO(frames, pfn, clock):
    pass

def updateLRU(frames, pfn, clock):
    frames[pfn].tolu = clock

def updateAging(frames, pfn, clock):
    frames[pfn].referenced = 1
    if clock % 50 == 0:
        for frame in frames:
            frame.counter = (frame.referenced << 9) | (frame.counter >> 1)
            frame.referenced = 0

if __name__=="__main__":

    # Get arguments and open trace file
    (filename, numFrames, alg, debug) = processArguments()        
    file = open(filename,'r')
    if not file:
        print ("Error", filename, "not found!")
        sys.exit(-1)
        
    replace = {
        FIFO: replFIFO,
        LRU: replLRU,
        AGING: replAging
    }

    update = {
        FIFO: updateFIFO,
        LRU: updateLRU,
        AGING: updateAging,
    }

    # 32 bit address, size(page) = 1024 bytes = 2^10 bytes
    # max frame address = num frames - 1 (bc it's 0 indexed)
    # num pages = 2^32 / num frames => page address offset => virtual page number
    sizePage = 1024
    sizeFrame = sizePage
    physMemSize = sizeFrame * numFrames
    memBitsNeeded = int(math.log2(physMemSize))
    # numBitsOffset = 10
    # offsetMask = 0
    # for i in range(numBitsOffset):
    #     offsetMask <<= 1
    #     offsetMask |= 1
        # print(f'offsetMask = {len(bin(offsetMask))-2} {bin(offsetMask)}')

    # vpnMask = 0
    # for i in range(32 - numBitsOffset):
    #     vpnMask |= 1 << (32 - i - 1)
        # print(f'vpnMask = {len(bin(vpnMask))-2} {bin(vpnMask)}')
    
    # print(f'{offsetMask: 08x}\t{vpnMask: 08x}')
    # page frame number = ??
    
    # Create the table to represent physical frames, initially all empty
    frames = []
    for ii in range(numFrames):
        frames.append(Frame(isValid=False, vpn=-1))

    numOps = numFaults = 0
    evicted = -1
    indexOld = 0

    # Read each line and send to simulator
    for line in file:
        # Update stats and check for early stopping -- you should NOT need to change this part
        numOps = numOps + 1
        if debug >= 2 and numOps >= 10000:      # stop early for debug mode 2
            break

        # Read next memory operation from file -- you should NOT need to change this part
        line_array = line.split()
        memOp = MemOp(line_array[1], line_array[2], line_array[3])   # start at 1 to skip over '#' at start of line

        # Examine virtual address to split into vpn and offset (yes, changes needed here!)
        vpn    = (memOp.virtAddress & 0xfffffc00) >> 10    # TODO (for part 1) -- you must compute this "virtual page number" from memOp.virtAddress !
        offset =  memOp.virtAddress & 0x000003ff    # TODO (for part 1) -- you must compute this "page offset"         from memOp.virtAddress !
        if debug >= 1:
            print ("time %d virtual address %08x  vpn: %06x offset: %03x" % (numOps, memOp.virtAddress, vpn, offset)) 
            
        pfn = 0
        for i, frame in enumerate(frames):
            # TODO (for part 2) -- make changes here to see if page 'vpn' is already in physical memory (look in 'frames')
            if frame.vpn == vpn:
                frameFound = True 
                pfn = i
                break
        else:
            # TODO (for part 2) -- handle page fault if not
            # only executes if frame is not found
            evicted, frameEvicted = replace[alg](evicted, frames, vpn, numOps)
            pfn = evicted
            if debug == 3:        
                print ("    picked frame %02x with counter (in hex) %x to evict" % (evicted, frameEvicted.counter) )
            if debug >= 2:
                print(f'    Page fault!  Will load page into frame{evicted: 03x}') # testing: \t\t{", ".join(map(lambda frame: str(frame.tolu), frames))}
            numFaults += 1
            if debug >= 2:
                if frameEvicted.isValid:
                    print(f'    (after evicting vpn{frameEvicted.vpn: 07x} from that frame)')
                else:
                    print(f'    (no eviction was needed)')
            indexOld = evicted

        # TODO (for part 2) -- update any reference/timing stats for page that was just used     
        update[alg](frames, pfn, numOps)

        if debug >= 2:
            sizeOffset = 10 # <-- from page
            # Print the physical address
            physAddress = (pfn << sizeOffset ) | offset # TODO (for part 2) -- compute physical address here, based what physical frame applies for this memory access
            # TODO (for part 2) -- uncomment this print statement
            print ("    physical address %04x (pfn: %02x offset: %03x)" % (physAddress, pfn, offset) )


        # Print some stats -- you should NOT need to change this part
        if numOps % 100000 == 0:
            print ("faults", numFaults, " of ", numOps, " faultRate: ", float(numFaults) / numOps)

        
    # Print some stats -- you should NOT need to change this part
    print ("faults", numFaults, " of ", numOps, " faultRate: ", float(numFaults) / numOps)

            
    
