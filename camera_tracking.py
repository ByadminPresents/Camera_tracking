import ctypes
import time
import xr
import math

import functions

with xr.ContextObject(
    instance_create_info=xr.InstanceCreateInfo(
        enabled_extension_names=[
            xr.KHR_OPENGL_ENABLE_EXTENSION_NAME,
        ],
    ),
) as context:
    left_controller_path = (xr.Path * 1)(
        xr.string_to_path(context.instance, "/user/hand/left"),
    )

    controller_pose_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.POSE_INPUT,
            action_name="hand_pose",
            localized_action_name="Hand Pose",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_a_button_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.BOOLEAN_INPUT,
            action_name="left_controller_a_button_press",
            localized_action_name="Left Controller A Button Press",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_b_button_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.BOOLEAN_INPUT,
            action_name="left_controller_b_button_press",
            localized_action_name="Left Controller B Button Press",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_thumbstick_x_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.FLOAT_INPUT,
            action_name="left_controller_thumbstick_x_coord",
            localized_action_name="Left Controller Thumbstick X Coord",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_thumbstick_y_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.FLOAT_INPUT,
            action_name="left_controller_thumbstick_y_coord",
            localized_action_name="Left Controller Thumbstick Y Coord",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_thumbstick_click_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.BOOLEAN_INPUT,
            action_name="left_controller_thumbstick_click",
            localized_action_name="Left Controller Thumbstick Click",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    left_controller_trigger_value_action = xr.create_action(
        action_set=context.default_action_set,
        create_info=xr.ActionCreateInfo(
            action_type=xr.ActionType.FLOAT_INPUT,
            action_name="left_controller_trigger",
            localized_action_name="Left Controller Trigger",
            count_subaction_paths=len(left_controller_path),
            subaction_paths=left_controller_path,
        ),
    )
    suggested_bindings = (xr.ActionSuggestedBinding * 6)(
        xr.ActionSuggestedBinding(
            action=controller_pose_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/grip/pose",
            ),
        ),
        xr.ActionSuggestedBinding(
            action=left_controller_a_button_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/a/click",
            ),
        ),
        xr.ActionSuggestedBinding(
            action=left_controller_b_button_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/b/click",
            ),
        ),
        xr.ActionSuggestedBinding(
            action=left_controller_thumbstick_x_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/thumbstick/x",
            ),
        ),
        xr.ActionSuggestedBinding(
            action=left_controller_thumbstick_y_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/thumbstick/y",
            ),
        ),
        xr.ActionSuggestedBinding(
            action=left_controller_thumbstick_click_action,
            binding=xr.string_to_path(
                instance=context.instance,
                path_string="/user/hand/left/input/thumbstick/click",
            )
        ),

    )
    xr.suggest_interaction_profile_bindings(
        instance=context.instance,
        suggested_bindings=xr.InteractionProfileSuggestedBinding(
            interaction_profile=xr.string_to_path(
                context.instance,
                "/interaction_profiles/valve/index_controller",
            ),
            count_suggested_bindings=len(suggested_bindings),
            suggested_bindings=suggested_bindings,
        ),
    )
    action_spaces = [
        xr.create_action_space(
            session=context.session,
            create_info=xr.ActionSpaceCreateInfo(
                action=controller_pose_action,
                subaction_path=left_controller_path[0],
            ),
        ),
    ]

    scenecenterxcoord = 192.5
    scenecenterycoord = 0
    scenecenterzcoord = 19.5

    dimensionsscale = 7
    heightscale = 2.7

    thumbstickscale = 0.25

    filepath = "C:\\Users\\ByadminPresents\\Desktop\\file.txt"

    firstxcoord = -90.0
    firstycoord = -90.0
    firstzcoord = -90.0

    arrlocx = []
    arrlocy = []
    arrlocz = []

    arrpitch = []
    arryaw = []

    starttracking = False

    startrecording = False
    recordingstarttime = 0

    thumbstickmode = 0

    lockedpitch = 0


    # Loop over the render frames
    for frame_index, frame_state in enumerate(context.frame_loop()):
        ingameticktime = time.time()
        if context.session_state == xr.SessionState.FOCUSED:
            active_action_set = xr.ActiveActionSet(
                action_set=context.default_action_set,
                subaction_path=xr.NULL_PATH,
            )
            xr.sync_actions(
                session=context.session,
                sync_info=xr.ActionsSyncInfo(
                    count_active_action_sets=1,
                    active_action_sets=ctypes.pointer(active_action_set),
                ),
            )

            left_controller_a_button_press = xr.get_action_state_boolean(
                session=context.session,
                get_info=xr.ActionStateGetInfo(action=left_controller_a_button_action)
            )
            left_controller_b_button_press = xr.get_action_state_boolean(
                session=context.session,
                get_info=xr.ActionStateGetInfo(action=left_controller_b_button_action)
            )
            left_controller_thumbstick_x_coord = xr.get_action_state_float(
                session=context.session,
                get_info=xr.ActionStateGetInfo(action=left_controller_thumbstick_x_action)
            )
            left_controller_thumbstick_y_coord = xr.get_action_state_float(
                session=context.session,
                get_info=xr.ActionStateGetInfo(action=left_controller_thumbstick_y_action)
            )
            left_controller_thumbstick_click = xr.get_action_state_boolean(
                session=context.session,
                get_info=xr.ActionStateGetInfo(action=left_controller_thumbstick_click_action)
            )

            found_count = 0
            for index, space in enumerate(action_spaces):
                space_location = xr.locate_space(
                    space=space,
                    base_space=context.space,
                    time=frame_state.predicted_display_time,
                )

                if left_controller_a_button_press.changed_since_last_sync and left_controller_a_button_press.current_state:
                    if starttracking == False:
                        starttracking = True
                        functions.MessageSender("Tracking has been started")
                    else: 
                        starttracking = False
                        functions.MessageSender("Tracking has been stopped")

                if left_controller_b_button_press.changed_since_last_sync and left_controller_b_button_press.current_state:
                    if starttracking == False:
                        functions.MessageSender("Error: Tracking isn't active")
                    elif startrecording == False and recordingstarttime == 0:
                        functions.MessageSender("Recording will start in: 3")
                        file = open(filepath, "a")
                        secondsbeforerecodingstarts = 2
                        currenttick = 0
                        recordingstarttime = time.time()
                    elif startrecording == True:
                        functions.MessageSender("Recording has been ended")
                        file.close()
                        startrecording = False

                if left_controller_thumbstick_click.changed_since_last_sync and left_controller_thumbstick_click.current_state:
                    thumbstickmode += 1
                    if (thumbstickmode == functions.ThumbstickModes.get("Static")): functions.MessageSender("Thumbstick mode: Static")
                    if (thumbstickmode == functions.ThumbstickModes.get("LockedAxis")): 
                        functions.MessageSender("Thumbstick mode: LockedAxis")
                        lockedpitch = -1000
                    if (thumbstickmode == functions.ThumbstickModes.get("Height")): functions.MessageSender("Thumbstick mode: Height")
                    if (thumbstickmode == 4):
                        functions.MessageSender("Thumbstick mode: Relative")
                        thumbstickmode = 0

                if recordingstarttime != 0:
                    if (secondsbeforerecodingstarts == 2 and 1 <= time.time() - recordingstarttime < 2):
                        functions.MessageSender("Recording will start in: 2")
                        secondsbeforerecodingstarts -= 1
                    elif (secondsbeforerecodingstarts == 1 and 2 <= time.time() - recordingstarttime < 3):
                        functions.MessageSender("Recording will start in: 1")
                        secondsbeforerecodingstarts -= 1
                    elif (secondsbeforerecodingstarts == 0 and 3 <= time.time() - recordingstarttime < 4):
                        functions.MessageSender("Action!")
                        recordingstarttime = 0
                        startrecording = True

                if starttracking == True:
                    rawstringpositiondata = str(space_location.pose).split()

                    xcoord = functions.DataExtractor(rawstringpositiondata[len(rawstringpositiondata) - 3])
                    ycoord = functions.DataExtractor(rawstringpositiondata[len(rawstringpositiondata) - 2])
                    zcoord = functions.DataExtractor(rawstringpositiondata[len(rawstringpositiondata) - 1])

                    qw = float(functions.DataExtractor(rawstringpositiondata[3]))
                    qx = float(functions.DataExtractor(rawstringpositiondata[0]))
                    qy = float(functions.DataExtractor(rawstringpositiondata[1]))
                    qz = float(functions.DataExtractor(rawstringpositiondata[2]))

                    pitch = 0 - math.atan2(2*qy*qw - 2*qx*qz, 1 - 2*qy*qy - 2*qz*qz) * 180 / math.pi + 90
                    yaw = math.asin(2*qx*qy + 2*qz*qw) * 180 / math.pi

                    arrlocx.append(float(xcoord))
                    arrlocy.append(float(ycoord))
                    arrlocz.append(float(zcoord))

                    arrpitch.append(pitch)
                    arryaw.append(yaw)

                    if (firstxcoord == -90.0): 
                        firstxcoord = float(xcoord) * dimensionsscale
                        firstycoord = float(ycoord) * heightscale
                        firstzcoord = float(zcoord) * dimensionsscale

                    if (len(arrlocx) == 3):

                        locx = sum(arrlocx) / 3
                        locy = sum(arrlocy) / 3
                        locz = sum(arrlocz) / 3

                        functions.RotationValueTranslate(arrpitch)

                        pitch = sum(arrpitch) / 3
                        yaw = sum(arryaw) / 3

                        if (lockedpitch == -1000): lockedpitch = pitch

                        (
                            scenecenterxcoord, 
                            scenecenterycoord, 
                            scenecenterzcoord
                        ) = functions.CenterOfSceneModifier(
                            scenecenterxcoord, 
                            scenecenterycoord, 
                            scenecenterzcoord, 
                            left_controller_thumbstick_x_coord.current_state, 
                            left_controller_thumbstick_y_coord.current_state, 
                            thumbstickmode, 
                            pitch, 
                            lockedpitch, 
                            thumbstickscale
                        )

                        functions.CommandPrinter("tp @a " + 
                        str(scenecenterxcoord + locx * dimensionsscale - firstxcoord) + " " + 
                        str(scenecenterycoord + locy * heightscale - firstycoord) + " " + 
                        str(scenecenterzcoord + locz * dimensionsscale - firstzcoord) + " " + 
                        str(pitch) + " " + 
                        str(yaw))

                        if startrecording == True:
                            file.write("execute if score @p animtick matches " + 
                            str(currenttick) + " run tp @p " + 
                            str(scenecenterxcoord + locx * dimensionsscale - firstxcoord) + " " + 
                            str(scenecenterycoord + locy * heightscale - firstycoord) + " " + 
                            str(scenecenterzcoord + locz * dimensionsscale - firstzcoord) + " " + 
                            str(pitch) + " " + str(yaw) + "\n")
                            currenttick += 1

                        del arrlocx[0]
                        del arrlocy[0]
                        del arrlocz[0]
                        del arrpitch[0]
                        del arryaw[0]

                found_count += 1
            if found_count == 0:
                print("No controllers active")
        while True:
            if (time.time() - ingameticktime >= 0.05): break
