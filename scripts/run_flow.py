"""Run in an installed OpenLane 2.1.11 + SKY130 environment; apply patches first."""
import os
from pathlib import Path
from openlane.config import Config
from openlane.state import State
from openlane.steps import Step
root = Path(__file__).resolve().parents[1]
os.chdir(root)
Config.interactive("scan_register", PDK_ROOT=os.environ.get("PDK_ROOT", str(Path.home()/".volare")), PDK="sky130A", CLOCK_PORT="clk", CLOCK_NET="clk", CLOCK_PERIOD=10, PRIMARY_GDSII_STREAMOUT_TOOL="klayout")
state = State()
steps = [
 ("Yosys.Synthesis", {"VERILOG_FILES":[str(root/"rtl/scan_register.v")]}),
 ("OpenROAD.Floorplan", {"FP_SIZING":"absolute", "DIE_AREA":[0,0,100,100]}),
 ("OpenROAD.TapEndcapInsertion", {}), ("OpenROAD.IOPlacement", {}),
 ("OpenROAD.GeneratePDN", {"FP_PDN_VWIDTH":2,"FP_PDN_HWIDTH":2,"FP_PDN_VPITCH":30,"FP_PDN_HPITCH":30}),
 ("OpenROAD.GlobalPlacement", {}), ("OpenROAD.DetailedPlacement", {}),
 ("OpenROAD.CTS", {}), ("OpenROAD.GlobalRouting", {}),
 ("OpenROAD.DetailedRouting", {}), ("OpenROAD.FillInsertion", {}),
 ("OpenROAD.RCX", {}), ("OpenROAD.STAPostPNR", {}),
 ("KLayout.StreamOut", {}), ("Magic.DRC", {}),
 ("Magic.SpiceExtraction", {}), ("Netgen.LVS", {})]
for name, args in steps:
 step = Step.factory.get(name)(state_in=state, **args)
 step.start()
 state = step.state_out
print("Flow completed; inspect reports and metrics before accepting results.")
