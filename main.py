from direct.showbase.ShowBase import ShowBase  # noqa
from direct.task import Task  # noqa
from panda3d.core import KeyboardButton, AmbientLight
from panda3d.core import DirectionalLight, WindowProperties
from panda3d.core import CollisionNode, CollisionBox, CollisionCapsule
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from components.ninja import Ninja


class Panda3dRoom(ShowBase, Ninja):

    # noinspection PyArgumentList
    def __init__(self):
        ShowBase.__init__(self)
        Ninja.__init__(self)
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
        dir_light_node = self.render.attach_new_node(dir_light)
        dir_light_node.set_hpr(60, 0, 90)
        self.render.set_light(dir_light_node)

        # remove this to use mouse left, middle, and right btns to position
        self.disable_mouse()

        self.scene.set_scale(4, 4, 4)
        self.scene.set_pos(0, 0, 0)

        self.ninja.reparent_to(self.render)
        new_ninja_pos = self.scene.find('CoffeeTable').get_pos()
        new_ninja_pos[0] += 5.0
        new_ninja_pos[2] -= 0.4
        self.ninja.set_pos(new_ninja_pos)

        self.tmp_node = self.render.attach_new_node('cam-%s' % self.ninja.get_name())  # noqa

        self.set_scene_collision_nodes()

        self.camera.set_pos(0, -20, 9.7)
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

    def check_keys(self):
        if self.is_down(self.left):
            self.turn_left()
        if self.is_down(self.right):
            self.turn_right()

        if self.is_down(self.up):
            if self.is_down(self.w):
                self.run_forward()
            else:
                self.walk_forward()
        elif self.is_down(self.down):
            self.walk_backward()
        elif self.is_down(self.s):
            self.punch()
        elif self.is_down(self.a):
            self.strafe_left()
        elif self.is_down(self.d):
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
        body_capsule = CollisionCapsule(0.0, 0.0, 1.2, 0.0, 0.0, 4.0, 1.5)
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

    def update(self, task):
        _ = task
        self.check_keys()
        self.move_ninja()
        return Task.cont


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
