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

        self.zoom_in, self.zoom_out, self.focused = False, False, False
        self.collision_wall, self.collision_pos = None, None
        self.zoom_start, self.zoom_initial_cam_y = 0.0, 0.0
        self.zoom_max = 7.0
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

    def at_zoom_max_x(self):
        return abs(self.collision_pos.x - self.ninja.get_x()) >= self.zoom_max

    def at_zoom_max_y(self):
        return abs(self.collision_pos.y - self.ninja.get_y()) >= self.zoom_max

    def camera_collide(self, task):
        _ = task

        if self.camera_handler.entries and not self.zoom_in and not self.focused:
            self.collision_wall = str(self.camera_handler.entries[0].get_into_node_path())
            self.zoom_initial_cam_y = self.camera.get_y()
            self.zoom_start = 0
            self.zoom_in = True
            self.collision_pos = self.ninja.get_pos()

        if self.focused and not self.zoom_out and not self.camera_handler.entries:
            heading = abs(self.ninja.get_h() % 360)
            if 'North' in self.collision_wall and ((heading < 90 or heading > 270) or self.at_zoom_max_y()):
                self.zoom_out = True
            elif 'South' in self.collision_wall and ((90 < heading < 270) or self.at_zoom_max_y()):
                self.zoom_out = True
            elif 'East' in self.collision_wall and ((360 > heading > 180) or self.at_zoom_max_x()):
                self.zoom_out = True
            elif 'West' in self.collision_wall and ((0 < heading < 180) or self.at_zoom_max_x()):
                self.zoom_out = True

            if self.zoom_out:
                self.zoom_start = 0
                self.zoom_initial_cam_y = self.camera.get_y()
        return Task.cont

    def camera_zoom(self):
        if self.zoom_in:
            if self.zoom_start < self.zoom_max:
                self.zoom_start += 0.2
            else:
                self.zoom_start = self.zoom_max
                self.zoom_in = False
                self.focused = True
            self.camera.set_pos(self.cam_x, self.zoom_initial_cam_y + self.zoom_start, self.cam_z)

        if self.zoom_out:
            if self.zoom_start < self.zoom_max:
                self.zoom_start += 0.2
            else:
                self.zoom_start = self.zoom_max
                self.zoom_out, self.focused = False, False
                self.collision_wall, self.collision_pos = None, None
            self.camera.set_pos(self.cam_x, self.zoom_initial_cam_y - self.zoom_start, self.cam_z)

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
        self.camera_zoom()
        return Task.cont


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
