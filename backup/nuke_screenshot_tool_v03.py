import nuke
import os
import os.path
from datetime import date

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


	filename = filePath.split('/')[-1]
	filename = filename.split('.')[0]
	fullfiilename = filename + "." + fileEnd

	pPath = filePath.split('online')[0]
	dPath = pPath + "online/_project_files/_dailies/_notes/" + str(tdate)


	dircmd = 'mkdir -p "' + dPath + '"'
	os.system(dircmd)


	fpath = dPath + "/" + fullfiilename

	nuke.activeViewer().node().capture(fpath)


	os.system( 'sips -s profile /Library/ColorSync/Profiles/Displays/StudioDisplay-7B124C67-2DD2-8F2D-1452-F1C958A0C9F4.icc "' + fpath + '"')

	os.system( 'sips --resampleHeight "' + str(fhi) + '" "' + fpath + '"')

	os.system( 'sips --cropToHeightWidth "' + str(fhi) + '" "' + str(fwi) + '" "' + fpath + '"')

	os.system('open "' + dPath + '"')

	os.system('open "' + fpath + '"')


