from sceneConfig import *

"""
Right Mouse button or Grip button on controller to turn on/off highlighter
Left Mouse click or Trigger Press to select menu item
Or use hand model to virtually press the buttons. Change controller input names to the ones in
your vizconnect file. Right thumbstick to hide/show menu and bring in focus
Press 'm' key or right thumbstick button on controller to reposition menu in front of you

"""

#Note remove this code if copying this code into the root folder of your project
import os
original_cwd = os.getcwd()
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))

import viz, vizfx, vizconnect, viztask, vizinfo, vizproximity
from utils import sightlab, selector
from settings import *
from tools import highlighter
from utils.tablet_manager import TabletManager

vizinfo.InfoPanel()

sightlab.is_GUI = 1

print("Ran 3d tablet menu")

#Get names from vizonnect for inputs
r_hand_input_name = 'r_hand_input'
l_hand_input_name = 'l_hand_input'

tablet = vizfx.addChild('utils/resources/objects/VR_Menu.osgb')
tablet.setPosition(0, 1.2, 1.5)
button1= tablet.getChild('button1_target')
button2 = tablet.getChild('button2_target')
buttonPressed1= tablet.getChild('button1')
buttonPressed1.visible(viz.OFF)
buttonPressed2 = tablet.getChild('button2')

tabletMain = tablet.getChild('main')

selector.tool.setItems([button1,button2])
selector.tool2.setItems([button1,button2])
selector.tool.setHighlightMode(highlighter.MODE_NONE)
selector.tool2.setHighlightMode(highlighter.MODE_NONE)

transportNode = vizconnect.getTransport('main_transport').getNode3d()
rightHandInput = vizconnect.getInput(r_hand_input_name).getRaw()
if not VIZCONNECT_CONFIGS[sightlab.configuration] == "Desktop":
    leftHandInput = vizconnect.getInput(l_hand_input_name).getRaw()
    selector.tool.setParent(transportNode)
    selector.tool2.setParent(transportNode)

beep = viz.addAudio('utils/resources/audio/beep.wav')

sightlab.grabObjectsDict["tablet"] = tablet

manager = vizproximity.Manager()
#manager.setDebug(viz.ON)
#Add hands or fingers as target
avatar= vizconnect.getAvatar()
rhand = avatar.getAttachmentPoint('r_hand').getNode3d()
rhand_target = vizproximity.Target(rhand)

lhand = avatar.getAttachmentPoint('l_hand').getNode3d()
lhand_target = vizproximity.Target(lhand)

manager.addTarget(lhand_target)
manager.addTarget(rhand_target)

button1Sensor = vizproximity.addBoundingBoxSensor(button1)
manager.addSensor(button1Sensor)
button2Sensor = vizproximity.addBoundingBoxSensor(button2)
manager.addSensor(button2Sensor)

def toggleLocation():
	transportNode.setPosition(TELEPORT_LOCATION1)
	transportNode.setEuler(TELEPORT_ORIENTATION1)
vizact.onkeydown('1',toggleLocation)

def toggleLocation2():
	transportNode.setPosition(TELEPORT_LOCATION2)
	transportNode.setEuler(TELEPORT_ORIENTATION2)
vizact.onkeydown('2',toggleLocation2)

def pressButtonOne(e):
    global currentHighlightedObject
    currentHighlightedObject = button1  # Set the global variable to button1
    confirmTarget(None)  # Call confirmTarget with None as the event argument
    
    # Check which hand triggered the sensor
    if e.target == rhand_target and not VIZCONNECT_CONFIGS[sightlab.configuration] == "Desktop":
        rightHandInput.setVibration(0.1, frequency=1.0, amplitude=0.5)
    elif e.target == lhand_target and not VIZCONNECT_CONFIGS[sightlab.configuration] == "Desktop":
        leftHandInput.setVibration(0.1, frequency=1.0, amplitude=0.5)
    transportNode.setPosition(TELEPORT_LOCATION1)
    transportNode.setEuler(TELEPORT_ORIENTATION1)	
    beep.play()

def pressButtonTwo(e): 
    global currentHighlightedObject
    currentHighlightedObject = button2  # Set the global variable to button2
    confirmTarget(None)  # Call confirmTarget with None as the event argument
    
    # Check which hand triggered the sensor
    if e.target == rhand_target and not VIZCONNECT_CONFIGS[sightlab.configuration] == "Desktop":
        rightHandInput.setVibration(0.1, frequency=1.0, amplitude=0.5)
    elif e.target == lhand_target and not VIZCONNECT_CONFIGS[sightlab.configuration] == "Desktop":
        leftHandInput.setVibration(0.1, frequency=1.0, amplitude=0.5)
    
    transportNode.setPosition(TELEPORT_LOCATION2)
    transportNode.setEuler(TELEPORT_ORIENTATION2)	
    beep.play()

manager.onEnter(button1Sensor, pressButtonOne)
manager.onEnter(button2Sensor, pressButtonTwo)

# Global variables and key event handlers
isConfirmingTarget = False
currentHighlightedObject = None
    
button_name_map = {button1: 'button1_target', button2: 'button2_target'}

def confirmTarget(e):
    global isConfirmingTarget, currentHighlightedObject
    isConfirmingTarget = True
    if currentHighlightedObject in [button1, button2]:
        print(f'{button_name_map[currentHighlightedObject]} pressed')
        if currentHighlightedObject == button1:
            if buttonPressed1 is not None:
                buttonPressed1.visible(viz.ON)
                buttonPressed2.visible(viz.OFF)  # Set buttonPressed2 visibility to OFF
                tabletMain.visible(viz.OFF)
                transportNode.setPosition(TELEPORT_LOCATION1)
                transportNode.setEuler(TELEPORT_ORIENTATION1)
        elif currentHighlightedObject == button2:
            if buttonPressed2 is not None:
                buttonPressed2.visible(viz.ON)
                transportNode.setPosition(TELEPORT_LOCATION2)
                transportNode.setEuler(TELEPORT_ORIENTATION2)
                buttonPressed1.visible(viz.OFF)  # Set buttonPressed1 visibility to OFF
                tabletMain.visible(viz.OFF)
        beep.play()
    isConfirmingTarget = False

# Highlight event callback
def onHighlight(e):
    global currentHighlightedObject
    currentHighlightedObject = e.new
    if isConfirmingTarget and currentHighlightedObject in [button1, button2]:
        print(f'{currentHighlightedObject} is highlighted')

viz.callback(viz.getEventID('triggerPress'), confirmTarget)
viz.callback(viz.getEventID('triggerPressLeft'), confirmTarget)
viz.callback(highlighter.HIGHLIGHT_EVENT, onHighlight)

def sightLabExperiment():
    yield viztask.waitKeyDown(' ')
    
    customOffsetDistance = 0.7  # Change this value as needed
    tabletManager = TabletManager(tablet, offsetDistance=customOffsetDistance)
    
    def getPosition():
        print(transportNode.getPosition())
        print(transportNode.getEuler())

    vizact.onkeydown('t',getPosition)
        
    yield viztask.waitKeyDown(' ')
    
viztask.schedule(sightlab.experiment)
viztask.schedule(sightLabExperiment)

