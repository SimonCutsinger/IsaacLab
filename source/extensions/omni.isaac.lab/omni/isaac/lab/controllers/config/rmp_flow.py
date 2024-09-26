# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import os

import omni.kit.app

from omni.isaac.lab.controllers.rmp_flow import RmpFlowControllerCfg

# Note: RMP-Flow config files for supported robots are stored in the motion_generation extension
extension_manager = omni.kit.app.get_app().get_extension_manager()
extension_id = extension_manager.get_enabled_extension_id(omni.isaac.motion_generation)
extension_path = extension_manager.get_extension_path(extension_id)

_RMP_CONFIG_DIR = os.path.join(extension_path, "motion_policy_configs")

# Path to current directory
_CUR_DIR = os.path.dirname(os.path.realpath(__file__))

FRANKA_RMPFLOW_CFG = RmpFlowControllerCfg(
    config_file=os.path.join(_RMP_CONFIG_DIR, "franka", "rmpflow", "franka_rmpflow_common.yaml"),
    urdf_file=os.path.join(_CUR_DIR, "data", "lula_franka_gen.urdf"),
    collision_file=os.path.join(_RMP_CONFIG_DIR, "franka", "rmpflow", "robot_descriptor.yaml"),
    frame_name="panda_end_effector",
    evaluations_per_frame=5,
)
"""Configuration of RMPFlow for Franka arm (default from `omni.isaac.motion_generation`)."""


UR10_RMPFLOW_CFG = RmpFlowControllerCfg(
    config_file=os.path.join(_RMP_CONFIG_DIR, "ur10", "rmpflow", "ur10_rmpflow_config.yaml"),
    urdf_file=os.path.join(_RMP_CONFIG_DIR, "ur10", "ur10_robot.urdf"),
    collision_file=os.path.join(_RMP_CONFIG_DIR, "ur10", "rmpflow", "ur10_robot_description.yaml"),
    frame_name="ee_link",
    evaluations_per_frame=5,
)
"""Configuration of RMPFlow for UR10 arm (default from `omni.isaac.motion_generation`)."""
