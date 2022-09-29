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
        self.set_lerps()
        self.turn_rate = 1.5

    def finish_running_lerps(self):
        _ = [lerp.finish() for _, lerp in self.animations.items() if lerp.is_playing()]  # noqa

    def animate_model(self, new_action):
        _, old_action = self.current_action.split('_')
        if old_action != new_action:
            self.finish_running_lerps()
            self.current_action = f'{old_action}_{new_action}'
            self.animations[self.current_action].start()  # noqa

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

    def set_lerps(self):
        transitions = (
            ('Idle', 'Walk'), ('Walk', 'Idle'),
            ('Idle', 'WalkBack'), ('WalkBack', 'Idle'),
            ('Idle', 'Run'), ('Run', 'Idle'),
            ('Run', 'Walk'), ('Walk', 'Run'),
            ('Idle', 'Punch'), ('Punch', 'Idle'),
            ('Run', 'Punch'), ('Punch', 'Run'),
            ('Walk', 'Punch'), ('Punch', 'Walk'),
            ('WalkBack', 'Punch'), ('Punch', 'WalkBack'),
            ('WalkBack', 'Run'), ('Run', 'WalkBack'),
            ('WalkBack', 'Walk'), ('Walk', 'WalkBack'),
            ('Walk', 'StrafeRight'), ('StrafeRight', 'Walk'),
            ('StrafeRight', 'WalkBack'), ('WalkBack', 'StrafeRight'),
            ('StrafeRight', 'Run'), ('Run', 'StrafeRight'),
            ('StrafeRight', 'Punch'), ('Punch', 'StrafeRight'),
            ('StrafeRight', 'Idle'), ('Idle', 'StrafeRight'),
            ('StrafeRight', 'StrafeLeft'), ('StrafeLeft', 'StrafeRight'),
            ('Walk', 'StrafeLeft'), ('StrafeLeft', 'Walk'),
            ('StrafeLeft', 'WalkBack'), ('WalkBack', 'StrafeLeft'),
            ('StrafeLeft', 'Run'), ('Run', 'StrafeLeft'),
            ('StrafeLeft', 'Punch'), ('Punch', 'StrafeLeft'),
            ('StrafeLeft', 'Idle'), ('Idle', 'StrafeLeft')
        )
        self.animations = {
            f'{transition[0]}_{transition[1]}':
                LerpAnimInterval(self.ninja, 0.25, transition[0], transition[1])
            for transition in transitions
        }
