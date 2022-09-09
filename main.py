from direct.actor.Actor import Actor  # noqa
from direct.showbase.ShowBase import ShowBase  # noqa
from panda3d.core import KeyboardButton, AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import CollisionNode, CollisionBox, CollisionSphere
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.interval.IntervalGlobal import LerpAnimInterval  # noqa
from direct.task import Task  # noqa
#
# Convert glb/gltf to bam by activating venv and running:
# gltf2bam assets/soldierx.glb assets/soldierx.bam
#
# Development:
# python main.py
#
# Build binaries for distribution:
# python setup.py build_apps


class Panda3dRoom(ShowBase):

    # noinspection PyArgumentList
    def __init__(self):
        ShowBase.__init__(self)

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
        dir_light.set_color_temperature(5000)  # noqa
        dir_light_node = self.render.attachNewNode(dir_light)
        dir_light_node.set_hpr(60, 0, 90)
        self.render.set_light(dir_light_node)

        # remove this to use mouse left, middle, and right btns to position
        self.disable_mouse()

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
            self.soldier.set_y(self.soldier, 0.1)

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
        head_sphere = CollisionSphere(0, 0, 1.5, 0.2)
        head_cnode = self.soldier.attach_new_node(CollisionNode('head_cnode'))  # noqa
        head_cnode.node().add_solid(head_sphere)
        # head_cnode.show()
        self.pusher.add_collider(head_cnode, self.soldier)  # noqa
        # Put FROM objects into traverser:
        self.cTrav.add_collider(head_cnode, self.pusher)  # noqa
        body_sphere = CollisionSphere(0.0, 0.0, 0.7, 0.3)
        body_cnode = self.soldier.attach_new_node(CollisionNode('body_cnode'))  # noqa
        body_cnode.node().add_solid(body_sphere)
        # body_cnode.show()
        self.pusher.add_collider(body_cnode, self.soldier)  # noqa
        # Put FROM objects into traverser:
        self.cTrav.add_collider(body_cnode, self.pusher)  # noqa

        # static TO objects don't need to be put in the Traverser:
        coffee_table = self.scene.find('CoffeeTable')
        coffee_tale_box = CollisionBox(0.0, 0.8, 1.6, 0.2)
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
        side_quest_wall_box = CollisionBox(0.0, 0.2, 4.0, 0.6)
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


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
