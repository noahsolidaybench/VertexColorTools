"""

	Core functionality for Vertex Color Bench (VCB) v1.0
	
	VCB offers a set of tools for editting vertex color information.
	Made by Noah Bench - noahbench.com - nbench0218@gmail.com

	Many thanks to Martin Dahlin for all his scripts have taught me about pymel

"""

## Imports
import pymel.core as pm
import math

## Initialization

## Core Functionalaity
	
# Applies a gradient to the selected mesh
def VCB_Apply():
	# Get Settings
	mode = pm.optionVar["gradientMode_VCB"]
	blendMode = pm.optionVar["blendMode_VCB"]
	# Color Settings
	colorMain = pm.optionVar["colorMain_VCB"]
	alphaMain = pm.optionVar["alphaMain_VCB"]
	colorSub = pm.optionVar["colorSub_VCB"]
	alphaSub = pm.optionVar["alphaSub_VCB"]
	# Gradient Settings
	gradientDirection = pm.optionVar["gradientDirection_VCB"]
	gradientMode = pm.optionVar["gradientBounds_VCB"]
	
	# Turn on Selection Order -- NOT WORKING
	pm.selectPref(trackSelectionOrder=True)
	
	# Get Selection and Validate
	selection = pm.ls(selection = True)
	if selection == [] or selection == None:
		errorCode(0) #no selection
		
	# Get Object Info and Validate Selections
	if mode == 1: # Standard
		# Validate
		if pm.filterExpand(selectionMask=[12,31,32,34,35]) == [] or pm.filterExpand(selectionMask=[12,31,32,34,35]) == None:
			errorCode(4) #only polygon objects or components
		
		object = pm.ls(selection, o=True)
		object = list(set(object))
		
		vertList = pm.ls( pm.polyListComponentConversion(toVertex = True), flatten = True)
		
	elif gradientMode == 1: # Mesh Bounds
		# Validate
		if pm.filterExpand(selectionMask=12) == [] or pm.filterExpand(selectionMask=12) == None:
			errorCode(1) #only meshes
				
		if len(pm.filterExpand(selectionMask=12)) > 1:
			errorCode(100) #more than one mesh warn
			
		object = pm.PyNode(selection[0])
		vertList = object.verts
		
	elif gradientMode == 2: # Point to Point
		# Order Selection
		#selection = pm.ls(selection, orderedSelection=True) ## FIX ME: Order of selection is not maintained
		
		#Validate
		if pm.filterExpand(selectionMask=31) == [] or pm.filterExpand(selectionMask=31) == None or len(pm.filterExpand(selectionMask=31)) <= 1:
			errorCode(3) #2 verts
			
		if len(pm.filterExpand(selectionMask=31)) > 2:
			errorCode(101) #more than 2 verts
		
		object = pm.ls(selection, o=True)
		object = list(set(object))

		if len(object) > 1:
			print(len(object))
			pm.error("You may only select vertices from a single mesh while performing this operation.")
		
		object = pm.PyNode(object[0])
		vertList = object.verts
	
	# Walk through our object's verts
	for vert in vertList:
		color = vert.getColor()
		
		if mode == 1: # Standard
			if blendMode == 1: # Replace
				color = [colorMain[0], colorMain[1], colorMain[2], alphaMain]
				
			elif blendMode == 2: # Add
				color += [colorMain[0], colorMain[1], colorMain[2], alphaMain]
				
			elif blendMode == 3: # Multiply
				color *= [colorMain[0], colorMain[1], colorMain[2], alphaMain]
		
		elif mode == 2: # Gradient
			# Determine how far our vert is from the bounds
			dist = VCB_GetVertexDistance( vert, gradientMode, gradientDirection, selection, object)
			
			# Blend our new color
			if blendMode == 1: # Replace
				color = VCB_GetColorAtDistance(colorMain, colorSub, alphaMain, alphaSub, dist)
				
			elif blendMode == 2: # Add
				color += VCB_GetColorAtDistance(colorMain, colorSub, alphaMain, alphaSub, dist)
				
			elif blendMode == 3: # Multiply
				color *= VCB_GetColorAtDistance(colorMain, colorSub, alphaMain, alphaSub, dist)
		
		# Apply the color
		pm.select(vert, replace = True)
		pm.polyColorPerVertex(rgb = (color[0:3]), a = color[3], colorDisplayOption = True)

	# Restore the user's selection
	pm.select(selection, replace = True)

# Apply and Close the window
def VCB_ApplyAndClose(window):
	VCB_Apply()
	pm.deleteUI(window)

