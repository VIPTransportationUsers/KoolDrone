
import time
from dronekit import connect, VehicleMode, LocationGlobal

# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).

    while True:
        # print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Drone Reached %d meters\r\n" %(aTargetAltitude))
            break
        time.sleep(1)

def landCopter(landingHeight):
	vehicle.mode = VehicleMode("LAND")
	while True:
#		print(" Altitude: ", vehicle.location.global_relative_frame.alt)
		if vehicle.location.global_relative_frame.alt * 0.95 <= 0:
		    print("Drone Landed at %d meters\r\n" %(landingHeight))
		    break

def chargeAndGatherData():
	print("Charging and Gathering Sensor Data\r\n")
	time.sleep(10)
	print("\r\nCharging Successful\r\n")
	print("Sensor Data Gathered\r\n")

# go to lat lon until it reaches there
def goUntil(lat,lon,height):
	point1 = LocationGlobal(lat,lon, height)
	vehicle.simple_goto(point1)
	while '%.4f'%(vehicle.location.global_relative_frame.lat) != '%.4f'%(lat) and '%.4f'%(vehicle.location.global_relative_frame.lon) != '%.4f'%(lon):
#		print "Lat: %s" % vehicle.location.global_relative_frame.lat
#		print "Lon: %s" % vehicle.location.global_relative_frame.lon		
		time.sleep(2)


############# main program ##############



# print("Set default/target airspeed to 100")
vehicle.airspeed = 1000

# print("Going towards first point")
# point1 = LocationGlobal(40.6736687,-74.0140448, 20)
# vehicle.simple_goto(point1)

arm_and_takeoff(40)

print("Going towards Red Hook\r\n")
goUntil(40.6694736,-74.0031773, 40)
print("Reached Red Hook and landing\r\n")
landCopter(0)
chargeAndGatherData()

arm_and_takeoff(40)

print("Going towards Brownsville\r\n")
goUntil(40.6672546,-73.9117037, 40)
print("Reached Brownsville and landing\r\n")
landCopter(10)
chargeAndGatherData()

arm_and_takeoff(120)

print("Going towards Financial District\r\n")
goUntil(40.7069504,-74.0111085, 120)
print("Reached Financial District and landing\r\n")
landCopter(17)
chargeAndGatherData()

arm_and_takeoff(120)

print("Going towards Hudson Yard\r\n")
goUntil(40.7549202,-74.0010170, 120)
print("Reached Hudson Yard and landing\r\n")
landCopter(3)
chargeAndGatherData()


# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
