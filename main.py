from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import KeyboardButton, AmbientLight, PointLight
from panda3d.core import DirectionalLight  # , Spotlight, PerspectiveLens
from panda3d.core import CollisionNode, CollisionBox, CollisionCapsule
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.interval.IntervalGlobal import LerpAnimInterval
from direct.task import Task
# Convert glb/gltf to .bam:
# source venv/bin/activate
# gltf2bam assets/soldierx.glb assets/soldierx.bam


class Panda3dWalking(ShowBase):

    # noinspection PyArgumentList
    def __init__(self):
        ShowBase.__init__(self)

        self.scene = self.loader.load_model('assets/Home2_Night.bam')
        self.scene.reparent_to(self.render)

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        amb_light = AmbientLight('ambient')
        amb_light.set_color((0.5, 0.4, 0.4, 1.0))  # noqa
        ambient_light_node = self.render.attach_new_node(amb_light)
        self.render.set_light(ambient_light_node)

        dir_light = DirectionalLight('directional')
        dir_light.set_color_temperature(5000)  # noqa
        dir_light_node = self.render.attachNewNode(dir_light)
        dir_light_node.set_hpr(60, 0, 90)
        self.render.set_light(dir_light_node)

        # remove this to use mouse left, middle, and right btns to position
        self.disable_mouse()

        # Apply scale and position transforms on the model.
        self.scene.set_scale(4, 4, 4)
        self.scene.set_pos(0, 0, 0)

        self.soldier = Actor('assets/soldierx.bam')
        self.soldier.reparent_to(self.render)

        new_soldier_pos = self.scene.find('CoffeeTable').get_pos()
        new_soldier_pos[0] += 5
        self.soldier.set_pos(new_soldier_pos)

        self.soldier.set_scale(4, 4, 4)

        self.soldier.loop('Idle')

        self.set_scene_collision_nodes()

        point_light = PointLight('point')
        point_light.set_color_temperature(6500)
        point_light_node = self.render.attach_new_node(point_light)
        point_light_node.set_pos(0, 0, 15)
        self.soldier.set_light(point_light_node)

        # spot_light = PointLight('spot')
        # spot_lens = PerspectiveLens()
        # spot_light.set_lens(spot_lens)  # noqa
        # spot_light.set_color((0.0, 0.9, 0.0, 0.1))  # noqa
        # spot_light.set_color_temperature(6000)  # noqa
        # spot_light.set_shadow_caster(True)  # noqa
        # spot_light_node = self.render.attach_new_node(spot_light)
        # spot_light_node.set_pos(-10, -10, 20)
        # spot_light_node.look_at(self.soldier)
        # self.render.set_light(spot_light_node)  # noqa
        # self.render.set_shader_auto()

        self.soldier_heading = 0
        self.soldier.enable_blend()

        self.camera.set_pos(0, -20, 9.7)
        self.camera.set_p(-15)

        self.task_mgr.add(self.update, 'Update')
        self.is_down = self.mouseWatcherNode.is_button_down

        self.current_action = 'Walk_Idle'
        self.animations = {
            'Idle_Walk': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Walk')
            },
            'Walk_Idle': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Idle')
            },
            'Idle_WalkBack': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Idle', 'WalkBack')
            },
            'WalkBack_Idle': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Idle')
            },
            'Idle_Run': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Run')
            },
            'Run_Idle': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Run', 'Idle')
            },
            'Run_Walk': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Run', 'Walk')
            },
            'Walk_Run': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Run')
            },
            'Idle_Punch': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Punch')
            },
            'Punch_Idle': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Idle')
            },
            'Run_Punch': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Run', 'Punch')
            },
            'Punch_Run': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Run')
            },
            'Walk_Punch': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Punch')
            },
            'Punch_Walk': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Walk')
            },
            'WalkBack_Punch': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Punch')
            },
            'Punch_WalkBack': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Punch', 'WalkBack')
            },
            'WalkBack_Run': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Run')
            },
            'Run_WalkBack': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Run', 'WalkBack')
            },
            'WalkBack_Walk': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Walk')
            },
            'Walk_WalkBack': {
                'lerp': LerpAnimInterval(self.soldier, 0.25, 'Walk', 'WalkBack')
            }
        }

        self.up = KeyboardButton.up()
        self.down = KeyboardButton.down()
        self.left = KeyboardButton.left()
        self.right = KeyboardButton.right()
        self.p = KeyboardButton.ascii_key('p')
        self.shift = KeyboardButton.shift()

        self.tmp_node = self.render.attach_new_node('cam-%s' % self.soldier.get_name())  # noqa
        self.turn_rate = 1.5

    def finish_running_lerps(self):
        _ = [lerp['lerp'].finish() for _, lerp in self.animations.items()  # noqa
             if lerp['lerp'].is_playing()]  # noqa

    def animate_soldier(self, new_action):
        _, old_action = self.current_action.split('_')
        if old_action != new_action:
            self.finish_running_lerps()
            self.current_action = f'{old_action}_{new_action}'
            self.animations[self.current_action]['lerp'].start()  # noqa

            if new_action != 'Punch':
                self.soldier.loop(new_action)
            else:
                self.soldier.play(new_action)

    def walk_forward(self):
        self.animate_soldier('Walk')

    def run_forward(self):
        self.animate_soldier('Run')

    def walk_backward(self):
        self.animate_soldier('WalkBack')

    def stop(self):
        self.animate_soldier('Idle')

    def punch(self):
        self.animate_soldier('Punch')

    def turn_left(self):
        self.soldier_heading += 3
        self.soldier.set_h(self.soldier_heading)  # noqa

    def turn_right(self):
        self.soldier_heading -= 3
        self.soldier.set_h(self.soldier_heading)  # noqa

    def check_keys(self):
        if self.is_down(self.left):
            self.turn_left()
        if self.is_down(self.right):
            self.turn_right()

        if self.is_down(self.up):
            if self.is_down(self.shift):
                self.run_forward()
            else:
                self.walk_forward()
        elif self.is_down(self.down):
            self.walk_backward()
        elif self.is_down(self.p):
            self.punch()
        else:
            self.stop()

    def move_soldier(self):
        _, action = self.current_action.split('_')
        if action == 'Walk':
            self.soldier.set_y(self.soldier, 0.05)
        elif action == 'WalkBack':
            self.soldier.set_y(self.soldier, -0.01)
        elif action == 'Run':
            self.soldier.set_y(self.soldier, 0.2)

        self.soldier.set_h(self.soldier_heading)  # noqa
        self.tmp_node.set_pos(self.soldier.get_pos())  # noqa
        heading = self.tmp_node.get_h()
        turn_diff = self.soldier.get_h() - heading  # noqa
        self.tmp_node.set_h(heading + turn_diff * self.turn_rate)
        self.camera.reparent_to(self.tmp_node)

    def update(self, task):
        _ = task
        self.check_keys()
        self.move_soldier()
        return Task.cont

    def set_scene_collision_nodes(self):
        # self.scene.ls()
        capsule = CollisionCapsule(0, 0, 0.4, 0, 0, 1.3, 0.45)
        soldier_cnode = self.soldier.attach_new_node(CollisionNode('soldier_cnode'))  # noqa
        soldier_cnode.node().add_solid(capsule)
        soldier_cnode.show()
        self.pusher.add_collider(soldier_cnode, self.soldier)  # noqa
        self.cTrav.add_collider(soldier_cnode, self.pusher)  # noqa

        coffee_table = self.scene.find('CoffeeTable')
        box = CollisionBox(coffee_table.get_pos()[0], 0.6, 1.4, 0.6)
        coffee_table_node = coffee_table.attach_new_node(CollisionNode('coffee_table_cnode'))
        coffee_table_node.node().add_solid(box)
        coffee_table_node.show()
        self.pusher.add_collider(coffee_table_node, coffee_table)  # noqa
        self.cTrav.add_collider(coffee_table_node, self.pusher)  # noqa


if __name__ == '__main__':
    app = Panda3dWalking()
    app.run()
