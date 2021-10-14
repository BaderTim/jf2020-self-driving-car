"""
	Created by Tim Bader
	For Jugend Forscht 2020
	© Tim Bader, 2020
"""
import math
import keyboard
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)


#STATIC VARIABLES
max_steering_angle = 40
sensor_length = 15
max_motor_torque = 1
loop_time = 0.0


def get_sensor_data():
	"""
		returns: list with a length of 3 containing float values
		
		Calculates distances of the 3 ultrasonic sensor 
		detections and returns them.
	"""
    sensor_data = [0.0, 0.0, 0.0]
    
    GPIO.setmode(GPIO.BCM)  
    TRIG1 = 23
    TRIG2 = 22
    TRIG3 = 27
    ECHO1 = 18
    ECHO2 = 17
    ECHO3 = 24
    
    pulse_start1 = time.time()
    pulse_end1 = time.time()
    
    pulse_start2 = time.time()
    pulse_end2 = time.time()
    
    pulse_start3 = time.time()
    pulse_end3 = time.time()
    
    GPIO.setup(TRIG1, GPIO.OUT)
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(TRIG3, GPIO.OUT)
    GPIO.setup(ECHO1, GPIO.IN)
    GPIO.setup(ECHO2, GPIO.IN)
    GPIO.setup(ECHO3, GPIO.IN)
    
    GPIO.output(TRIG1, False)
    time.sleep(0.06)
    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)
    
    while GPIO.input(ECHO1)==0:
        pulse_start1 = time.time()
    while GPIO.input(ECHO1)==1:
        pulse_end1 = time.time()
    
    GPIO.output(TRIG2, False)
    time.sleep(0.06)
    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)
    
    while GPIO.input(ECHO2)==0:
        pulse_start2 = time.time()
        
    while GPIO.input(ECHO2)==1:
        pulse_end2 = time.time()
        
    GPIO.output(TRIG3, False)
    time.sleep(0.06)
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)
    
    while GPIO.input(ECHO3)==0:
        pulse_start3 = time.time()
        
    while GPIO.input(ECHO3)==1:
        pulse_end3 = time.time()
        
    pulse_duration1 = pulse_end1 - pulse_start1
    distance1 = pulse_duration1 * 17150
    distance1 = round(distance1, 2)
    print ("Right: ",distance1,"cm")
    
    pulse_duration2 = pulse_end2 - pulse_start2
    distance2 = pulse_duration2 * 17150
    distance2 = round(distance2, 2)
    print ("Left: ",distance2,"cm")
    
    pulse_duration3 = pulse_end3 - pulse_start3
    distance3 = pulse_duration3 * 17150
    distance3 = round(distance3, 2)
    print ("Mid: ",distance3,"cm")
    GPIO.cleanup()
    sensor_data[2] = distance1
    sensor_data[0] = distance2
    sensor_data[1] = distance3
    return sensor_data
    

def get_distances():
	"""
		returns: list with a length of 3 containing float values
		
		Removes certain anomalies from the raw sensor data 
		calculations and normaizes them
	"""
    dist = [0.0, 0.0, 0.0]

    sensor_input = get_sensor_data()
    
    left = sensor_input[0]
    mid = sensor_input[1]
    right = sensor_input[2]

    if left >= sensor_length:
        left = 0.0
    else:
        left = 1 - left/sensor_length

    if mid >= sensor_length:
        mid = 0.0
    else:
        mid = 1 - mid / sensor_length

    if right >= sensor_length:
        right = 0.0
    else:
        right = 1 - right / sensor_length

    dist[0] = left
    dist[1] = mid
    dist[2] = right
    return dist


def move(l, r):
    """
		r:	right motor speed
		l:	left motor speed
		
		Executes motor speed changes by getting the initial speed
		the network wants them to be at, evaluating those and then
		calling motor functions.
	"""
    print("Left motor speed: " + str(l))
    print("Right motor speed: " + str(r))
    if l > r + 0.3:
        right(l-r)
    elif r > l + 0.3:
        left(r-l)
    else:
        forward(0.3)


