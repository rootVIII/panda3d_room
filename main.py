from direct.actor.Actor import Actor, DirectionalLight, Spotlight # noqa
from direct.actor.Actor import AmbientLight, PointLight, PerspectiveLens # noqa
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpAnimInterval
from direct.task import Task
# Convert glb/gltf to .bam:
# source venv/bin/activate
# gltf2bam assets/soldierx.glb assets/soldierx.bam


class Panda3dWalking(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.scene = self.loader.load_model('assets/Home2_Night.bam')
        self.scene.reparent_to(self.render)

        # https://docs.panda3d.org/1.10/python/programming/scene-graph/searching-scene-graph
        # self.scene.ls()
        print(self.scene.find('CoffeeTable'))
        coffee_table_pos = self.scene.find('CoffeeTable').get_pos()
        print(coffee_table_pos[0])

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
        self.soldier.reparent_to(self.render)  # noqa

        self.soldier.set_pos(3.0, 4.0, -0.5)  # noqa
        # self.soldier.set_pos(coffee_table_pos)  # noqa

        self.soldier.set_scale(4, 4, 4)  # noqa

        self.soldier.loop('Idle')

        point_light = PointLight('point')
        point_light.set_color_temperature(6500)  # noqa
        point_light_node = self.render.attach_new_node(point_light)
        point_light_node.set_pos(0, 0, 15)
        self.soldier.set_light(point_light_node)  # noqa

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

        self.camera.set_pos(0, -24, 5.7)

        self.accept('arrow_up', self.walk_forward)
        self.accept('arrow_down', self.walk_backward)

        self.accept('arrow_up-up', self.stop)
        self.accept('arrow_down-up', self.stop)
        self.accept('control-arrow_up', self.run_forward)

        self.accept('arrow_left-repeat', self.turn_left)
        self.accept('arrow_right-repeat', self.turn_right)

        self.accept('p', self.punch)

        self.soldier_heading = 0

        self.soldier.enable_blend()

        self.idle_walk = LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Walk')
        self.walk_idle = LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Idle')

        self.idle_walkback = LerpAnimInterval(self.soldier, 0.25, 'Idle', 'WalkBack')
        self.walkback_idle = LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Idle')

        self.idle_run = LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Run')
        self.run_idle = LerpAnimInterval(self.soldier, 0.25, 'Run', 'Idle')

        self.run_walk = LerpAnimInterval(self.soldier, 0.25, 'Run', 'Walk')
        self.walk_run = LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Run')

        self.idle_punch = LerpAnimInterval(self.soldier, 0.25, 'Idle', 'Punch')
        self.punch_idle = LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Idle')

        self.run_punch = LerpAnimInterval(self.soldier, 0.25, 'Run', 'Punch')
        self.punch_run = LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Run')

        self.walk_punch = LerpAnimInterval(self.soldier, 0.25, 'Walk', 'Punch')
        self.punch_walk = LerpAnimInterval(self.soldier, 0.25, 'Punch', 'Walk')

        self.walkback_punch = LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Punch')
        self.punch_walkback = LerpAnimInterval(self.soldier, 0.25, 'Punch', 'WalkBack')

        self.walkback_run = LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Run')
        self.run_walkback = LerpAnimInterval(self.soldier, 0.25, 'Run', 'WalkBack')

        self.walkback_walk = LerpAnimInterval(self.soldier, 0.25, 'WalkBack', 'Walk')
        self.walk_walkback = LerpAnimInterval(self.soldier, 0.25, 'Walk', 'WalkBack')

        # self.task_mgr.add(self.get_mouse_coords_task, 'GetMouseCoordsTask')
        self.printing_coords = False

        self.animations = {
            'idle_walk': {'is_current': False, 'lerp': self.idle_walk},
            'walk_idle': {'is_current': True, 'lerp': self.walk_idle},
            'idle_walkback': {'is_current': False, 'lerp': self.idle_walkback},
            'walkback_idle': {'is_current': False, 'lerp': self.walkback_idle},
            'idle_run': {'is_current': False, 'lerp': self.idle_run},
            'run_idle': {'is_current': False, 'lerp': self.run_idle},
            'run_walk': {'is_current': False, 'lerp': self.run_walk},
            'walk_run': {'is_current': False, 'lerp': self.walk_run},
            'idle_punch': {'is_current': False, 'lerp': self.idle_punch},
            'punch_idle': {'is_current': False, 'lerp': self.punch_idle},
            'run_punch': {'is_current': False, 'lerp': self.run_punch},
            'punch_run': {'is_current': False, 'lerp': self.punch_run},
            'walk_punch': {'is_current': False, 'lerp': self.walk_punch},
            'punch_walk': {'is_current': False, 'lerp': self.punch_walk},
            'walkback_punch': {'is_current': False, 'lerp': self.walkback_punch},
            'punch_walkback': {'is_current': False, 'lerp': self.punch_walkback},
            'walkback_run': {'is_current': False, 'lerp': self.walkback_run},
            'run_walkback': {'is_current': False, 'lerp': self.run_walkback},
            'walkback_walk': {'is_current': False, 'lerp': self.walkback_walk},
            'walk_walkback': {'is_current': False, 'lerp': self.walk_walkback},
        }

    def finish_running_lerps(self):
        for _, lerp_details in self.animations.items():
            if lerp_details['lerp'].is_playing():  # noqa
                lerp_details['lerp'].finish()  # noqa

    def move_soldier(self, action):
        self.finish_running_lerps()
        new_action = action.lower()

        for key, val in self.animations.items():
            if val['is_current'] is True:
                _, old_action = key.split('_')
                if old_action == new_action:
                    continue
                next_direction = '%s_%s' % (old_action, new_action)
                self.animations[next_direction]['is_current'] = True
                self.animations[next_direction]['lerp'].start()  # noqa
                self.animations[key]['is_current'] = False
                break

        if new_action != 'punch':
            self.soldier.loop(action)
        else:
            self.soldier.play(action)

    def walk_forward(self):
        self.move_soldier('Walk')

    def run_forward(self):
        self.move_soldier('Run')

    def walk_backward(self):
        self.move_soldier('WalkBack')

    def stop(self):
        self.move_soldier('Idle')

    def punch(self):
        self.move_soldier('Punch')

    def turn_left(self):
        self.soldier_heading += 5
        self.soldier.set_h(self.soldier_heading)  # noqa

    def turn_right(self):
        self.soldier_heading -= 5
        self.soldier.set_h(self.soldier_heading)  # noqa

    # def get_mouse_coords_task(self, task):
    #     current = int(task.time) % 5
    #     if not self.printing_coords and current == 0:
    #         self.printing_coords = True
    #         print('%f, %f, %f' % (self.camera.get_x(),
    #                               self.camera.get_y(),
    #                               self.camera.get_z()))
    #     if current != 0:
    #         self.printing_coords = False
    #
    #     return Task.cont


if __name__ == '__main__':
    app = Panda3dWalking()
    app.run()
