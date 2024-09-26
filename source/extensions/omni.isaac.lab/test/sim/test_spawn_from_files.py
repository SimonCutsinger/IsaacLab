# Copyright (c) 2022-2024, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from omni.isaac.lab.app import AppLauncher, run_tests

"""Launch Isaac Sim Simulator first."""

# launch omniverse app
simulation_app = AppLauncher(headless=True).app

"""Rest everything follows."""

import unittest

import omni.isaac.core.utils.prims as prim_utils
import omni.kit.app
import omni.usd
from omni.isaac.core.simulation_context import SimulationContext

import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.utils.assets import ISAACLAB_NUCLEUS_DIR


class TestSpawningFromFiles(unittest.TestCase):
    """Test fixture for checking spawning of USD references from files with different settings."""

    def setUp(self) -> None:
        """Create a blank new stage for each test."""
        # Create a new stage
        omni.usd.get_context().new_stage()
        # Simulation time-step
        self.dt = 0.1
        # Load kit helper
        self.sim = SimulationContext(physics_dt=self.dt, rendering_dt=self.dt, backend="numpy")

    def tearDown(self) -> None:
        """Stops simulator after each test."""
        # stop simulation
        self.sim.stop()
        self.sim.clear()
        self.sim.clear_all_callbacks()
        self.sim.clear_instance()

    """
    Basic spawning.
    """

    def test_spawn_usd(self):
        """Test loading prim from Usd file."""
        # Spawn cone
        cfg = sim_utils.UsdFileCfg(usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/FrankaEmika/panda_instanceable.usd")
        prim = cfg.func("/World/Franka", cfg)
        # Check validity
        self.assertTrue(prim.IsValid())
        self.assertTrue(prim_utils.is_prim_path_valid("/World/Franka"))
        self.assertEqual(prim.GetPrimTypeInfo().GetTypeName(), "Xform")

    def test_spawn_usd_fails(self):
        """Test loading prim from Usd file fails when asset usd path is invalid."""
        # Spawn cone
        cfg = sim_utils.UsdFileCfg(usd_path=f"{ISAACLAB_NUCLEUS_DIR}/Robots/FrankaEmika/panda2_instanceable.usd")

        with self.assertRaises(FileNotFoundError):
            cfg.func("/World/Franka", cfg)

    def test_spawn_urdf(self):
        """Test loading prim from URDF file."""
        # enable URDF importer extension
        extension_manager = omni.kit.app.get_app().get_extension_manager()
        extension_manager.set_extension_enabled_immediate("omni.importer.urdf", True)
        # retrieve path to URDF importer extension
        extension_id = extension_manager.get_enabled_extension_id("omni.importer.urdf")
        extension_path = extension_manager.get_extension_path(extension_id)

        # Spawn franka from URDF
        cfg = sim_utils.UrdfFileCfg(
            asset_path=f"{extension_path}/data/urdf/robots/franka_description/robots/panda_arm_hand.urdf", fix_base=True
        )
        prim = cfg.func("/World/Franka", cfg)
        # Check validity
        self.assertTrue(prim.IsValid())
        self.assertTrue(prim_utils.is_prim_path_valid("/World/Franka"))
        self.assertEqual(prim.GetPrimTypeInfo().GetTypeName(), "Xform")

    def test_spawn_ground_plane(self):
        """Test loading prim for the ground plane from grid world USD."""
        # Spawn ground plane
        cfg = sim_utils.GroundPlaneCfg(color=(0.1, 0.1, 0.1), size=(10.0, 10.0))
        prim = cfg.func("/World/ground_plane", cfg)
        # Check validity
        self.assertTrue(prim.IsValid())
        self.assertTrue(prim_utils.is_prim_path_valid("/World/ground_plane"))
        self.assertEqual(prim.GetPrimTypeInfo().GetTypeName(), "Xform")


if __name__ == "__main__":
    run_tests()
