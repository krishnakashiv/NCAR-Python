import Nio, Ngl
import numpy as np

f1 = Nio.open_file("~/Desktop/dask/cmaTLL.nc")
f2 = Nio.open_file("~/Desktop/dask/cmaTLL_NCL.nc")

u = f1.variables["xAnom"][0,:,:]
v = f2.variables["xAnom"][0,:,:]

w = v-u

print(w.min())
print(w.max())



tlat = f1.variables["TLAT"][:,0]
ulat = f1.variables["ULAT"][:,0]
lat = np.concatenate((tlat,ulat))

tlon = f1.variables["TLON"][0,:]
ulon = f1.variables["ULON"][0,:]
lon = np.concatenate((tlon, ulon))

#lat = f1.variables["lat"][:]
#lon = f1.variables["lon"][:]



#-- open a workstation
wkres             =  Ngl.Resources()            #-- generate an resources object for workstation
wkres.wkColorMap  = "BkBlAqGrYeOrReViWh200"                   #-- choose colormap
wkres.wkWidth     =  1024                       #-- width of workstation
wkres.wkHeight    =  1024                       #-- height of workstation
wks_type          = "png"                       #-- output type
wks               =  Ngl.open_wks(wks_type,"calc_mon_anom_TLL",wkres)  #-- open workstation




#minval =  0.                                #-- minimum contour level
#maxval =  30.                               #-- maximum contour level
#inc    =  2.5                                #-- contour level spacing
#ncn    = (maxval-minval)/inc + 1               #-- number of contour levels



#-- set res
mpres                       =  Ngl.Resources()    #-- generate an res object for plot
mpres.nglDraw               = False               #-- don't draw individual plots
mpres.nglFrame              = False               #-- don't advance frame


#-- contour resources
mpres.cnFillOn              =  True               #-- turn on contour fill
mpres.cnFillPalette         =  True
mpres.cnLineLabelsOn        =  False              #-- turn off line labels
mpres.cnInfoLabelOn         =  False              #-- turn off info label
#res.cnLevelSelectionMode  = "ManualLevels"      #-- set manual levels
#res.cnMinLevelValF        =  minval             #-- minimum value
#res.cnMaxLevelValF        =  maxval             #-- maximum value
#res.cnLevelSpacingF       =  inc                #-- increment

mpres.sfXArray               =  lon
mpres.sfXArray               =  lat

#-- axis label
#res.tiXAxisString          = "Longitude"
#res.tiYAxisString          = "Latitude"

# mpres

mpres.nglMaximize          = False
mpres.mpOutlineOn          = True
mpres.mpLimitMode          = "LatLon"

mpres.mpProjection         = "Stereographic"
mpres.mpEllipticalBoundary = True

mpres.mpMaxLatF             =  90.              #-- maximum latitude; northern hemisphere
mpres.mpMinLatF             =  30.              #-- minimum latitude
mpres.mpCenterLatF          =  90.              #-- center latitude
#map = Ngl.map(wks,mpres)                        #-- create base map

#Ngl.draw(map)                                   #-- draw map

#-- labelbar resources
mpres.pmLabelBarDisplayMode = "Never"             #-- turn off the label bar

#-- assign plot array for all 3 plots
plot = []

#-- create the plots, but don't draw it yet
#-- plot 1
mpres.tiMainString            = "Python Output"     #-- title string
mpres.tiMainFont        = "Helvetica-bold"
mpres.tiMainOffsetXF          = -0.07
mpres.mpProjection         = "Stereographic"
mpres.mpEllipticalBoundary = True
plot.append(Ngl.contour_map (wks,u,mpres))   #-- time = 0

#-- plot 2
mpres.tiMainString              = "NCL Output"     #-- title string
mpres.tiMainFont        = "Helvetica-bold"
mpres.tiMainOffsetXF          = -0.08
mpres.mpProjection         = "Stereographic"
mpres.mpEllipticalBoundary = True
plot.append(Ngl.contour_map (wks,v,mpres)) #-- time = 0

#-- plot 3
mpres.tiMainString              = "(NCL-Python) Output"     #-- title string
mpres.tiMainFont        = "Helvetica-bold"
mpres.tiMainOffsetXF          = -0.05
mpres.mpProjection         = "Stereographic"
mpres.mpEllipticalBoundary = True
plot.append(Ngl.contour_map (wks,w,mpres)) #-- time = 0

textres = Ngl.Resources()
textres.txFontHeightF = 0.013
textres.txFont        = "Helvetica-bold"
textres.txFontThicknessF = 3
Ngl.text_ndc(wks,"calcMonAnomTLL",0.5,.97,textres)  #-- add title to plot

#-- set some panel resources: a common labelbar and title
#-- "[3,1]" indicates 3 row, 1 columns
panelres                  =  Ngl.Resources()
panelres.nglFrame         = False
panelres.nglPanelLabelBar =  True               #-- common labelbar
panelres.nglPanelTop         =  0.95
panelres.nglPanelBottom      =  0.01               #-- bottom position of panel

panelres.lbTitleString    = "salt flux ice to ocn (cpl) in kg/m^2/day"
panelres.lbTitleFontHeightF = 0.01
panelres.lbTitleFont      = "Helvetica-bold"
panelres.pmLabelBarOrthogonalPosF = 0.10

#-- create the panel
Ngl.panel(wks,plot,[3,1],panelres)


#Ngl.overlay(map,plot)                           #-- overlay this contour on map
#Ngl.draw(map)                                   #-- draw the map


#-- advance the frame
Ngl.frame(wks)

#-- done
Ngl.end()
