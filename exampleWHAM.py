# This file is part of AstroHOG
#
# Copyright (C) 2013-2017 Juan Diego Soler

import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

sys.path.append('/Users/jsoler/Documents/astrohog/')
from astrohog import *

from astropy.wcs import WCS
from reproject import reproject_interp

def astroHOGexampleWHAM(frame, vmin, vmax, ksz=1):
	fstr="%4.2f" % frame

	dir='WHAM/'
	hdu1=fits.open(dir+'hi_filament_cube.fits')
	hdu2=fits.open(dir+'ha_filament_cube.fits')

	v1=vmin*1000.;	v2=vmax*1000.
        v1str="%4.1f" % vmin     
	v2str="%4.1f" % vmax
	limsv=np.array([v1, v2, v1, v2])

	cube1=hdu1[0].data
	sz1=np.shape(hdu1[0].data)
	CTYPE3=hdu1[0].header['CTYPE3']
	CDELT3=hdu1[0].header['CDELT3']
	CRVAL3=hdu1[0].header['CRVAL3']
	CRPIX3=hdu1[0].header['CRPIX3']
	#zmin1=0        
	zmin1=int(CRPIX3+(v1-CRVAL3)/CDELT3)
	#zmax1=sz1[0]-1
	zmax1=int(CRPIX3+(v2-CRVAL3)/CDELT3)
	velvec1=hdu1[0].header['CRVAL3']+(np.arange(sz1[0])-hdu1[0].header['CRPIX3'])*hdu1[0].header['CDELT3']
        #np.arange(v1,v2,CDELT3)/1000.
	
	cube2=hdu2[0].data
	sz2=np.shape(hdu2[0].data)
        CTYPE3=hdu2[0].header['CTYPE3']
        CDELT3=hdu2[0].header['CDELT3']
        CRVAL3=hdu2[0].header['CRVAL3']
        CRPIX3=hdu2[0].header['CRPIX3']
        #zmin2=0
	zmin2=int(CRPIX3+(v1-CRVAL3)/CDELT3)
        #zmax2=sz2[0]-1  
	zmax2=int(CRPIX3+(v2-CRVAL3)/CDELT3)
        velvec2=hdu2[0].header['CRVAL3']+(np.arange(sz2[0])-hdu2[0].header['CRPIX3'])*hdu2[0].header['CDELT3'] 

	refhdr1=hdu1[0].header.copy()
        NAXIS31=refhdr1['NAXIS3']
        del refhdr1['NAXIS3']
        del refhdr1['CTYPE3']
        del refhdr1['CRVAL3']
        del refhdr1['CRPIX3']
        del refhdr1['CDELT3']
        del refhdr1['CUNIT3']
	del refhdr1['CNAME3']
        refhdr1['NAXIS']=2
	refhdr1['WCSAXES']=2

	refhdr2=hdu2[0].header.copy()
        NAXIS3=refhdr2['NAXIS3']
	del refhdr2['NAXIS3']
        del refhdr2['CTYPE3']
	del refhdr2['CRVAL3']
	del refhdr2['CRPIX3']
	del refhdr2['CDELT3']
	del refhdr2['CUNIT3']
	del refhdr2['CNAME3']
	del refhdr2['PV1_3']
        refhdr2['NAXIS']=2
	refhdr2['WCSAXES']=2

	newcube1=np.zeros([NAXIS31, sz2[1], sz2[2]])		

	for i in range(0, NAXIS31):
		hduX=fits.PrimaryHDU(cube1[i,:,:])
		hduX.header=refhdr1
		mapX, footprintX=reproject_interp(hduX, refhdr2)

		newcube1[i,:,:]=mapX

	#import pdb; pdb.set_trace()

	# ==========================================================================================================
	sz1=np.shape(newcube1)
	x=np.sort(newcube1.ravel())
  	minrm=x[int(0.2*np.size(x))]
	#minrm=np.std(newcube1[0,:,:])
	mask1=np.zeros(sz1)
	mask1[(newcube1 > minrm).nonzero()]=1

	sz2=np.shape(cube2)
	minrm=np.std(cube2[0,:,:])
	mask2=np.zeros(sz2)
	mask2[(cube2 > minrm).nonzero()]=1
	#mask2[:,ymin:ymax,:]=1
        #mask2[(hdu2[0].data < 0.0).nonzero()]=0
	#import pdb; pdb.set_trace()
	#corrplane=HOGcorr_cube(hdu1[0].data, hdu2[0].data, zmin1, zmax1, zmin2, zmax2, mask1=mask1, mask2=mask2)
	corrplane, corrcube=HOGcorr_cube(newcube1, cube2, zmin1, zmax1, zmin2, zmax2, ksz=ksz, mask1=mask1, mask2=mask2)
	#corrplane=HOGcorr_cube(hdu1[0].data, hdu2[0].data, zmin1, zmax1, zmin2, zmax2, ksz=5, mask1=mask1, mask2=mask2, wd=3)
	#corrplane=HOGcorr_cube(hdu1[0].data, hdu2[0].data, zmin1, zmax1, zmin2, zmax2, mask1=mask1, mask2=mask2, wd=3)
	
	strksz="%i" % ksz

	plt.imshow(corrplane, origin='lower', extent=limsv/1e3)
	plt.xlabel(r'$v_{HI}$ [km/s]')
        plt.ylabel(r'$v_{H\alpha}$ [km/s]')
        plt.yticks(rotation='vertical')
	plt.colorbar()
	plt.show()
	#plt.savefig('HOGcorrelationPlanck353GRSL'+fstr+'_b'+blimstr+'_k'+strksz+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        #plt.close()
        import pdb; pdb.set_trace()

