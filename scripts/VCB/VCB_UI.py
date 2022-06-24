"""

	User interface for Vertex Color Bench (VCB) v1.0
	
	VCB offers a set of tools for editting vertex color information.
	Made by Noah Bench - noahbench.com - nbench0218@gmail.com

	Many thanks to Martin Dahlin for all his scripts have taught me about pymel

"""

## Table of Contents
# Initialization
# Main Window

## Imports
import pymel.core as pm
import VCB_core as core
import VCB_optVars as vars

## Initialize

# Margins
MARGIN_SM = 4
MARGIN_MD = 8
MARGIN_LG = 12

COLUMN_01 = 100

WIN_MAIN_WIDTH = 300
WIN_MAIN_HEIGHT = 400

# UI Names
WIN_MAIN = "VCB_winMain"

FRAME_SETTINGS = "FRAME_SETTINGS"
FRAME_GRADIENT = "FRAME_GRADIENT"
FRAME_COLORS = "FRAME_COLORS"

## Main Window

def createUI():
	# Check for window duplicate
	if pm.window(WIN_MAIN, exists = True):
		pm.deleteUI(WIN_MAIN)
	
	visStateMode = True
	visStateBounds = True
	
	# Read Opt Vars and set visibility
	if pm.optionVar["gradientMode_VCB"] == 1:
		visStateMode = False
		
	if pm.optionVar["gradientBounds_VCB"] == 2:
		visStateBounds = False
	
	# Create Major UI Containers
	with pm.window(WIN_MAIN, title = "Vertex Color Bench", resizeToFitChildren = True, menuBar=True) as winVCB:
		menuTool = pm.menu(allowOptionBoxes=False, label="Tool Options", tearOff=False)
		with pm.formLayout(parent=winVCB) as formContainer:
			with pm.frameLayout(labelVisible=False, marginHeight = MARGIN_SM, marginWidth=MARGIN_SM) as frameMain:
				with pm.formLayout() as formMain:
					frameSettings = pm.frameLayout(FRAME_SETTINGS, label="Settings", collapsable=False,borderVisible=False, parent=formMain)	
					frameColors = pm.frameLayout(FRAME_COLORS, label="Colors", collapsable=True,borderVisible=False, parent=formMain)
					frameGradientOptions = pm.frameLayout(FRAME_GRADIENT, label="Gradient Options", collapsable=True, borderVisible=False, parent=formMain, enable = visStateMode)
						
	# Add Tool Menu Items
	with menuTool:
		pm.menuItem(
			label = "Reset Settings",
			annotation = "Reset all VCB settings.",
			command = lambda *args: vars.reset()
		)
		pm.menuItem(divider=True)
		pm.menuItem(
			label = "Create Shelf Button",
			annotation = "Create a shelf button on the currently active shelf.",
			command = lambda *args: core.VCB_CreateShelfBtn()
		)
	
	# Add Settings Controls
	with frameSettings:
		radioGrpGradientMode = pm.radioButtonGrp(
			label = "Mode:",
			numberOfRadioButtons = 2,
			label1 = "Standard",
			label2 = "Gradient",
			select = pm.optionVar["gradientMode_VCB"],
			changeCommand = lambda *args: SettingsOptVars(0),
			vertical = False,
			columnWidth = [1,COLUMN_01],
		)
		radioGrpBlendMode = pm.radioButtonGrp(
			label = "Blend:",
			numberOfRadioButtons = 3,
			label1 = "Replace",
			label2 = "Add",
			label3 = "Multiply",
			select = pm.optionVar["blendMode_VCB"],
			changeCommand = lambda *args: SettingsOptVars(1),
			vertical = False,
			columnWidth = [1,COLUMN_01],
		)
		
	# Settings Opt Vars
	def SettingsOptVars(varType):
		if varType == 0:
			# Adjust UI and set opt var
			if radioGrpGradientMode.getSelect() == 1: # Standard
				frameGradientOptions.setEnable(False) # Hide
				hLayoutSwapColor.setEnable(False) # Hide
				colorSub.setEnable(False) # Hide
				alphaSub.setEnable(False) # Hide
			else:
				frameGradientOptions.setEnable(True) # Show
				frameGradientOptions.setEnable(True) # Show
				hLayoutSwapColor.setEnable(True) # Show
				colorSub.setEnable(True) # Show
				alphaSub.setEnable(True) # Show
				
			pm.optionVar["gradientMode_VCB"] = radioGrpGradientMode.getSelect()
			
		elif varType == 1:
			pm.optionVar["blendMode_VCB"] = radioGrpBlendMode.getSelect()
	
	# Add Color Controls
	with frameColors:
		# Main Color
		colorMain = pm.colorSliderGrp(
			label = "Main Color:",
			rgbValue = pm.optionVar["colorMain_VCB"],
			changeCommand = lambda *args: ColorOptVars(0),
			columnWidth = [1,COLUMN_01],
		)
		alphaMain = pm.floatSliderGrp(
			label = "Main Alpha:",
			value = pm.optionVar["alphaMain_VCB"],
			changeCommand = lambda *args: ColorOptVars(1),
			field = True,
			maxValue = 1.0,
			minValue = 0.0,
			precision = 2,
			columnWidth = [1,COLUMN_01],
		)
		# Color Swap Controls
		with pm.horizontalLayout(ratios = [0,0], spacing = MARGIN_LG, enable = visStateMode) as hLayoutSwapColor:
			pm.text(
				label = "Swap Colors:",
				align = "right",
				width = 88
			)
			pm.iconTextButton(
				style = "iconOnly",
				annotation = "Swap Colors",
				command = lambda *args: SwapColors(),
				image = "vcb_swapColors_icon.png",
				width = 32,
				height = 32
			)
		
		# Sub Color
		colorSub = pm.colorSliderGrp(
			label = "Sub Color:",
			rgbValue = pm.optionVar["colorSub_VCB"],
			changeCommand = lambda *args: ColorOptVars(2),
			columnWidth = [1,COLUMN_01],
			enable = visStateMode,
		)
		alphaSub = pm.floatSliderGrp(
			label = "Sub Alpha:",
			value = pm.optionVar["alphaSub_VCB"],
			changeCommand = lambda *args: ColorOptVars(3),
			field = True,
			maxValue = 1.0,
			minValue = 0.0,
			precision = 2,
			columnWidth = [1,COLUMN_01],
			enable = visStateMode,
		)
	
	# Swap Colors
	def SwapColors():
		# Store Main
		tempColor = colorMain.getRgbValue()
		tempAlpha = alphaMain.getValue()
		# Set Main
		colorMain.setRgbValue(colorSub.getRgbValue())
		alphaMain.setValue(alphaSub.getValue())
		# Set Sub
		colorSub.setRgbValue(tempColor)
		alphaSub.setValue(tempAlpha)
		# Set Opt Vars
		ColorOptVars(0)
		ColorOptVars(1)
		ColorOptVars(2)
		ColorOptVars(3)
		
	# Color Opt Vars
	def ColorOptVars(varType):
		if varType == 0:
			pm.optionVar["colorMain_VCB"] = colorMain.getRgbValue()
		elif varType == 1:
			pm.optionVar["alphaMain_VCB"] = alphaMain.getValue()
		elif varType == 2:
			pm.optionVar["colorSub_VCB"] = colorSub.getRgbValue()
		elif varType == 3:
			pm.optionVar["alphaSub_VCB"] = alphaSub.getValue()
		
	# Add Gradient Controls
	with frameGradientOptions:
		radioGrpGradBounds = pm.radioButtonGrp(
			label = "Gradient Bounds:",
			numberOfRadioButtons = 2,
			label1 = "Mesh Bounds",
			label2 = "Point to Point",
			select = pm.optionVar["gradientBounds_VCB"],
			changeCommand = lambda *args: GradientOptVars(0),
			vertical = False,
			columnWidth = [1,COLUMN_01],
		)
		radioGrpGradDirection = pm.radioButtonGrp(
			label = "Gradient Direction:",
			numberOfRadioButtons = 3,
			label1 = "X",
			label2 = "Y",
			label3 = "Z",
			select = pm.optionVar["gradientDirection_VCB"],
			changeCommand = lambda *args: GradientOptVars(1),
			vertical = False,
			columnWidth = [1,COLUMN_01],
			enable = visStateBounds,
		)
	
	# Gradient Opt Vars
	def GradientOptVars(varType):
		if varType == 0:
			# Adjust UI and set opt var
			if radioGrpGradBounds.getSelect() == 2: # Point to Point
				radioGrpGradDirection.setEnable(False) # Hide
			else:
				radioGrpGradDirection.setEnable(True) # Show
				
			pm.optionVar["gradientBounds_VCB"] = radioGrpGradBounds.getSelect()
			
		elif varType == 1:
			pm.optionVar["gradientDirection_VCB"] = radioGrpGradDirection.getSelect()
	
	# Add the Bottom Buttons
	with formContainer:
		with pm.horizontalLayout(spacing=MARGIN_SM) as hLayoutBottomButtons:
			btnApplyAndClose = pm.button(
				annotation = 'Apply vertex color and close the tool',
				label = 'Apply Color', 
				command = lambda *args: core.VCB_ApplyAndClose(winVCB)
			)
			btnApply = pm.button(
				annotation = 'Apply vertex color',
				label = 'Apply', 
				command = lambda *args: core.VCB_Apply()
			)
			btnClose = pm.button(
				annotation = 'Closes the window.',
				label = 'Close', 
				command = lambda *args: pm.deleteUI(winVCB)
			)
			
			hLayoutBottomButtons.redistribute()
	
	
	# Format the UI Containers
	pm.formLayout(
		formMain,
		edit = True,
		attachForm = [
			(frameSettings, "top", 0),
			(frameSettings, "left", 0),
			(frameSettings, "right", 0),
			(frameColors, "left", 0),
			(frameColors, "right", 0),
			(frameGradientOptions, "left", 0),
			(frameGradientOptions, "right", 0),
		],
		attachControl = [
			(frameColors, "top", MARGIN_MD, frameSettings),
			(frameGradientOptions, "top", MARGIN_MD, frameColors),
		]
	)
	
	pm.formLayout(
		formContainer,
		edit = True,
		attachForm = [
			(frameMain, "top", MARGIN_SM),
			(frameMain, "left", MARGIN_SM),
			(frameMain, "right", MARGIN_SM),
			(hLayoutBottomButtons, "bottom", 0),
			(hLayoutBottomButtons, "left", 0),
			(hLayoutBottomButtons, "right", 0),
		]
	)