def init_motors():
	"""
		Initializes motors by changing the voltage of the
		GPIO outputs.
	"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(31, GPIO.OUT)
    GPIO.setup(29, GPIO.OUT)


def forward(tf):
	"""
		Moves forward for a certain time.
	"""
    init_motors()
    GPIO.output(29, False)
    GPIO.output(31, True)
    GPIO.output(36, True)
    GPIO.output(37, False)
    time.sleep(tf)
    GPIO.cleanup()
    
	
def backward(tf):
	"""
		Moves backwards for a certain time.
	"""
    init_motors()
    GPIO.output(29, True)
    GPIO.output(31, False)
    GPIO.output(36, False)
    GPIO.output(37, True)
    time.sleep(tf)
    GPIO.cleanup()
    
	
def left(tf):
	"""
		Moves left for a certain time.
	"""
    init_motors()
    GPIO.output(29, True)
    GPIO.output(31, False)
    GPIO.output(36, True)
    GPIO.output(37, False)
    time.sleep(tf)
    GPIO.cleanup()
    
	
def right(tf):
	"""
		Moves right for a certain time.
	"""
    init_motors()
    GPIO.output(29, False)
    GPIO.output(31, True)
    GPIO.output(36, False)
    GPIO.output(37, True)
    time.sleep(tf)
    GPIO.cleanup()
    

def sigmoid(x):
	"""
		x: rational number
		returns: value between -1 and 1
	"""
    return 1/(1 + math.exp(-float(x)))


def network(inputs):
	"""
		inputs: list of floats with length of 3 (distances)
		returns: network results
	"""
    parameters = [3, 6, 2] #nn architecture
    #best generation of weights from pre-trained neural network
    weights = [[[-0.980175495147705, -0.186096787452698, 0.80379843711853, 0.948149442672729, -0.180595278739929, -0.904619455337524],
                [-0.30886709690094, -0.582291841506958, -0.6927809715271, 0.557246446609497, 0.611737489700317, -0.190137267112732],
                [-0.756172895431519, 0.545915603637695, -0.368541121482849, -0.635722160339355, 0.956294536590576, 0.745823383331299]],

                [[-0.972720861434937, 0.146159529685974],
                [0.563815593719482, 0.683503150939941],
                [0.439907282590866, 0.566266775131226],
                [0.725433349609375, -0.598716497421265],
                [-0.830876111984253, -0.262409806251526],
                [-0.68674635887146, -0.45588481426239]]]
    for i in range(2): #layers
        outputs = [0.0] * parameters[i+1]
        for j in range(len(inputs)): #neurons
            for k in range(len(outputs)): #weight of each neuron
                outputs[k] += inputs[j] * weights[i][j][k] #first part of math is multiplication of input and weight
        inputs = [0.0] * len(outputs)
        for l in range(len(outputs)):
            inputs[l] = sigmoid(outputs[l] * 5) #second part of math is sigmoid function, output becomes input for next loop
    return inputs


"""
	MAIN LOOP
"""

print("WELCOME TO CAR AI made by Tim Bader")
print("Controls: X = exit, P = pause, R = resume")
print("Press S to start.")
keyboard.wait("s")
while True:
    results = network(get_distances())
    steering = max_steering_angle*(results[0]-0.5)*2
    speed = max_motor_torque*results[1]+0.2

    #combining speed and steering variables to one with math
    #because real wheels are static and cannot rotate
    l = speed
    r = speed
    if steering > 0.1: #right
        r = r - steering/100
    if steering < -0.1: #left
        l = l + steering/100
    move(l, r)

    #PAUSE
    if keyboard.is_pressed("p"):
        print("Paused. Press R to resume.")
        keyboard.wait("r")
    #EXIT
    if keyboard.is_pressed("x"):
        print("Exiting...")
        break
    time.sleep(loop_time)
