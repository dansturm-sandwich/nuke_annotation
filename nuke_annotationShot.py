import nuke
import os
import os.path
from datetime import date
import subprocess

def annotationNukeX():
	tdate = date.today().strftime('%y%m%d')

	frame = f'{(int(nuke.frame())):04}'

	fileEnd = str(frame) + ".jpg"

	viewer = nuke.activeViewer()
	viewerNode = viewer.node()
	activeBuffer = viewer.activeInput()
	inputNode = viewerNode.input(activeBuffer)

	topNode = nuke.toNode(nuke.tcl('full_name [topnode {0}]'.format(inputNode.name())))
	filePath = topNode['file'].getValue()
	fwi = topNode.width()
	fhi =  topNode.height()
	fpa = topNode.pixelAspect()
	fwi = fwi*fpa

	filename = filePath.split('/')[-1]
	filename = filename.split('.')[0]
	fullfiilename = filename + "." + fileEnd

	pPath = filePath.split('online')[0]
	dPath = pPath + "online/_ops/_dailies/_notes/" + str(tdate)

	dircmd = 'mkdir -p "' + dPath + '"'
	os.system(dircmd)

	fpath = dPath + "/" + fullfiilename

	nuke.activeViewer().node().capture(fpath)

	spw = 'sips -g pixelWidth '
	sph = 'sips -g pixelHeight '
	gpw = 'grep "pixelWidth: " '
	gph = 'grep "pixelHeight: " '
	akc = "awk '{print $2}'"
	pipe = ' | '

	wcmd = spw + '"' + fpath + '"' + pipe + gpw + pipe + akc
	hcmd = sph + '"' + fpath + '"' + pipe + gph + pipe + akc

	canvwid = subprocess.getoutput(wcmd)
	canvhig = subprocess.getoutput(hcmd)

	canvwid = float(canvwid)
	canvhig = float(canvhig)

	svwid = fwi*(canvhig/fhi)                # scaled width of viewer
	svhig = fhi*(canvwid/fwi)                # scaled height of viewer


	sratio = (fwi/fhi)        # sequence ratio (format)
	vratio = (canvwid/canvhig)        # viewer ratio (canvas)

	if sratio > vratio:
	    ssx = (svhig/2) - (fhi/2)                # position of left edge of frame
	    os.system( 'sips --resampleWidth "' + str(fwi) + '" "' + fpath + '"')
	    os.system( 'sips --cropToHeightWidth "' + str(fhi) + '" "' + str(fwi) + '" "' + fpath + '"')
	else:
	    ssx = (svwid/2) - (fwi/2)                # position of left edge of frame
	    os.system( 'sips --resampleHeight "' + str(fhi) + '" "' + fpath + '"')
	    os.system( 'sips --cropToHeightWidth "' + str(fhi) + '" "' + str(fwi) + '" "' + fpath + '"')

	os.system( 'sips -s profile /Library/ColorSync/Profiles/Displays/StudioDisplay-7B124C67-2DD2-8F2D-1452-F1C958A0C9F4.icc "' + fpath + '"')

	os.system('open "' + dPath + '"')

	os.system('open "' + fpath + '"')

	annotools = """
	osascript -e 'tell application "System Events" to keystroke "a" using {command down, shift down}' 
	"""
	os.system(annotools)
