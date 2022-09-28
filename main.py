from direct.showbase.ShowBase import ShowBase  # noqa
from direct.task import Task  # noqa
from panda3d.core import KeyboardButton, AmbientLight
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

        self.set_scene_collision_nodes(self.scene)

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

    def update(self, task):
        _ = task
        self.check_keys()
        self.move_ninja()
        return Task.cont


if __name__ == '__main__':
    app = Panda3dRoom()
    app.run()
