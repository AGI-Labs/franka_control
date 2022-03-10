import os
import time

import argparse
import glob
import numpy as np
import yaml

from franka_env import FrankaEnv
from util import Rate, TIME, HZ, HOMES


parser = argparse.ArgumentParser()
parser.add_argument("name")
parser.add_argument("--task", type=str, default="pour")


def _get_filename(dir, input, task):
    index = 0
    for name in glob.glob("{}/{}_{}_*.npz".format(dir, input, task)):
        n = int(name[:-4].split("_")[-1])
        if n >= index:
            index = n + 1
    return "{}/{}_{}_{}.npz".format(dir, input, task, index)


if __name__ == "__main__":
    args = parser.parse_args()
    name = args.name
    task = args.task

    home = HOMES[task]
    env = FrankaEnv(home=home, hz=HZ, gain_type="record", camera=False)

    while True:
        filename = _get_filename("data", name, task)

        user_in = "r"
        while user_in == "r":
            env.reset()
            user_in = input("Ready. Recording {}".format(filename))

        joints = []
        for state in range(int(TIME * HZ) - 1):
            joints.append(env.step(None)[0]["q"])
        env.close()

        if not os.path.exists("./data"):
            os.mkdir("data")
        np.savez(filename, home=home, hz=HZ, traj=joints)
