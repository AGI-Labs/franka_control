import time

import argparse
import numpy as np
import torch

from franka_env import FrankaEnv
from baselines import net, agents, build_transform
from util import HOMES


parser = argparse.ArgumentParser()
parser.add_argument("pretrained")
parser.add_argument("--max_t", type=float, default=10)
parser.add_argument("--hz", type=int, default=30)
parser.add_argument("--task", type=str, default="pour")
parser.add_argument("--H", type=int, default=1)
parser.add_argument("--LSTM", action="store_true")
parser.add_argument("--gain", type=str, default="default")
parser.add_argument("--ndp", action="store_true")


if __name__ == "__main__":
    args = parser.parse_args()

    features = net.VGGSoftmax()
    if args.ndp:
        policy = net.DMPNet(features, T=args.T)
        policy.load_state_dict(torch.load(args.pretrained))
        agent = agents.OpenLoopAgent(policy.cuda().eval())
    else:
        policy = (
            net.RNNPolicy(features) if args.LSTM else net.CNNPolicy(features, H=args.H)
        )
        policy.load_state_dict(torch.load(args.pretrained))
        agent = (
            agents.RNNAgent(policy.cuda().eval())
            if args.LSTM
            else agents.ClosedLoopAgent(policy.cuda().eval(), H=args.H)
        )

    home = HOMES[args.task]
    env = FrankaEnv(home=np.array(home), hz=args.hz, gain_type=args.gain)
    img2tensor = build_transform((120, 160))

    while True:
        agent.reset()
        o, done = env.reset(), False
        user_in = input("Next? ")
        if user_in == "n":
            break
        elif user_in == "r":
            while user_in != "y":
                o = env.reset()
                user_in = input("Ready? ")

        while not done:
            start = time.time()
            with torch.no_grad():
                img = img2tensor(o["rgb"]).cuda()
                state = torch.from_numpy(o["q"]).float().cuda()
                action = agent(img[None], state[None])
                action = action.cpu().numpy()[0]
            o, r, done, info = env.step(action)
            print("hz", 1.0 / (time.time() - start))
        env.close()
        input("reset?")
