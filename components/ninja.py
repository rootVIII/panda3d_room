from direct.actor.Actor import Actor  # noqa
from direct.interval.IntervalGlobal import LerpAnimInterval  # noqa


class Ninja:
    def __init__(self):
        self.ninja = Actor('assets/ninja.bam')
        self.ninja.loop('Idle')
        self.ninja_heading = 0
        self.ninja.enable_blend()
        self.current_action = 'Walk_Idle'
        self.animations = None
        self.set_character_lerps(self.ninja)
        self.turn_rate = 1.5

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

    def set_character_lerps(self, character):
        self.animations = {
            'Idle_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'Walk')
            },
            'Walk_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'Idle')
            },
            'Idle_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'WalkBack')
            },
            'WalkBack_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'Idle')
            },
            'Idle_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'Run')
            },
            'Run_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'Idle')
            },
            'Run_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'Walk')
            },
            'Walk_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'Run')
            },
            'Idle_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'Punch')
            },
            'Punch_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'Idle')
            },
            'Run_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'Punch')
            },
            'Punch_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'Run')
            },
            'Walk_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'Punch')
            },
            'Punch_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'Walk')
            },
            'WalkBack_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'Punch')
            },
            'Punch_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'WalkBack')
            },
            'WalkBack_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'Run')
            },
            'Run_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'WalkBack')
            },
            'WalkBack_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'Walk')
            },
            'Walk_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'WalkBack')
            },
            'Walk_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'StrafeRight')
            },
            'StrafeRight_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'Walk')
            },
            'StrafeRight_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'WalkBack')
            },
            'WalkBack_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'StrafeRight')
            },
            'StrafeRight_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'Run')
            },
            'Run_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'StrafeRight')
            },
            'StrafeRight_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'Punch')
            },
            'Punch_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'StrafeRight')
            },
            'StrafeRight_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'Idle')
            },
            'Idle_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'StrafeRight')
            },
            'StrafeRight_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeRight', 'StrafeLeft')
            },
            'StrafeLeft_StrafeRight': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'StrafeRight')
            },
            'Walk_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'Walk', 'StrafeLeft')
            },
            'StrafeLeft_Walk': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'Walk')
            },
            'StrafeLeft_WalkBack': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'WalkBack')
            },
            'WalkBack_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'WalkBack', 'StrafeLeft')
            },
            'StrafeLeft_Run': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'Run')
            },
            'Run_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'Run', 'StrafeLeft')
            },
            'StrafeLeft_Punch': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'Punch')
            },
            'Punch_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'Punch', 'StrafeLeft')
            },
            'StrafeLeft_Idle': {
                'lerp': LerpAnimInterval(character, 0.25, 'StrafeLeft', 'Idle')
            },
            'Idle_StrafeLeft': {
                'lerp': LerpAnimInterval(character, 0.25, 'Idle', 'StrafeLeft')
            }
        }