from pybulletgym.envs.roboschool.robots.robot_bases import MJCFBasedRobot
import numpy as np


class InvertedPendulum(MJCFBasedRobot):
    swingup = False

    def __init__(self, model_xml="inverted_pendulum.xml"):
        MJCFBasedRobot.__init__(self, model_xml, 'cart', action_dim=1, obs_dim=5)

    def robot_specific_reset(self, bullet_client):
        self._p = bullet_client
        self.pole = self.parts["pole"]
        self.slider = self.jdict["slider"]
        self.j1 = self.jdict["hinge"]
        u = self.np_random.uniform(low=-.1, high=.1)
        self.j1.reset_current_position( u if not self.swingup else 3.1415+u , 0)
        self.j1.set_motor_torque(0)

    def apply_action(self, a):
        assert( np.isfinite(a).all() )
        if not np.isfinite(a).all():
            print("a is inf")
            a[0] = 0
        self.slider.set_motor_torque(  100*float(np.clip(a[0], -1, +1)) )

    def calc_state(self):
        self.theta, self.theta_dot = self.j1.current_position()
        self.x, self.x_dot = self.slider.current_position()
        assert( np.isfinite(self.x) )

        if not np.isfinite(self.x):
            print("x is inf")
            self.x = 0

        if not np.isfinite(self.x_dot):
            print("x_dot is inf")
            self.x_dot = 0

        if not np.isfinite(self.theta):
            print("theta is inf")
            self.theta = 0

        if not np.isfinite(self.theta_dot):
            print("theta_dot is inf")
            self.theta_dot = 0

        return np.array([
            self.x, self.x_dot,
            np.cos(self.theta), np.sin(self.theta), self.theta_dot
        ])


class InvertedPendulumSwingup(InvertedPendulum):
    swingup = True
