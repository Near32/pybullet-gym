import gym, gym.spaces, gym.utils, gym.utils.seeding
import numpy as np
import pybullet
from pybullet_utils import bullet_client

from pkg_resources import parse_version
from pybulletgym.utils.logging import log_contacts, log_kinematics, log_joint_states


class BaseBulletEnv(gym.Env):
  """
  Base class for Bullet physics simulation environments in a Scene.
  These environments create single-player scenes and behave like normal Gym environments, if
  you don't use multiplayer.
  """

  metadata = {
    'render_modes': ['human', 'rgb_array'],
    'render_fps': 60,
    }

  def __init__(
    self, 
    robot, 
    render=False, 
    logs_with_joints=False, 
    timestep=0.0166,
    frame_skip=1,
    obfuscate_logs=False, 
    minimal_logs=False,
    **kwargs,
  ):
    self.scene = None
    self.physicsClientId = -1
    self.ownsPhysicsClient = 0
    self.camera = Camera()
    self.isRender = render
    self.robot = robot
    self._seed()
    self._cam_dist = 3
    self._cam_yaw = 0
    self._cam_pitch = -30
    self._render_width = 320
    self._render_height = 240
    
    self.logs_with_joints = logs_with_joints
    self.obfuscate_logs = obfuscate_logs
    self.minimal_logs = minimal_logs 
    self.timestep = timestep
    self.frame_skip = frame_skip
    self.nbr_time_steps = 0

    self.action_space = robot.action_space
    self.observation_space = robot.observation_space

  def configure(self, args):
    self.robot.args = args

  def _seed(self, seed=None):
    self.np_random, seed = gym.utils.seeding.np_random(seed)
    self.robot.np_random = self.np_random  # use the same np_randomizer for robot as for env
    return [seed]
  
  def _generate_name_swap(self):
    self.nameSwap = {f'{self.robot.robot_name}': f'{self.robot.robot_name}'}
    for part_name in self.robot.parts.keys():
      self.nameSwap[part_name] = part_name
    if self.obfuscate_logs: 
      for partIdx, part_name in enumerate(self.nameSwap.keys()):
        self.nameSwap[part_name] = f'RB{partIdx}'
     
  def _generate_logs(self):
    printoptions = np.get_printoptions()
    np.set_printoptions(formatter={'float_kind': lambda x: "%.2f" % x})
    loglist = [[f"Time: {self.nbr_time_steps * self._p.getPhysicsEngineParameters()['fixedTimeStep']:.3f}"]]
    # Function to log contact events
    # Ignore parts that have been added by the system for bookkeeping around joint configuration:
    parts = {k:v for k,v in self.robot.parts.items() if 'link' not in k}
    #parts = self.robot.parts
    list_infos = ['position', 'orientation', 'linear_velocity', 'angular_velocity']
    if self.minimal_logs:
      # TODO: update to be more general, only for cartpole now:
      parts = {'pole': parts['pole']}
      list_infos = ['angular_velocity']
    loglist.append(log_contacts(self._p, parts=parts, NS=self.nameSwap))
    loglist.append(log_kinematics(self._p, parts=parts, NS=self.nameSwap, list_infos=list_infos))
    if not self.logs_with_joints: return loglist 
    bodyIndices = []
    for part in self.robot.parts.values(): 
      if part.bodyIndex in bodyIndices: continue 
      bodyIndices.append(part.bodyIndex) 
      loglist.append(log_joint_states(self._p, robot_id=part.bodyIndex))
    np.set_printoptions(**printoptions) 
    return loglist

  def reset(self, **kwargs):
    if 'seed' in kwargs.keys(): self.seed(kwargs['seed']) 
    self.nbr_time_steps = 0
    reset_output = self._reset(**kwargs)
    self._generate_name_swap()
    if not isinstance(reset_output, tuple):
      info = {'logs': self._generate_logs()}
      reset_output = tuple([reset_output, info])
    return reset_output 
    
  def _reset(self, **kwargs):
    if self.physicsClientId < 0:
      self.ownsPhysicsClient = True

      if self.isRender:
        self._p = bullet_client.BulletClient(connection_mode=pybullet.GUI)
      else:
        self._p = bullet_client.BulletClient()

      self.physicsClientId = self._p._client
      self._p.configureDebugVisualizer(pybullet.COV_ENABLE_GUI,0)

    if self.scene is None:
      self.scene = self.create_single_player_scene(
        self._p,
        timestep=self.timestep,
        frame_skip=self.frame_skip,
    )
    if not self.scene.multiplayer and self.ownsPhysicsClient:
      self.scene.episode_restart(self._p)

    self.robot.scene = self.scene

    self.frame = 0
    self.done = 0
    self.reward = 0
    dump = 0
    s = self.robot.reset(self._p)
    self.potential = self.robot.calc_potential()
    return s

  def _render(self, mode, close=False):
    if mode == "human":
      self.isRender = True
    if mode != "rgb_array":
      return np.array([])

    base_pos = [0,0,0]
    if hasattr(self,'robot'):
      if hasattr(self.robot,'body_xyz'):
        base_pos = self.robot.body_xyz

    view_matrix = self._p.computeViewMatrixFromYawPitchRoll(
      cameraTargetPosition=base_pos,
      distance=self._cam_dist,
      yaw=self._cam_yaw,
      pitch=self._cam_pitch,
      roll=0,
      upAxisIndex=2)
    proj_matrix = self._p.computeProjectionMatrixFOV(
      fov=60, aspect=float(self._render_width)/self._render_height,
      nearVal=0.1, farVal=100.0)
    (_, _, px, _, _) = self._p.getCameraImage(
    width=self._render_width, height=self._render_height, viewMatrix=view_matrix,
      projectionMatrix=proj_matrix,
      renderer=pybullet.ER_BULLET_HARDWARE_OPENGL
      )
    rgb_array = np.array(px)
    rgb_array = rgb_array[:, :, :3]
    return rgb_array

  def _close(self):
    if self.ownsPhysicsClient:
      if self.physicsClientId >= 0:
        self._p.disconnect()
    self.physicsClientId = -1

  def HUD(self, state, a, done):
    pass

  # backwards compatibility for gym >= v0.9.x
  # for extension of this class.
  def step(self, *args, **kwargs):
    self.nbr_time_steps += 1
    step_output = self._step(*args, **kwargs)
    if len(step_output) == 4:
      info = step_output[-1]
      info['logs'] = self._generate_logs()
      step_output = list(step_output[:-1])+[False]
      step_output.append(info)
    return tuple(step_output)

  if parse_version(gym.__version__)>=parse_version('0.9.6'):
    close = _close
    render = _render
    # REMOVED in order to allow some extra post-processing:
    #reset = _reset
    seed = _seed


class Camera:
  def __init__(self):
    pass

  def move_and_look_at(self, i, j, k, x, y, z, distance=10, yaw=10, pitch=-20):
    lookat = [x, y, z]
    self._p.resetDebugVisualizerCamera(distance, yaw, pitch, lookat)
