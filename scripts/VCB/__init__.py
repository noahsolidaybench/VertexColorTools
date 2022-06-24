"""

	Package initiation for Vertex Color Bench (VCB) v1.0
	
	VCB offers a set of tools for editting vertex color information.
	Made by Noah Bench - noahbench.com - nbench0218@gmail.com

	Many thanks to Martin Dahlin for all his scripts have taught me about pymel

"""

## Import
import pymel.core as pm

# Option vars
import VCB_optVars as vars
vars.create()

## Startup

# Import and create UI
import VCB.VCB_UI as UI
UI.createUI()