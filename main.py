from direct.showbase.ShowBase import ShowBase  # noqa
from direct.showbase.InputStateGlobal import inputState as InputState  # noqa
from direct.task import Task  # noqa
from panda3d.core import KeyboardButton, AmbientLight, InputDevice
from panda3d.core import DirectionalLight, WindowProperties
from components.ninja import Ninja
from components.collisions import Collisions


class Panda3dRoom(ShowBase, Ninja, Collisions):

    # noinspection PyArgumentList
    def __init__(self):
        ShowBase.__init__(self)
        Ninja.__init__(self)
        Collisions.__init__(self)
        props = WindowProperties()
        props.setTitle('panda3d room')
        self.win.requestProperties(props)

        self.scene = self.loader.load_model('assets/Home2_Night.bam')
        self.scene.reparent_to(self.render)
        self.set_background_color(0, 0, 0, 1.0)

        amb_light = AmbientLight('ambient')
        amb_light.set_color((0.5, 0.4, 0.4, 1.0))  # noqa
        ambient_light_node = self.render.attach_new_node(amb_light)
        self.render.set_light(ambient_light_node)

        dir_light = DirectionalLight('directional')
        dir_light.set_color_temperature(4500)  # noqa
        dir_light_node = self.render.attach_new_node(dir_light)
        dir_light_node.set_hpr(60, 0, 90)
        self.render.set_light(dir_light_node)

        self.disable_mouse()

        self.scene.set_scale(4, 4, 4)
        self.scene.set_pos(0, 0, 0)

        self.ninja.reparent_to(self.render)
        new_ninja_pos = self.scene.find('CoffeeTable').get_pos()
        new_ninja_pos[0] += 5.0
        new_ninja_pos[2] -= 0.4
        self.ninja.set_pos(new_ninja_pos)

        self.tmp_node = self.render.attach_new_node('ThirdPersonCam')  # noqa

        self.set_scene_collision_nodes(self.scene)

        self.cam_x, self.cam_y, self.cam_z = 0, -20, 9.7
        self.camera.set_pos(self.cam_x, self.cam_y, self.cam_z)
        self.camera.set_p(-15)
        self.camLens.set_near(12)

        self.task_mgr.add(self.update, 'Update')
        self.is_down = self.mouseWatcherNode.is_button_down

        self.up = KeyboardButton.up()
        self.down = KeyboardButton.down()
        self.left = KeyboardButton.left()
        self.right = KeyboardButton.right()
        self.a = KeyboardButton.ascii_key('a')
        self.s = KeyboardButton.ascii_key('s')
        self.d = KeyboardButton.ascii_key('d')
        self.w = KeyboardButton.ascii_key('w')

        self.gamepad = None
        for device in self.devices.get_devices(InputDevice.DeviceClass.gamepad):
            if 'xbox' in device.name.lower():
                self.connect_input_device(device)

        InputState.watch_with_modifiers('dpad_down', 'gamepad-dpad_down')
        InputState.watch_with_modifiers('dpad_left', 'gamepad-dpad_left')
        InputState.watch_with_modifiers('dpad_right', 'gamepad-dpad_right')
        InputState.watch_with_modifiers('dpad_up', 'gamepad-dpad_up')
        InputState.watch_with_modifiers('lshoulder', 'gamepad-lshoulder')
        InputState.watch_with_modifiers('rshoulder', 'gamepad-rshoulder')
        InputState.watch_with_modifiers('face_a', 'gamepad-face_a')
        InputState.watch_with_modifiers('face_x', 'gamepad-face_x')

        self.accept('connect-device', self.connect_input_device)
        self.accept('disconnect-device', self.disconnect_input_device)
        # self.accept('gamepad-start', self.pause)  # TODO

        self.zoom_in, self.zoom_out = False, False
        self.zoom_start, self.zoom_initial_cam_y = 0, 0
        self.focused_direction = None
        self.task_mgr.add(self.camera_collide, 'CameraCollider')

    def connect_input_device(self, device):
        if not self.gamepad and device.device_class == InputDevice.DeviceClass.gamepad:
            print(f'connecting {device.name}')
            self.gamepad = device
            self.attach_input_device(device, prefix='gamepad')

    def disconnect_input_device(self, device):
        if self.gamepad == device:
            print(f'disconnecting {device.name}')
            self.detach_input_device(device)
            self.gamepad = None

    def camera_collide(self, task):
        _ = task
        # if self.camera_handler.entries:
        #     for entry in self.camera_handler.entries:
        #         print(entry)
        # return Task.cont

        if self.camera_handler.entries:
            from_node = str(self.camera_handler.entries[0].get_from_node_path())
            into_node = str(self.camera_handler.entries[0].get_into_node_path())
            self.camera.set_pos(self.cam_x, self.cam_y, self.cam_z)
            if 'CameraCnode' in from_node and 'Walls' in into_node:
                if not self.zoom_in and not self.focused_direction:
                    self.zoom_initial_cam_y = self.camera.get_y()
                    self.zoom_in = True
                    self.focused_direction = into_node.split('/')[-1][:4]
                    print(self.camera_handler.entries[0].get_from_node_path())
                    print(self.camera_handler.entries[0].get_into_node_path())
                    print(self.ninja.get_pos())

        return Task.cont

    def check_keys(self):
        if self.is_down(self.left) or InputState.is_set('dpad_left'):
            self.turn_left()
        if self.is_down(self.right) or InputState.is_set('dpad_right'):
            self.turn_right()

        if self.is_down(self.up) or InputState.is_set('dpad_up'):
            if self.is_down(self.w) or InputState.is_set('face_a'):
                self.run_forward()
            else:
                self.walk_forward()
        elif self.is_down(self.down) or InputState.is_set('dpad_down'):
            self.walk_backward()
        elif self.is_down(self.s) or InputState.is_set('face_x'):
            self.punch()
        elif self.is_down(self.a) or InputState.is_set('lshoulder'):
            self.strafe_left()
        elif self.is_down(self.d) or InputState.is_set('rshoulder'):
            self.strafe_right()
        else:
            self.stop()

    def move_ninja(self):
        _, action = self.current_action.split('_')
        if action == 'Walk':
            self.ninja.set_y(self.ninja, 0.1)
        elif action == 'WalkBack':
            self.ninja.set_y(self.ninja, -0.05)
        elif action == 'Run':
            self.ninja.set_y(self.ninja, 0.3)
        elif action == 'StrafeLeft':
            self.ninja.set_x(self.ninja, -0.1)
        elif action == 'StrafeRight':
            self.ninja.set_x(self.ninja, 0.1)

        self.ninja.set_h(self.ninja_heading)  # noqa
        self.tmp_node.set_pos(self.ninja.get_pos())  # noqa
        heading = self.tmp_node.get_h()
        turn_diff = self.ninja.get_h() - heading  # noqa
        self.tmp_node.set_h(heading + turn_diff * self.turn_rate)
        self.camera.reparent_to(self.tmp_node)

    def update(self, task):
        _ = task
        self.check_keys()
        self.move_ninja()
        # self.camera_zoom()
        return Task.cont


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
