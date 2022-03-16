# Franka Control Stack
This repo provides a lightweight environment definition for the Franka Panda robot. Users can use this to collect kinesthetic demonstrations, replay action trajectories on the robot, and deploy visual imitation policies for testing. It is built upon [Polymetis](https://facebookresearch.github.io/fairo/polymetis/index.html) and the [RealSense](https://dev.intelrealsense.com/docs/python2) camera stack, and was used for the [RB2](https://rb2.info/) benchmarking project.

If you find this useful please cite:
```
@inproceedings{dasari2021rb2,
    title={RB2: Robotic Manipulation Benchmarking with a Twist},
    author={Sudeep Dasari and Jianren Wang and Joyce Hong and Shikhar Bahl and Yixin Lin and Austin Wang and Abitha Thankaraj and Karanbir Chahal and Berk Calli and Saurabh Gupta and David Held and Lerrel Pinto and Deepak Pathak and Vikash Kumar and Abhinav Gupta},
    year={2021},
    eprint={2203.08098},
    archivePrefix={arXiv},
    primaryClass={cs.RO},
    booktitle={NeurIPS 2021 Datasets and Benchmarks Track}
}
```

## Installation
Before running this code you must setup a Franka Panda and install [polymetis](https://facebookresearch.github.io/fairo/polymetis/installation.html). Note that we assume access to both a server computer (w/ real time patch) that runs the Polymetis server, and GPU enabled client computer for running `franka_control` code.


## Usage
While this codebase is quite flexible, we imagined a 3 stage pipeline for collecting demonstrations using it. These steps are outlined below:

1. Use `record.py` to collect joint trajectories kinesthetically. For example, `python record.py task_prefix --task pour`, will configure the robot to collect and save pouring demonstrations.
2. Use `python playback.py path/to/pouring_0.npz` to ingest trajectories (from the previous stage) and produce expert demonstrations without the human in the video frame. This is crucial in order to collect data with real environment dynamics.
3. Finally, use `test_policy.py` to evaluate trained policies. See the [robot_baselines](https://github.com/AGI-Labs/robot_baselines) repo for baseline policy implementations.

Note that each of these requires a Polymetis server executing *before* the code can run. You can accomplish this by running `sh launch.sh` on the configured server machine.