def astroHOGexampleHIandPlanck(frame, vmin, vmax, ksz=1):
	fstr="%4.2f" % frame

	dir='/Users/jsoler/PYTHON/HItest/'
        hdu1=fits.open(dir+'lite'+'THOR_and_VGPS_HI_without_continuum_L'+fstr+'_40arcsec.fits')

        dir='/Users/jsoler/PYTHON/HItest/'
        temp=fits.open(dir+'Planck353GHzL'+fstr+'_Qmap.fits')
        Qmap=convolve_fft(temp[0].data,Gaussian2DKernel(3))
        temp=fits.open(dir+'Planck353GHzL'+fstr+'_Umap.fits')
        Umap=convolve_fft(temp[0].data,Gaussian2DKernel(3))
        temp=fits.open(dir+'Planck353GHzL'+fstr+'_LIC.fits')
        LICmap=temp[0].data
        psi=0.5*np.arctan2(-Umap,Qmap)
        Ex=np.sin(psi); Bx=-np.cos(psi)
        Ey=np.cos(psi); By= np.sin(psi)

        v1=vmin*1000.;  v2=vmax*1000.
        v1str="%4.1f" % vmin
        v2str="%4.1f" % vmax
        limsv=np.array([v1, v2, v1, v2])

        CTYPE3=hdu1[0].header['CTYPE3']
        CDELT3=hdu1[0].header['CDELT3']
        CRVAL3=hdu1[0].header['CRVAL3']
        CRPIX3=hdu1[0].header['CRPIX3']
        zmin1=int(CRPIX3+(v1-CRVAL3)/CDELT3)
        zmax1=int(CRPIX3+(v2-CRVAL3)/CDELT3)
        velvec1=CRVAL3+(np.arange(zmin1,zmax1)-CRPIX3)*CDELT3

	lmin1=hdu1[0].header['CRVAL1']-(hdu1[0].header['NAXIS1']-hdu1[0].header['CRPIX1'])*hdu1[0].header['CDELT1']
        lmax1=hdu1[0].header['CRVAL1']+(hdu1[0].header['NAXIS1']-hdu1[0].header['CRPIX1'])*hdu1[0].header['CDELT1']

	sz1=np.shape(hdu1[0].data)

	# ==========================================================================================================
        blim=1.2; blimstr="%2.1f" % blim
        ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
        mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	HIcube=hdu1[0].data
        HIcube[(mask1 == 0.).nonzero()]=0.
        HIcube[np.isnan(HIcube).nonzero()]=0.
        lvmap=HIcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1)
        plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
        ax=plt.gca()
        plt.xlabel(r'$l$ [deg]')
        plt.ylabel(r'$v$ [km/s]')
        plt.yticks(rotation='vertical')
        plt.colorbar()
        #plt.show()
	plt.savefig('VLdiagramTHORL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

        corrvecA=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ==========================================================================================================
        blim=0.8; blimstr="%2.1f" % blim
        ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
        mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	HIcube=hdu1[0].data
        HIcube[(mask1 == 0.).nonzero()]=0.
        HIcube[np.isnan(HIcube).nonzero()]=0.
        lvmap=HIcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1)
        plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
        ax=plt.gca()
        plt.xlabel(r'$l$ [deg]')
        plt.ylabel(r'$v$ [km/s]')
        plt.yticks(rotation='vertical')
        plt.colorbar()
        #plt.show()
	plt.savefig('VLdiagramTHORL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

        corrvecB=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ===========================================================================================================
        blim=0.4; blimstr="%2.1f" % blim
        ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
        mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	HIcube=hdu1[0].data
        HIcube[(mask1 == 0.).nonzero()]=0.
        HIcube[np.isnan(HIcube).nonzero()]=0.
        lvmap=HIcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1)
        plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
        ax=plt.gca()
        plt.xlabel(r'$l$ [deg]')
        plt.ylabel(r'$v$ [km/s]')
        plt.yticks(rotation='vertical')
        plt.colorbar()
        #plt.show()
	plt.savefig('VLdiagramTHORL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

        corrvecC=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# =============================================================================================================
        sz2=np.shape(Qmap)
        #testEx=np.random.uniform(low=-1., high=1., size=sz2)
        #testEy=np.random.uniform(low=-1., high=1., size=sz2)
	testEx=np.zeros(sz2)
	testEy=1.+np.zeros(sz2)
        corrvecN=HOGcorr_cubeandpol(hdu1[0].data, testEx, testEy, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

        strksz="%i" % ksz

        plt.plot(velvec1/1e3, corrvecA, 'b', label=r'$|b| <$ 1.2')
        plt.plot(velvec1/1e3, corrvecB, 'g', label=r'$|b| <$ 0.8')
        plt.plot(velvec1/1e3, corrvecC, 'r', label=r'$|b| <$ 0.4')
        plt.plot(velvec1/1e3, corrvecN, 'k')
        plt.ylabel('HOG correlation')
        plt.legend()
        #plt.show()
        plt.savefig('HOGcorrelationPlanck353THORL'+fstr+'_k'+strksz+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
	plt.close()


def astroHOGexampleCOandPlanck(frame, vmin, vmax, ksz=1):
	fstr="%4.2f" % frame

	dir='/Users/jsoler/PYTHON/COtest/'
        hdu1=fits.open(dir+'grs_L'+fstr+'.fits')

	dir='/Users/jsoler/PYTHON/HItest/'
	temp=fits.open(dir+'Planck353GHzL'+fstr+'_Qmap.fits')
        Qmap=convolve_fft(temp[0].data,Gaussian2DKernel(3))
        temp=fits.open(dir+'Planck353GHzL'+fstr+'_Umap.fits')
        Umap=convolve_fft(temp[0].data,Gaussian2DKernel(3))
        temp=fits.open(dir+'Planck353GHzL'+fstr+'_LIC.fits')
        LICmap=temp[0].data
        psi=0.5*np.arctan2(-Umap,Qmap)
        Ex=np.sin(psi); Bx=-np.cos(psi)
        Ey=np.cos(psi); By= np.sin(psi)

        v1=vmin*1000.;  v2=vmax*1000.
        v1str="%4.1f" % vmin
        v2str="%4.1f" % vmax
        limsv=np.array([v1, v2, v1, v2])

        CTYPE3=hdu1[0].header['CTYPE3']
        CDELT3=hdu1[0].header['CDELT3']
        CRVAL3=hdu1[0].header['CRVAL3']
        CRPIX3=hdu1[0].header['CRPIX3']
        zmin1=int(CRPIX3+(v1-CRVAL3)/CDELT3)
        zmax1=int(CRPIX3+(v2-CRVAL3)/CDELT3)
        velvec1=CRVAL3+(np.arange(zmin1,zmax1)-CRPIX3)*CDELT3

	lmin1=hdu1[0].header['CRVAL1']-(hdu1[0].header['NAXIS1']-hdu1[0].header['CRPIX1'])*hdu1[0].header['CDELT1']
	lmax1=hdu1[0].header['CRVAL1']+(hdu1[0].header['NAXIS1']-hdu1[0].header['CRPIX1'])*hdu1[0].header['CDELT1']

        sz1=np.shape(hdu1[0].data)

	# ===========================================================================================================
	blim=1.2; blimstr="%2.1f" % blim
	ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
	ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
	mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	COcube=hdu1[0].data
	COcube[(mask1 == 0.).nonzero()]=0.
	COcube[np.isnan(COcube).nonzero()]=0.
	lvmap=COcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1)	
	plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
	ax=plt.gca()
	plt.xlabel(r'$l$ [deg]')
	plt.ylabel(r'$v$ [km/s]')
	plt.yticks(rotation='vertical')
	plt.colorbar()
	#plt.show()
	plt.savefig('VLdiagramGRSL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

	corrvecA=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ===========================================================================================================
	blim=0.8; blimstr="%2.1f" % blim
        ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
        mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	COcube=hdu1[0].data
        COcube[(mask1 == 0.).nonzero()]=0.
        COcube[np.isnan(COcube).nonzero()]=0.
        lvmap=COcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1)
        plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
        plt.xlabel(r'$l$ [deg]')
        plt.ylabel(r'$v$ [km/s]')
        plt.yticks(rotation='vertical')
        plt.colorbar()
        #plt.show()
	plt.savefig('VLdiagramGRSL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

        corrvecB=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ===========================================================================================================	
	blim=0.4; blimstr="%2.1f" % blim
        ymax=int(hdu1[0].header['CRPIX2']+( blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        ymin=int(hdu1[0].header['CRPIX2']+(-blim-hdu1[0].header['CRVAL2'])/hdu1[0].header['CDELT2'])
        mask1=np.zeros(sz1)
        mask1[:,ymin:ymax,:]=1
        mask1[(hdu1[0].data < 0.0).nonzero()]=0

	COcube=hdu1[0].data
        COcube[(mask1 == 0.).nonzero()]=0.
        COcube[np.isnan(COcube).nonzero()]=0.
        lvmap=COcube[zmin1:zmax1,ymin:ymax,:].sum(axis=1) 
        plt.imshow(lvmap, origin='lower', extent=[lmin1,lmax1,vmin,vmax], aspect='auto')
        plt.xlabel(r'$l$ [deg]')
        plt.ylabel(r'$v$ [km/s]')
        plt.yticks(rotation='vertical')
	plt.colorbar()
	#plt.show()
	plt.savefig('VLdiagramGRSL'+fstr+'_b'+blimstr+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
        plt.close()

        corrvecC=HOGcorr_cubeandpol(hdu1[0].data, Ex, Ey, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ==============================================================================================================
	sz2=np.shape(Qmap)
	testEx=np.zeros(sz2)
        testEy=1.+np.zeros(sz2)
	corrvecN=HOGcorr_cubeandpol(hdu1[0].data, testEx, testEy, zmin1, zmax1, ksz=ksz, mask1=mask1, rotatepol=True)

	# ==============================================================================================================
	strksz="%i" % ksz

	plt.plot(velvec1/1e3, corrvecA, 'b', label=r'$|b| <$ 1.2')
	plt.plot(velvec1/1e3, corrvecB, 'g', label=r'$|b| <$ 0.8')
	plt.plot(velvec1/1e3, corrvecC, 'r', label=r'$|b| <$ 0.4')
	plt.plot(velvec1/1e3, corrvecN, 'k')
	plt.ylabel('HOG correlation')
	plt.legend()
	#plt.show()
	plt.savefig('HOGcorrelationPlanck353GRSL'+fstr+'_k'+strksz+'_v'+v1str+'to'+v2str+'.png', bbox_inches='tight')
	plt.close()	

	#import pdb; pdb.set_trace()

ksz=3
#astroHOGexampleHIandPlanck(23.75, -5., 135., ksz=9)
#astroHOGexampleCOandPlanck(23.75,  -5., 135., ksz=9)
#astroHOGexampleHIandCO(23.75,  -5.,  30., ksz=ksz)
astroHOGexampleWHAM(23.75, -45., 45., ksz=ksz)



