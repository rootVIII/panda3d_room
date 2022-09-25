from direct.actor.Actor import Actor  # noqa
from direct.showbase.ShowBase import ShowBase  # noqa
from direct.showbase.InputStateGlobal import inputState as InputState  # noqa
from direct.interval.IntervalGlobal import LerpAnimInterval  # noqa
from direct.task import Task  # noqa
from panda3d.core import InputDevice, KeyboardButton, AmbientLight
from panda3d.core import DirectionalLight, WindowProperties
from panda3d.core import CollisionNode, CollisionBox, CollisionCapsule
from panda3d.core import CollisionTraverser, CollisionHandlerPusher


class Panda3dRoom(ShowBase):

    # noinspection PyArgumentList
    def __init__(self):
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('panda3d room')
        self.win.requestProperties(props)

        self.scene = self.loader.load_model('assets/Home2_Night.bam')
        self.scene.reparent_to(self.render)
        self.set_background_color(0, 0, 0, 1.0)

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        amb_light = AmbientLight('ambient')
        amb_light.set_color((0.5, 0.4, 0.4, 1.0))  # noqa
        ambient_light_node = self.render.attach_new_node(amb_light)
        self.render.set_light(ambient_light_node)

        dir_light = DirectionalLight('directional')
        dir_light.set_color_temperature(4500)  # noqa
        dir_light_node = self.render.attachNewNode(dir_light)
        dir_light_node.set_hpr(60, 0, 90)
        self.render.set_light(dir_light_node)

        self.disable_mouse()

        self.scene.set_scale(4, 4, 4)
        self.scene.set_pos(0, 0, 0)

        self.ninja = Actor('assets/ninja.bam')
        self.ninja.reparent_to(self.render)

        new_ninja_pos = self.scene.find('CoffeeTable').get_pos()
        new_ninja_pos[0] += 5.0
        new_ninja_pos[2] -= 0.4
        self.ninja.set_pos(new_ninja_pos)

        self.ninja.loop('Idle')

        self.set_scene_collision_nodes()

        self.ninja_heading = 0
        self.ninja.enable_blend()

        self.camera.set_pos(0, -20, 9.7)
        self.camera.set_p(-15)
        self.camLens.set_near(12)

        self.task_mgr.add(self.update, 'Update')

        self.is_down = self.mouseWatcherNode.is_button_down

        InputState.watch_with_modifiers('dpad_down', 'gamepad-dpad_down')
        InputState.watch_with_modifiers('dpad_left', 'gamepad-dpad_left')
        InputState.watch_with_modifiers('dpad_right', 'gamepad-dpad_right')
        InputState.watch_with_modifiers('dpad_up', 'gamepad-dpad_up')
        InputState.watch_with_modifiers('lshoulder', 'gamepad-lshoulder')
        InputState.watch_with_modifiers('rshoulder', 'gamepad-rshoulder')
        InputState.watch_with_modifiers('face_a', 'gamepad-face_a')
        InputState.watch_with_modifiers('face_x', 'gamepad-face_x')

        # TODO: add kick or an extra punch:
        # inputState.watch_with_modifiers('face_b', 'gamepad-face_b')
        # inputState.watch_with_modifiers('face_y', 'gamepad-face_y')

        self.current_action = 'Walk_Idle'
        self.animations = {
            'Idle_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'Walk')
            },
            'Walk_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'Idle')
            },
            'Idle_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'WalkBack')
            },
            'WalkBack_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'Idle')
            },
            'Idle_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'Run')
            },
            'Run_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'Idle')
            },
            'Run_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'Walk')
            },
            'Walk_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'Run')
            },
            'Idle_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'Punch')
            },
            'Punch_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'Idle')
            },
            'Run_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'Punch')
            },
            'Punch_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'Run')
            },
            'Walk_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'Punch')
            },
            'Punch_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'Walk')
            },
            'WalkBack_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'Punch')
            },
            'Punch_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'WalkBack')
            },
            'WalkBack_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'Run')
            },
            'Run_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'WalkBack')
            },
            'WalkBack_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'Walk')
            },
            'Walk_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'WalkBack')
            },
            'Walk_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'StrafeRight')
            },
            'StrafeRight_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'Walk')
            },
            'StrafeRight_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'WalkBack')
            },
            'WalkBack_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'StrafeRight')
            },
            'StrafeRight_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'Run')
            },
            'Run_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'StrafeRight')
            },
            'StrafeRight_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'Punch')
            },
            'Punch_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'StrafeRight')
            },
            'StrafeRight_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'Idle')
            },
            'Idle_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'StrafeRight')
            },
            'StrafeRight_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeRight', 'StrafeLeft')
            },
            'StrafeLeft_StrafeRight': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'StrafeRight')
            },
            'Walk_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Walk', 'StrafeLeft')
            },
            'StrafeLeft_Walk': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'Walk')
            },
            'StrafeLeft_WalkBack': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'WalkBack')
            },
            'WalkBack_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'WalkBack', 'StrafeLeft')
            },
            'StrafeLeft_Run': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'Run')
            },
            'Run_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Run', 'StrafeLeft')
            },
            'StrafeLeft_Punch': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'Punch')
            },
            'Punch_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Punch', 'StrafeLeft')
            },
            'StrafeLeft_Idle': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'StrafeLeft', 'Idle')
            },
            'Idle_StrafeLeft': {
                'lerp': LerpAnimInterval(self.ninja, 0.25, 'Idle', 'StrafeLeft')
            }
        }

        self.up = KeyboardButton.up()
        self.down = KeyboardButton.down()
        self.left = KeyboardButton.left()
        self.right = KeyboardButton.right()
        self.a = KeyboardButton.ascii_key('a')
        self.s = KeyboardButton.ascii_key('s')
        self.d = KeyboardButton.ascii_key('d')
        self.w = KeyboardButton.ascii_key('w')

        self.tmp_node = self.render.attach_new_node('cam-%s' % self.ninja.get_name())  # noqa
        self.turn_rate = 1.5

        self.gamepad = None
        for device in self.devices.get_devices(InputDevice.DeviceClass.gamepad):
            if 'xbox' in device.name.lower():
                self.connect_input_device(device)

        self.accept('connect-device', self.connect_input_device)
        self.accept('disconnect-device', self.disconnect_input_device)
        # self.accept('gamepad-start', self.pause)

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

    def finish_running_lerps(self):
        _ = [lerp['lerp'].finish() for _, lerp in self.animations.items()  # noqa
             if lerp['lerp'].is_playing()]  # noqa

    def animate_model(self, new_action):
        _, old_action = self.current_action.split('_')
        if old_action != new_action:
            self.finish_running_lerps()
            self.current_action = f'{old_action}_{new_action}'
            self.animations[self.current_action]['lerp'].start()  # noqa

            if new_action != 'Punch':
                self.ninja.loop(new_action)
            else:
                self.ninja.play(new_action)

    def walk_forward(self):
        self.animate_model('Walk')

    def run_forward(self):
        self.animate_model('Run')

    def walk_backward(self):
        self.animate_model('WalkBack')

    def stop(self):
        self.animate_model('Idle')

    def punch(self):
        self.animate_model('Punch')

    def strafe_left(self):
        self.animate_model('StrafeLeft')

    def strafe_right(self):
        self.animate_model('StrafeRight')

    def turn_left(self):
        self.ninja_heading += 3
        self.ninja.set_h(self.ninja_heading)  # noqa

    def turn_right(self):
        self.ninja_heading -= 3
        self.ninja.set_h(self.ninja_heading)  # noqa

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

    def set_scene_collision_nodes(self):
        # self.scene.ls()
        body_capsule = CollisionCapsule(0, 0, 1.2, 0, 0, 4.0, 1.5)
        body_cnode = self.ninja.attach_new_node(CollisionNode('body_cnode'))  # noqa
        body_cnode.node().add_solid(body_capsule)
        # body_cnode.show()
        self.pusher.add_collider(body_cnode, self.ninja)  # noqa
        # Put FROM objects into traverser:
        self.cTrav.add_collider(body_cnode, self.pusher)  # noqa

        # static TO objects don't need to be put in the Traverser:
        coffee_table = self.scene.find('CoffeeTable')
        coffee_tale_box = CollisionBox(0.0, 0.9, 1.6, 0.2)
        coffee_table_node = coffee_table.attach_new_node(CollisionNode('coffee_table_cnode'))
        coffee_table_node.set_pos(0.0, 0.1, 0.4)
        coffee_table_node.node().add_solid(coffee_tale_box)
        # coffee_table_node.show()
        self.pusher.add_collider(coffee_table_node, coffee_table)  # noqa

        seat = self.scene.find('Seat')
        seat_box = CollisionBox(0.0, 0.7, 0.6, 0.3)
        seat_node = seat.attach_new_node(CollisionNode('seat_cnode'))
        seat_node.set_pos(-1.8, -8.0, 0.0)
        seat_node.set_h(40)
        seat_node.node().add_solid(seat_box)
        # seat_node.show()
        self.pusher.add_collider(seat_node, seat)  # noqa

        curtain_wall = self.scene.find('Curtain001')
        curtain_wall_box = CollisionBox(0.0, 2.2, 0.2, 0.6)
        curtain_wall_box_node = curtain_wall.attach_new_node(CollisionNode('curtain_wall_cnode'))
        curtain_wall_box_node.set_pos(0.7, -2.2, 0.0)
        curtain_wall_box_node.node().add_solid(curtain_wall_box)
        # curtain_wall_box_node.show()
        self.pusher.add_collider(curtain_wall_box_node, curtain_wall)  # noqa

        side_quest_wall = self.scene.find('fwaf')
        side_quest_wall_box = CollisionBox(0.0, 0.4, 4.0, 0.6)
        side_quest_wall_box_node = side_quest_wall.attach_new_node(CollisionNode('side_quest_wall_cnode'))
        side_quest_wall_box_node.set_pos(-2.2, 1.3, 0.0)
        side_quest_wall_box_node.node().add_solid(side_quest_wall_box)
        # side_quest_wall_box_node.show()
        self.pusher.add_collider(side_quest_wall_box_node, side_quest_wall)  # noqa

        door_wall = self.scene.find('Door')
        door_wall_box = CollisionBox(0.0, 3.8, 0.2, 0.6)
        door_wall_box_node = door_wall.attach_new_node(CollisionNode('door_wall_cnode'))
        door_wall_box_node.set_pos(1.8, -0.4, 0.0)
        door_wall_box_node.node().add_solid(door_wall_box)
        # door_wall_box_node.show()
        self.pusher.add_collider(door_wall_box_node, door_wall)  # noqa

        plant_wall = self.scene.find('Sphere002')
        plant_wall_box = CollisionBox(0.0, 0.2, 2.7, 0.6)
        plant_wall_box_node = plant_wall.attach_new_node(CollisionNode('plant_wall_cnode'))
        plant_wall_box_node.set_pos(-4.5, -1.6, 0.0)
        plant_wall_box_node.set_h(10)
        plant_wall_box_node.node().add_solid(plant_wall_box)
        # plant_wall_box_node.show()
        self.pusher.add_collider(plant_wall_box_node, plant_wall)  # noqa

        sofas = self.scene.find('SofaFinal')
        sofa1_box = CollisionBox(0.0, 1.0, 0.8, 0.6)
        sofa1_box_node = sofas.attach_new_node(CollisionNode('sofa1_cnode'))
        sofa1_box_node.set_pos(0.0, 2.5, 0.0)
        sofa1_box_node.node().add_solid(sofa1_box)
        # sofa1_box_node.show()
        self.pusher.add_collider(sofa1_box_node, sofas)  # noqa
        sofa2_box = CollisionBox(0.0, 0.3, 1.3, 0.6)
        sofa2_box_node = sofas.attach_new_node(CollisionNode('sofa2_cnode'))
        sofa2_box_node.set_pos(1.8, 0.1, 0.0)
        sofa2_box_node.node().add_solid(sofa2_box)
        # sofa2_box_node.show()
        self.pusher.add_collider(sofa2_box_node, sofas)  # noqa

    @staticmethod
    def test(button):
        print(f'button: {button}')

    def update(self, task):
        _ = task
        self.check_keys()
        self.move_ninja()
        return Task.cont


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
