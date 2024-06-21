import gym
from gym.envs.registration import register

for env_k in list(gym.envs.registration.registry.keys()):
    if 'Bullet' in env_k:
        del gym.envs.registration.registry[env_k]
    if 'MuJoCo' in env_k:
        del gym.envs.registration.registry[env_k]

# roboschool envs
## pendula
register(
	id='InvertedPendulumPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.pendulum.inverted_pendulum_env:InvertedPendulumBulletEnv',
	max_episode_steps=1000,
	reward_threshold=950.0,
  order_enforce=False,
	)

register(
	id='InvertedDoublePendulumPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.pendulum.inverted_double_pendulum_env:InvertedDoublePendulumBulletEnv',
	max_episode_steps=1000,
	reward_threshold=9100.0,
  order_enforce=False,
	)

register(
	id='InvertedPendulumSwingupPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.pendulum.inverted_pendulum_env:InvertedPendulumSwingupBulletEnv',
	max_episode_steps=1000,
	reward_threshold=800.0,
  order_enforce=False,
	)


## manipulators
register(
	id='ReacherPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.manipulation.reacher_env:ReacherBulletEnv',
	max_episode_steps=150,
	reward_threshold=18.0,
  order_enforce=False,
	)

register(
	id='PusherPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.manipulation.pusher_env:PusherBulletEnv',
	max_episode_steps=150,
	reward_threshold=18.0,
  order_enforce=False,
)

register(
	id='ThrowerPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.manipulation.thrower_env:ThrowerBulletEnv',
	max_episode_steps=100,
	reward_threshold=18.0,
  order_enforce=False,
)

register(
	id='StrikerPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.manipulation.striker_env:StrikerBulletEnv',
	max_episode_steps=100,
	reward_threshold=18.0,
  order_enforce=False,
)

## locomotors
register(
	id='Walker2DPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.walker2d_env:Walker2DBulletEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
	)
register(
	id='HalfCheetahPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.half_cheetah_env:HalfCheetahBulletEnv',
	max_episode_steps=1000,
	reward_threshold=3000.0,
  order_enforce=False,
	)

register(
	id='AntPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.ant_env:AntBulletEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
	)

register(
	id='HopperPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.hopper_env:HopperBulletEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
	)

register(
	id='HumanoidPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.humanoid_env:HumanoidBulletEnv',
	max_episode_steps=1000,
  order_enforce=False,
	)

register(
	id='HumanoidFlagrunPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.humanoid_flagrun_env:HumanoidFlagrunBulletEnv',
	max_episode_steps=1000,
	reward_threshold=2000.0,
  order_enforce=False,
	)

register(
	id='HumanoidFlagrunHarderPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.humanoid_flagrun_env:HumanoidFlagrunHarderBulletEnv',
	max_episode_steps=1000,
  order_enforce=False,
	)

register(
	id='AtlasPyBulletEnv-v0',
	entry_point='pybulletgym.envs.roboschool.envs.locomotion.atlas_env:AtlasBulletEnv',
	max_episode_steps=1000,
  order_enforce=False,
	)

# mujoco envs
register(
	id='InvertedPendulumMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.pendulum.inverted_pendulum_env:InvertedPendulumMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=950.0,
  order_enforce=False,
)

register(
	id='InvertedDoublePendulumMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.pendulum.inverted_double_pendulum_env:InvertedDoublePendulumMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=9100.0,
  order_enforce=False,
)

register(
	id='Walker2DMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.locomotion.walker2d_env:Walker2DMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
)
register(
	id='HalfCheetahMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.locomotion.half_cheetah_env:HalfCheetahMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=3000.0,
  order_enforce=False,
)

register(
	id='AntMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.locomotion.ant_env:AntMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
)

register(
	id='HopperMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.locomotion.hopper_env:HopperMuJoCoEnv',
	max_episode_steps=1000,
	reward_threshold=2500.0,
  order_enforce=False,
)

register(
	id='HumanoidMuJoCoEnv-v0',
	entry_point='pybulletgym.envs.mujoco.envs.locomotion.humanoid_env:HumanoidMuJoCoEnv',
	max_episode_steps=1000,
  order_enforce=False,
)


def get_list():
	envs = ['- ' + spec.id for spec in gym.pgym.envs.registry.all() if spec.id.find('Bullet') >= 0 or spec.id.find('MuJoCo') >= 0]
	return envs
