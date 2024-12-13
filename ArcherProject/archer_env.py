import argparse
from omni.isaac.lab.app import AppLauncher
#arguments parcer and omniverse app launcher
#create argparse
parser = argparse.ArgumentParser(description="tutorial on creating an empty stage.")
#append applauncher's command line arguments (args)
AppLauncher.add_app_launcher_args(parser)
#parse the args
args_cli = parser.parse_args()
#launch the app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

from omni.isaac.lab.sim import SimulationCfg, SimulationContext
import omni.isaac.core.utils.prims as prim_utils
import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.utils.assets import ISAAC_NUCLEUS_DIR

#scene creation
def scene():
    #ground defined
    cfg_ground = sim_utils.GroundPlaneCfg()
    #ground created in world as defaultGroundPlane
    cfg_ground.func("/World/defaultGroundPlane", cfg_ground)
    #light defined
    cfg_light = sim_utils.DistantLightCfg(
        intensity=3000.0,
        color=(1, 0.75, 0.75),
    )
    #light creation and location
    cfg_light.func("/World/lightDistant", cfg_light, translation=(1, 0, 10))
    #xform prims for all objects below
    prim_utils.create_prim("/World/Objects","Xform")
    #red cone defined
    cfg_red_cone = sim_utils.ConeCfg(
        radius=0.15,
        height=0.5,
        visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0,0.0,0.0)),
    )
    #cone creation and location
    cfg_red_cone.func("/World/Objects/Cone1", cfg_red_cone, translation=(0.5,-0.5,1.0))
    cfg_red_cone.func("/World/Objects/Cone2", cfg_red_cone, translation=(-0.5,0.5,1.0))
    #porting and spawning usd file
    tile_cfg = sim_utils.UsdFileCfg(usd_path=f"ArcherProject/Assets/Tiles/text_blocks.usd")
    tile_cfg.func("/Wolrd/Objects/Tile", tile_cfg, translation=(0.0,0.0,0.1))

def main():
 #initialize the simulation context
    sim_cfg = SimulationCfg(dt=0.01)
    sim = SimulationContext(sim_cfg)
    #set main camera
    sim.set_camera_view([2.5, 2.5, 2.5], [0.0, 0.0, 0.0])
    #adding scene function for asset creation
    scene()
    #play
    sim.reset()
    print("[INFO]: Setup compelete.")
    #physics
    while simulation_app.is_running():
        sim.step()

if __name__ == "__main__":
    #run the function
    main()
    #close
    simulation_app.close()