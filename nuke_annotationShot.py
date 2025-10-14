import nuke
import os
import os.path
from datetime import date
import time
import subprocess

def annotationNukeX():
    # Timestamp no longer used for filename; kept if needed elsewhere
    tdate = date.today().strftime('%y%m%d')

    frame = f'{(int(nuke.frame())):04}'

    viewer = nuke.activeViewer()
    viewerNode = viewer.node()
    activeBuffer = viewer.activeInput()
    inputNode = viewerNode.input(activeBuffer)

    topNode = nuke.toNode(nuke.tcl('full_name [topnode {0}]'.format(inputNode.name())))
    filePath = topNode['file'].getValue()
    fwi = topNode.width()
    fhi = topNode.height()
    fpa = topNode.pixelAspect()
    fwi = fwi * fpa

    # derive source filename base
    filename = filePath.split('/')[-1]
    filename = filename.split('.')[0]

    # build dated notes folder path under the project structure
    pPath = filePath.split('online')[0]
    dPath = os.path.join(pPath, "online", "_ops", "_dailies", "_notes", tdate)

    # ensure folder exists
    os.makedirs(dPath, exist_ok=True)

    # build base filename and find next available numeric suffix (.1, .2, ...)
    base_name = f"{filename}.{frame}"
    index = 1
    while True:
        fullfilename = f"{base_name}.{index}.jpg"
        fpath = os.path.join(dPath, fullfilename)
        if not os.path.exists(fpath):
            break
        index += 1

    # capture viewer to file
    nuke.activeViewer().node().capture(fpath)

    # get canvas pixel dimensions with sips + shell parsing
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

    try:
        canvwid = float(canvwid)
        canvhig = float(canvhig)
    except Exception:
        # if sips parsing failed, fall back to the capture dimensions (best-effort)
        canvwid = fwi
        canvhig = fhi

    svwid = fwi * (canvhig / fhi)    # scaled width of viewer
    svhig = fhi * (canvwid / fwi)    # scaled height of viewer

    sratio = (fwi / fhi)             # sequence ratio (format)
    vratio = (canvwid / canvhig)     # viewer ratio (canvas)

    # scale & crop to match sequence format
    if sratio > vratio:
        ssx = (svhig / 2) - (fhi / 2)
        os.system('sips --resampleWidth "' + str(int(fwi)) + '" "' + fpath + '"')
        os.system('sips --cropToHeightWidth "' + str(int(fhi)) + '" "' + str(int(fwi)) + '" "' + fpath + '"')
    else:
        ssx = (svwid / 2) - (fwi / 2)
        os.system('sips --resampleHeight "' + str(int(fhi)) + '" "' + fpath + '"')
        os.system('sips --cropToHeightWidth "' + str(int(fhi)) + '" "' + str(int(fwi)) + '" "' + fpath + '"')

    # apply ICC profile
    os.system('sips -s profile /Library/ColorSync/Profiles/Displays/StudioDisplay-7B124C67-2DD2-8F2D-1452-F1C958A0C9F4.icc "' + fpath + '"')

    # reveal results
    os.system('open "' + dPath + '"')
    os.system('open "' + fpath + '"')

    # trigger annotation tool (Cmd+Shift+A)
    time.sleep(1)
    annotools = """
    osascript -e 'tell application "System Events" to keystroke "a" using {command down, shift down}'
    """
    os.system(annotools)

    print("Saved annotation:", fpath)