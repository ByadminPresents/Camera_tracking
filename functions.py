from pynput.keyboard import Key, Controller
import math

keyboard = Controller()

ThumbstickModes = {
    "Relative" : 0,      #(movement direction depends on direction of view)
    "Static" : 1,        #(static direction of movement)
    "LockedAxis" : 2,    #(on switch locks the axis)
    "Height" : 3         #(move on y axis)
}

def DataExtractor(rawdata: str):
    whitelistsymbols = "-.0123456789"
    extracteddata = ""
    for i in range (0, len(rawdata)):
        if (whitelistsymbols.find(rawdata[i]) >= 0):
            extracteddata += rawdata[i]
    return extracteddata

def MessageSender(message: str):
    for char in "say " + message:
        keyboard.press(char)
        keyboard.release(char)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def CommandPrinter(command: str):
    for char in command:
        keyboard.press(char)
        keyboard.release(char)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def RotationValueTranslate(array: list([float])) -> list([float]):
    if (abs(array[0] - array[1]) > 300):
        if (array[1] >= 0):
            if array[0] < 0:
                array[0] += 360
            if array[2] < 0:
                array[2] += 360
        else:
            if array[0] > 0:
                array[0] -= 360
            if array[2] > 0:
                array[2] -= 360
                            
    if (abs(array[1] - array[2]) > 300):
        if (array[2] >= 0):
            if array[0] < 0:
                array[0] += 360
            if array[1] < 0:
                array[1] += 360
        else:
            if array[0] > 0:
                array[0] -= 360
            if array[1] > 0:
                array[1] -= 360

    if (abs(array[0] - array[2]) > 300):
        if (array[2] >= 0):
            if array[0] < 0:
                array[0] += 360
            if array[1] < 0:
                array[1] += 360
        else:
            if array[0] > 0:
                array[0] -= 360
            if array[1] > 0:
                array[1] -= 360
    return array

def CenterOfSceneModifier(scenecenterxcoord : float, 
scenecenterycoord : float, 
scenecenterzcoord : float, 
current_state_of_left_controller_thumbstick_x_coord : float, 
current_state_of_left_controller_thumbstick_y_coord : float, 
movementmode: int, 
pitch: float, 
lockedpitch: float, 
thumbstickscale : float) -> tuple():
    if (movementmode == ThumbstickModes.get("Relative")):
        thumbstickvectorangle = 0
        thumbstickvectorlength = math.sqrt(current_state_of_left_controller_thumbstick_x_coord**2 + current_state_of_left_controller_thumbstick_y_coord**2)
        if (thumbstickvectorlength != 0):
            if (current_state_of_left_controller_thumbstick_y_coord < 0):
                thumbstickvectorangle = math.pi + math.acos(current_state_of_left_controller_thumbstick_x_coord / thumbstickvectorlength)
            else:
                thumbstickvectorangle = math.pi - math.acos(current_state_of_left_controller_thumbstick_x_coord / thumbstickvectorlength)

        resultvectorangle = pitch * math.pi / 180 + thumbstickvectorangle
        zcoordinateincrement = thumbstickvectorlength * math.cos(resultvectorangle)
        xcoordinateincrement = thumbstickvectorlength * math.cos(math.pi / 2 - resultvectorangle)

        scenecenterxcoord -= xcoordinateincrement * thumbstickscale
        scenecenterzcoord += zcoordinateincrement * thumbstickscale
    elif (movementmode == ThumbstickModes.get("Static")):
        scenecenterxcoord -= current_state_of_left_controller_thumbstick_y_coord * thumbstickscale
        scenecenterzcoord -= current_state_of_left_controller_thumbstick_x_coord * thumbstickscale
    elif (movementmode == ThumbstickModes.get("LockedAxis")):
        thumbstickvectorlength = math.sqrt(current_state_of_left_controller_thumbstick_x_coord**2 + current_state_of_left_controller_thumbstick_y_coord**2)
        if (thumbstickvectorlength != 0):
            if (current_state_of_left_controller_thumbstick_x_coord < 0):
                zcoordinateincrement = thumbstickvectorlength * math.cos(lockedpitch * math.pi / 180)
                xcoordinateincrement = thumbstickvectorlength * math.cos(math.pi / 2 - lockedpitch * math.pi / 180)
            elif (current_state_of_left_controller_thumbstick_x_coord > 0):
                zcoordinateincrement = thumbstickvectorlength * math.cos(math.pi + lockedpitch * math.pi / 180)
                xcoordinateincrement = thumbstickvectorlength * math.cos(1.5 * math.pi - lockedpitch * math.pi / 180)

            scenecenterxcoord -= xcoordinateincrement * thumbstickscale
            scenecenterzcoord += zcoordinateincrement * thumbstickscale
    elif (movementmode == ThumbstickModes.get("Height")):
        thumbstickvectorlength = math.sqrt(current_state_of_left_controller_thumbstick_x_coord**2 + current_state_of_left_controller_thumbstick_y_coord**2)
        if (thumbstickvectorlength != 0):
            if (current_state_of_left_controller_thumbstick_x_coord < 0):
                scenecenterycoord += thumbstickvectorlength * thumbstickscale
            elif (current_state_of_left_controller_thumbstick_x_coord > 0):
                scenecenterycoord -= thumbstickvectorlength * thumbstickscale
    return (scenecenterxcoord, scenecenterycoord, scenecenterzcoord)