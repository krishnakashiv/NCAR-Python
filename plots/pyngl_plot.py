import Nio, Ngl
import numpy as np

f1 = Nio.open_file("~/cmv/cmv_avg_opt.nc")
f2 = Nio.open_file("~/cmv/cmv_avg_opt_NCL.nc")

u = f1.variables["xMon"][0,:,:]
v = f2.variables["xMon"][0,:,:]

w = v-u

print(w.min())
print(w.max())



tlat = f1.variables["TLAT"][:,0]
ulat = f1.variables["ULAT"][:,0]
lat = np.concatenate((tlat,ulat))

tlon = f1.variables["TLONG"][0,:]
ulon = f1.variables["ULONG"][0,:]
lon = np.concatenate((tlon, ulon))


#-- open a workstation
wkres             =  Ngl.Resources()            #-- generate an resources object for workstation
#wkres.wkColorMap  = "gui_default"                   #-- choose colormap
wkres.wkWidth     =  1024                       #-- width of workstation
wkres.wkHeight    =  1024                       #-- height of workstation
wks_type          = "png"                       #-- output type
wks               =  Ngl.open_wks(wks_type,"calculate_monthly_values_avg_opt",wkres)  #-- open workstation




minval =  0.                                #-- minimum contour level
maxval =  30.                               #-- maximum contour level
inc    =  2.5                                #-- contour level spacing
ncn    = (maxval-minval)/inc + 1               #-- number of contour levels



#-- set res
res                       =  Ngl.Resources()    #-- generate an res object for plot
res.nglDraw               = False               #-- don't draw individual plots
res.nglFrame              = False               #-- don't advance frame


#-- contour resources
res.cnFillOn              =  True               #-- turn on contour fill
res.cnFillPalette         =  True
res.cnLineLabelsOn        =  False              #-- turn off line labels
res.cnInfoLabelOn         =  False              #-- turn off info label
res.cnLevelSelectionMode  = "ManualLevels"      #-- set manual levels
res.cnMinLevelValF        =  minval             #-- minimum value
res.cnMaxLevelValF        =  maxval             #-- maximum value
res.cnLevelSpacingF       =  inc                #-- increment

res.sfXArray               =  lon
res.sfXArray               =  lat

#-- axis label
res.tiXAxisString          = "Longitude"
res.tiYAxisString          = "Latitude"

# mpres
mpres = Ngl.Resources()
mpres.gsnMaximize          = True
mpres.mpOutlineOn          = True
mpres.mpLimitMode          = "LatLon"

#-- labelbar resources
res.pmLabelBarDisplayMode = "Never"             #-- turn off the label bar

#-- assign plot array for all 3 plots
plot = []

#-- create the plots, but don't draw it yet
#-- plot 1
res.tiMainString            = "Python Output"     #-- title string
res.tiMainFont        = "Helvetica-bold"
res.tiMainOffsetXF          = -0.07
plot.append(Ngl.contour (wks,u,res))   #-- time = 0

#-- plot 2
res.tiMainString              = "NCL Output"     #-- title string
res.tiMainFont        = "Helvetica-bold"
res.tiMainOffsetXF          = -0.08
plot.append(Ngl.contour (wks,v,res)) #-- time = 0

#-- plot 3
res.tiMainString              = "(NCL-Python) Output"     #-- title string
res.tiMainFont        = "Helvetica-bold"
res.tiMainOffsetXF          = -0.05
plot.append(Ngl.contour (wks,w,res)) #-- time = 0

textres = Ngl.Resources()
textres.txFontHeightF = 0.013
textres.txFont        = "Helvetica-bold"
textres.txFontThicknessF = 3
Ngl.text_ndc(wks,"calculate_monthly_values(avg,opt)",0.5,.97,textres)  #-- add title to plot

#-- set some panel resources: a common labelbar and title
#-- "[3,1]" indicates 3 row, 1 columns
panelres                  =  Ngl.Resources()
panelres.nglFrame         = False
panelres.nglPanelLabelBar =  True               #-- common labelbar
panelres.nglPanelTop         =  0.95
panelres.nglPanelBottom      =  0.01               #-- bottom position of panel

panelres.lbTitleString    = "Surface Potential Temperature in degC"
panelres.lbTitleFontHeightF = 0.01
panelres.lbTitleFont      = "Helvetica-bold"
panelres.pmLabelBarOrthogonalPosF = 0.10

#-- create the panel
Ngl.panel(wks,plot,[3,1],panelres)

#-- advance the frame
Ngl.frame(wks)

#-- done
Ngl.end()
