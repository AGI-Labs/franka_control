import argparse
import glob
import numpy as np
from franka_env import FrankaEnv


parser = argparse.ArgumentParser()
parser.add_argument("file")


def _separate_filename(filename):
    split = filename[:-4].split("_")
    name = "_".join(split[:-1:])
    i = int(split[-1])
    return name, i


def _format_out_dict(list_obs, actions, hz, home):
    out_dict = {k: [] for k in list(list_obs[0].keys())}
    for obs in list_obs:
        for k in out_dict.keys():
            out_dict[k].append(obs[k])
    out_dict = {k: np.array(v) for k, v in out_dict.items()}

    out_dict["actions"] = actions
    out_dict["rate"] = hz
    out_dict["home"] = home
    return out_dict


if __name__ == "__main__":
    args = parser.parse_args()

    name, i = _separate_filename(args.file)
    num_files = len(glob.glob("data/{}_*.npz".format(name)))
    gain_type = (
        "stiff" if name.endswith("insertion") or name.endswith("zip") else "default"
    )

    data = np.load("data/" + args.file)
    home, traj, hz = data["home"], data["traj"], data["hz"]
    env = FrankaEnv(home=home, hz=hz, gain_type=gain_type, camera=False)

    for i in range(i, num_files):
        data = np.load("data/{}_{}.npz".format(name, i))

        user_in = "r"
        while user_in == "r":
            obs = [env.reset()]
            user_in = input("Ready. Loaded {} ({} hz):".format(name, hz))
        actions = []

        # Execute trajectory
        for acs in data["traj"]:
            actions.append(acs)
            obs.append(env.step(acs)[0])
        env.close()

        out_dict = _format_out_dict(obs, np.array(actions), hz, home)
        np.savez("playbacks/{}_{}.npz".format(name, i), **out_dict)
        input("Next?")