def VCB_GetColorAtDistance(colorMain, colorSub, alphaMain, alphaSub, dist):
	return [colorMain[0] + (colorSub[0]-colorMain[0]) * dist, 	#red
		colorMain[1] + (colorSub[1]-colorMain[1]) * dist, 		#green
		colorMain[2] + (colorSub[2]-colorMain[2]) * dist, 		#blue
		alphaMain + (alphaSub-alphaMain) * dist] 				#alpha
	
def VCB_DistanceBetweenTwoPoints( pointOne, pointTwo ):
	return math.sqrt((pointOne.x - pointTwo.x)**2 + (pointOne.y - pointTwo.y)**2 + (pointOne.z - pointTwo.z)**2)	
	
# Return given vertex's distance between bounds as percent
def VCB_GetVertexDistance( vert, gradientMode, gradientDirection, selection, object):
	meshBounds = VCB_GetMeshBounds(object)

	if gradientMode == 2: # Point to Point
		return max(min(VCB_DistanceBetweenTwoPoints(vert.getPosition(), selection[0].getPosition()) / VCB_DistanceBetweenTwoPoints(selection[0].getPosition(), selection[1].getPosition()), 1), 0)
	elif gradientDirection == 1: # X
		return abs((vert.getPosition().x - meshBounds.max().x) / (meshBounds.max().x - meshBounds.min().x))
	elif gradientDirection == 2: # Y
		return abs((vert.getPosition().y - meshBounds.max().y) / (meshBounds.max().y - meshBounds.min().y))
	elif gradientDirection == 3: # Z
		return abs((vert.getPosition().z - meshBounds.max().z) / (meshBounds.max().z - meshBounds.min().z))

# Return the bounding box of the given mesh
def VCB_GetMeshBounds(mesh):
	return mesh.boundingBox()
		
# Create VCB Shelf button
def VCB_CreateShelfBtn():

    shelfImg = "vcb_ico_32.png"
    
    # Get top shelf as parent
    pm.mel.eval("global string $gShelfTopLevel")
    topShelf = pm.mel.eval("$temp = $gShelfTopLevel")
    currentShelf = pm.tabLayout(topShelf, query=True, selectTab=True)
    pm.setParent(topShelf + "|" + currentShelf)
    
    # Create the button
    pm.shelfButton(
        annotation="Vertex Color Bench",
        command="python(\"import sys\");"
        "if (`window -ex VCB_winMain`){"
        "    if (`window -q -iconify VCB_winMain`){"
        "        window -e -iconify 0 VCB_winMain;"
        "    }else{"
        "        window -e -iconify 1 VCB_winMain;}"
        "}else{"
        "    catchQuiet ( `python(\"del sys.modules['VCB']\")`);"
        "    catchQuiet ( `python(\"del sys.modules['VCB.VCB_UI']\")`);"
        "    catchQuiet ( `python(\"del sys.modules['VCB.VCB_core']\")`);"
        "    python(\"import VCB\");"
        "}",
        label="VCB",
        image1=shelfImg,
        sourceType="mel"
    )
	
## Error Codes
# 0 No selection
# 1 Only Meshes
# 2 At least one mesh
# 3 At least two verts
# 4 Only meshes or mesh components
## Warning Codes
# 100 More than one mesh
# 101 More than two verts

def errorCode(code, detail = "detail"):
	# No selection at all
	if code == 0:
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="You must select something before performing this operation.",
			title="Error!"
		)
		pm.error("You must select something before performing this operation.")
	
	# Only meshes allowed
	if code == 1:
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="You may only select mesh objects while performing this operation.",
			title="Error!"
		)
		pm.error("You may only select meshes while performing this operation.")
	
	# At least one mesh
	if code == 2:
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="You must have at least one mesh selected while performing this operation.",
			title="Error!"
		)
		pm.error("You must have at least one mesh selected while performing this operation.")
		
	# At least two vertices
	if code == 3:
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="You must select two mesh vertices before performing this operation.",
			title="Error!"
		)
		pm.error("You must select two mesh vertices before performing this operation.")
		
	# Only Mesh or Mesh Components
	if code == 3:
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="You may only select mesh objects or mesh components before performing this operation.",
			title="Error!"
		)
		pm.error("You may only select mesh objects or mesh components before performing this operation.")
	
	# More than one mesh selected
	if code == 100:
		"""
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="Wanring: More than one mesh is selected.\nOperation will only be performed on the first mesh.",
			title="Warning!"
		)"""
		pm.warning("Operation will only be performed on the first selected mesh.")
	
	# More than two vertices selected
	if code == 101:
		"""
		pm.confirmDialog(
			button="Ok",
			cancelButton="Ok",
			defaultButton="Ok",
			dismissString="Ok",
			message="Wanring: More than two vertices selected.\nOperation will be performed using the first two.",
			title="Warning!"
		)"""
		pm.warning("Operation will be performed using only the first two selected vertices.")