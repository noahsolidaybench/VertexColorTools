"""

	Option variable initiation for Vertex Color Bench (VCB) v1.0
	
	VCB offers a set of tools for editting vertex color information.
	Made by Noah Bench - noahbench.com - nbench0218@gmail.com

	Many thanks to Martin Dahlin for all his scripts have taught me about pymel

"""

## Import
import pymel.core as pm


## Functions

# Create
def create():
	# Global Settings
	if "gradientMode_VCB" not in pm.env.optionVars: pm.optionVar["gradientMode_VCB"] = True
	if "blendMode_VCB" not in pm.env.optionVars: pm.optionVar["blendMode_VCB"] = True

	# Color Settings
	if "colorMain_VCB" not in pm.env.optionVars: pm.optionVar["colorMain_VCB"] = [ 1.0, 1.0, 1.0 ]
	if "alphaMain_VCB" not in pm.env.optionVars: pm.optionVar["alphaMain_VCB"] = 1.0
	if "colorSub_VCB" not in pm.env.optionVars: pm.optionVar["colorSub_VCB"] = [ 1.0, 1.0, 1.0 ]
	if "alphaSub_VCB" not in pm.env.optionVars: pm.optionVar["alphaSub_VCB"] = 1.0
	
	# Gradient Settings
	if "gradientBounds_VCB" not in pm.env.optionVars: pm.optionVar["gradientBounds_VCB"] = True
	if "gradientDirection_VCB" not in pm.env.optionVars: pm.optionVar["gradientDirection_VCB"] = True


# Reset All
def reset():

	userResponse = pm.confirmDialog(
		button=["Yes", "No"],
		cancelButton="No",
		defaultButton="No",
		dismissString="No",
		message="Do you really want to reset all VCB settings? This is not undoable.", 
		title="Reset VCB settings",
	)

	if userResponse == "No":
		pass
	else:
		pm.optionVar["gradientMode_VCB"]
		pm.optionVar["blendMode_VCB"]
		
		pm.optionVar["colorMain_VCB"] = [ 1.0, 1.0, 1.0 ]
		pm.optionVar["alphaMain_VCB"] = 1.0
		pm.optionVar["colorSub_VCB"] = [ 1.0, 1.0, 1.0 ]
		pm.optionVar["alphaSub_VCB"] = 1.0
	
		pm.optionVar["gradientBounds_VCB"] = True
		pm.optionVar["gradientDirection_VCB"] = True

		# Restart
		pm.confirmDialog(
			button=["Yes"],
			cancelButton="Yes",
			defaultButton="Yes",
			dismissString="Yes",
			message="Settings reset. Please close and restart VCB.",
			title="Reset Complete",
		)