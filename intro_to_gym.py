import gym
import numpy as np
env = gym.make("MountainCar-v0")
env.reset()
LEARNING_RATE = 0.01
DISCOUNT = 0.95
episodes = 25000
show_life=2000
#print(env.observation_space.high)
#print(env.observation_space.low)
#print(env.action_space)
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low)/DISCRETE_OS_SIZE
#print(discrete_os_win_size)
epsilon=0.5
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = episodes // 2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING-START_EPSILON_DECAYING)

q_table=np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE+[env.action_space.n]))
print(q_table.shape)


def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

render=False
for episode in range(episodes):
    if(episode%show_life==0):
        print(episode)
        render = True
    else:
        render = False
    discrete_state=get_discrete_state(env.reset())
    done=False
    while not done:
        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(q_table[discrete_state])
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)
        new_state,reward,done,_ = env.step(action)
        new_discrete_state = get_discrete_state(new_state)
        if (render):
            env.render()
        if not done:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state+(action,)]
            new_q = (1-LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            q_table[discrete_state+(action,)] = new_q
        elif new_state[0]>=env.goal_position:
            print("we made it by {}".format(episode))
            q_table[discrete_state+(action,)] = 0
            render=True
        discrete_state = new_discrete_state
        if(END_EPSILON_DECAYING>=episode>=START_EPSILON_DECAYING):
            epsilon-=epsilon_decay_value
env.close()
