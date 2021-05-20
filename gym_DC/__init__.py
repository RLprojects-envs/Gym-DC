from gym.envs.registration import register

register(
     id='DCgym-v0',
     entry_point='gym_DC.envs:DCGymEnv',
 )
