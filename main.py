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
        self.scene.ls()
        capsule = CollisionCapsule(0, 0, 0.4, 0, 0, 1.3, 0.45)
        soldier_cnode = self.soldier.attach_new_node(CollisionNode('soldier_cnode'))  # noqa
        soldier_cnode.node().add_solid(capsule)
        soldier_cnode.show()
        self.pusher.add_collider(soldier_cnode, self.soldier)  # noqa
        self.cTrav.add_collider(soldier_cnode, self.pusher)  # noqa

        coffee_table = self.scene.find('CoffeeTable')
        coffee_table_x, coffee_table_y, coffee_table_z = coffee_table.get_pos()
        coffee_tale_box = CollisionBox(coffee_table_x, 0.6, 1.4, 0.2)
        coffee_table_node = coffee_table.attach_new_node(CollisionNode('coffee_table_cnode'))
        coffee_table_node.set_pos(0, 0, 0.4)
        coffee_table_node.node().add_solid(coffee_tale_box)
        coffee_table_node.show()
        self.pusher.add_collider(coffee_table_node, coffee_table)  # noqa
        self.cTrav.add_collider(coffee_table_node, self.pusher)  # noqa

        seat = self.scene.find('Seat')
        seat_x, _, _, = seat.get_pos()
        seat_box = CollisionBox(0.0, 0.6, 0.6, 0.3)
        seat_node = seat.attach_new_node(CollisionNode('seat_cnode'))
        seat_node.set_pos(-1.8, -8.0, 0.0)
        seat_node.set_h(40)
        seat_node.node().add_solid(seat_box)
        seat_node.show()
        self.pusher.add_collider(seat_node, seat)  # noqa
        self.cTrav.add_collider(seat_node, self.pusher)  # noqa

        """
        PandaNode Sphere002 T:m(pos -0.694494 0.465446 0.298059 hpr 79.7098 0 0 scale 0.898964)
        PandaNode CoffeeTable T:m(pos -0.0541124 2.10138 -0.102804 hpr 180 0 0 scale 0.766159 0.672106 1)
        PandaNode Plane001 T:m(pos 0.232862 0.661916 -0.120272 hpr 180 0 0)
        PandaNode Door T:m(pos -2.72154 -2.15377 -0.120272 hpr 90 0 0 scale 1.18064 1 1)
        PandaNode RecordPlayer T:m(pos 2.19253 2.09771 0.598156 hpr 180 0 0 scale 0.513492 0.696524 1.42864)
        PandaNode Box043 T:m(pos 2.53411 1.31676 0.842399 hpr 180 0 50.6667 scale 1.74696)
        PandaNode Seat T:m(pos 0.396586 -4.00901 0.326915 hpr 180 0 0)
        PandaNode Roof T:m(pos 0.232862 0.661916 3.32537 hpr 180 0 180)
        PandaNode Box077 T:m(pos -2.6911 1.02895 1.8482 hpr 180 0 0 scale 0.770214 0.770214 0.829118)
        PandaNode Lights T:m(pos -1.33388 2.7471 3.32118 hpr 180 0 0)
        PandaNode Box094 T:m(pos -0.0970315 1.99833 -0.1306 hpr 180 0 0 scale 0.932252 1 1)
        PandaNode Storage T:m(pos -2.35017 -0.387263 0.231372 hpr 180 0 0 scale 0.839194 1.12143 0.474423)
        PandaNode Books T:m(pos 2.61092 -1.1386 0.461835 hpr -175 0 0 scale 0.911785)
        PandaNode Box091 T:m(pos 0.116134 4.92379 2.69559 hpr -6.83019e-06 90 -1.82123e-06 scale 0.936823 1 -0.732712)
          PandaNode ReverseCulling S:(CullFaceAttrib)
        PandaNode Box121 T:m(pos -1.00511 -4.34932 1.79195 hpr 180 0 0 scale 1.12577 0.940561 1.12577)
        PandaNode Plane003 T:m(pos 2.90311 2.49744 1.64551 hpr 0 90 -90 scale 4.33458)
        PandaNode Walls T:m(pos 0.232861 0.661916 -0.120272 hpr 180 0 0)
        PandaNode Curtain001 T:m(pos -0.0454077 2.12796 -0.064358 hpr 180 0 2.34103e-06 scale 1.00062 1.00141 0.991328)
        PandaNode SofaFinal T:m(pos -0.0470138 2.09851 -0.0630138 hpr 180 0 0 scale 1.02902 1.05268 1.20711)
        PandaNode Rail T:m(pos -0.0541124 2.00523 -0.21298 hpr 180 0 0 scale 0.75 0.77715 0.77715)
        PandaNode fwaf T:m(pos 0.232862 0.661916 -0.120272 hpr 180 0 0)
          PandaNode FinalShelvesef T:m(scale 1 1 1.61898)
        PandaNode Group002 T:m(pos 0.232862 0.661916 -0.120272 hpr 180 0 0)
          PandaNode fireGlas T:m(scale 0.961389 1.00968 1.00968)
          PandaNode Chimney T:m(hpr 90 0 0 scale 0.761784)
          PandaNode Fireplace T:m(scale 0.952176 1 1)
        PandaNode Decorations T:m(pos -0.0541126 2.10138 -0.102804 hpr 180 5.21849e-06 0 scale 0.683426 0.684426 0.684426)
        PandaNode GLOBEY T:m(pos 0.396587 -4.00901 0.326915 hpr 180 0 0)
          PandaNode GlobeSphere T:m(hpr -162.943 89.9999 -177.057 scale 0.944469)
          PandaNode GlobeBase T:m(pos -2.14441 0.0635236 0.407292 hpr 20 0 0 scale 1.52784)
          PandaNode plantz T:m(hpr -164.703 -8.1029 -17.471 scale 0.493729)
        PandaNode Group001 T:m(pos 0.232862 0.661916 -0.120272 hpr 180 0 0 scale 1 1 1.61898)
          PandaNode Box124 T:m(scale 1.04556 1.04556 0.645816)
        PandaNode Particle View 001 T:m(pos 0.116133 0.408226 -0.120272 hpr 180 0 0)
        """


if __name__ == '__main__':
    app = Panda3dWalking()
    app.run()
