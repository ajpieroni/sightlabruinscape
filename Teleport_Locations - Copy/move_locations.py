from sceneConfig import *

"""
Right Mouse button or Grip button on controller to turn on/off highlighter
Left Mouse click or Trigger Press to select menu item
Or use hand model to virtually press the buttons. Change controller input names to the ones in
your vizconnect file. Right thumbstick to hide/show menu and bring in focus
"""

#Note remove this code if copying this code into the root folder of your project
import os
original_cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

import viz, vizfx, vizconnect, viztask
from utils import sightlab
from settings import *

sightlab.is_GUI = 1

transportNode = vizconnect.getTransport('main_transport').getNode3d()

# lOCATIONS
# Custom teleport locations and orientations
# Renamed to avoid conflicts with existing settings
# Custom location and orientation 1 (amb1)
CUSTOM_LOCATION1 = [-1.583414912223816, 0.10996247082948685, -3.5207571983337402]
CUSTOM_ORIENTATION1 = [88.53834533691406, -0.0, 0.0]
# Custom location and orientation 2 (amb3)
CUSTOM_LOCATION2 = [17.671348571777344, -52.68771743774414, 172.31236267089844]
CUSTOM_ORIENTATION2 = [0.0, -0.0, 0.0]
# Custom location and orientation 3
CUSTOM_LOCATION3 = [-0.8684664964675903, 0.10996247082948685, -6.075732707977295]
CUSTOM_ORIENTATION3 = [88.53834533691406, -0.0, 0.0]
# Updated locations list with custom locations

locations = [
	(CUSTOM_LOCATION1, CUSTOM_ORIENTATION1),
	(CUSTOM_LOCATION2, CUSTOM_ORIENTATION2),
	(CUSTOM_LOCATION3, CUSTOM_ORIENTATION3)
]

def toggleLocation():
	transportNode.setPosition(TELEPORT_LOCATION1)
	transportNode.setEuler(TELEPORT_ORIENTATION1)
vizact.onkeydown('1',toggleLocation)

def toggleLocation2():
	transportNode.setPosition(TELEPORT_LOCATION2)
	transportNode.setEuler(TELEPORT_ORIENTATION2)
vizact.onkeydown('2',toggleLocation2)
def toggleLocation3():
	transportNode.setPosition(TELEPORT_LOCATION3)
	transportNode.setEuler(TELEPORT_ORIENTATION3)
vizact.onkeydown('3',toggleLocation3)

# Current index of the location
current_location_index = 0

def changeLocation():

	global current_location_index

	# Get the next location and orientation
	location, orientation = locations[current_location_index]
	# Changing location to current location indexc
	print("Changing location to: ", current_location_index+1)
	
	# Move the transport node to the new location and orientation
	transportNode.setPosition(location)
	transportNode.setEuler(orientation)

	# Update the index for the next call
	current_location_index = (current_location_index + 1) % len(locations)

# Schedule the location change every X seconds (e.g., 5 seconds)


def sightLabExperiment():
	#env = sightlab.objects[0]
	#env.optimize(viz.OPT_REMOVE_REDUNDANT_NODES)
	#env.hint(viz.VBO_HINT)
	
	def getPosition():
		print(transportNode.getPosition())
		print(transportNode.getEuler())

	vizact.onkeydown('t',getPosition) 


		
	yield viztask.waitKeyDown(' ')
	# Wait to start timer until the experiment has started. Currently, the timer is set for 30 seconds.
	vizact.ontimer(30, changeLocation)
	
viztask.schedule(sightlab.experiment)
viztask.schedule(sightLabExperiment)

