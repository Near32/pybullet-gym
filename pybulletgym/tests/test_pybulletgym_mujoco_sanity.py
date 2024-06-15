import gym
import numpy as np
import traceback
import pybulletgym  # required for the Bullet envs to be initialized

envs = [spec.id for spec in gym.envs.registry.values() if spec.id.find('MuJoCo') >= 0]
bugged_envs = []
for env_name in envs:
    try:
        print('[TESTING] ENV', env_name, '...')
        env = gym.make(env_name)
        #env.render(mode='human')
        env.reset()
        #time.sleep(1)
        env.step(np.random.random(env.action_space.shape))
        #time.sleep(1)
        env.close()
        print('[SUCCESS] ENV', env_name, '\n')
    except Exception as e:
        print(env_name, ': ', traceback.format_exc())
        bugged_envs.append(env_name)
        print('[FAIL] ENV', env_name, '\n')
        env.close()

print('The following envs have problems:', bugged_envs)
