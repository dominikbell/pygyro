import numpy as np
from scipy.interpolate              import lagrange
from math                           import pi, floor, ceil

from ..splines.splines              import Spline1D, Spline2D
from ..splines.spline_interpolators import SplineInterpolator1D, SplineInterpolator2D
from ..initialisation.initialiser   import fEq
from ..initialisation               import constants

"""
def iota(r):
    return 0
    #return 0.8

def fieldline(theta,z,idx,full_z):
    return theta+iota(r0)*(full_z[idx%len(full_z)]-z)
"""

class fluxSurfaceAdvection:
    def __init__( self, eta_grid, splines, iota = constants.iota ):
        self._points = eta_grid[1:3]
        self._nPoints = (self._points[0].size,self._points[1].size)
        self._interpolator = SplineInterpolator1D(splines[0])
        self._thetaSplines = [Spline1D(splines[0]) for i in range(self._nPoints[1])]
        self._dz = eta_grid[2][1]-eta_grid[2][0]
        try:
            self._dtheta =  np.atleast_2d(self._dz * iota() / constants.R0)
        except:
            self._dtheta = np.atleast_2d(self._dz * iota(eta_grid[0]) / constants.R0).T
        
        self._bz = self._dz / np.sqrt(self._dz**2+self._dtheta**2)
    
    def step( self, f, dt, c, rGIdx = 0 ):
        assert(f.shape==self._nPoints)
        
        zDist = -c*self._bz[rGIdx]*dt
        
        Shifts = floor( zDist ) + np.array([-2,-1,0,1,2,3])
        thetaShifts = self._dtheta[rGIdx]*Shifts
        
        LagrangeVals = np.ndarray([self._nPoints[1],self._nPoints[0], 6])
        for i in range(self._nPoints[1]):
            for j in range(self._nPoints[0]):
                for k in range(6):
                    LagrangeVals[i,j,k]=k+j*6+i*6*self._nPoints[0]
        
        for i,spline in enumerate(self._thetaSplines):
            self._interpolator.compute_interpolant(f[:,i],spline)
            for j,s in enumerate(Shifts):
                LagrangeVals[(i-s)%self._nPoints[1],:,j]=spline.eval(self._points[0]+thetaShifts[j])
        
        for i,z in enumerate(self._points[1]):
            zPts = z+self._dz*Shifts
            for j in range(self._nPoints[0]):
                poly = lagrange(zPts,LagrangeVals[i,j,:])
                f[j,i] = poly(z+zDist)

class vParallelAdvection:
    def __init__( self, eta_vals, splines ):
        self._points = eta_vals[3]
        self._nPoints = (self._points.size,)
        self._interpolator = SplineInterpolator1D(splines)
        self._spline = Spline1D(splines)
        
        self.evalFunc = np.vectorize(self.evaluate)
    
    def step( self, f, dt, c, r ):
        assert(f.shape==self._nPoints)
        self._interpolator.compute_interpolant(f,self._spline)
        
        #f[:]=self._spline.eval(self._points-c*dt)
        f[:]=self.evalFunc(self._points-c*dt, r)
    
    def evaluate( self, v, r ):
        if (v<self._points[0] or v>self._points[-1]):
            return fEq(r,v);
        else:
            return self._spline.eval(v)

class poloidalAdvection:
    def __init__( self, eta_vals, splines ):
        self._points = eta_vals
        self._nPoints = (self._points[0].size,self._points[1].size)
        self._interpolator = SplineInterpolator2D(splines[0],splines[1])
        self._spline = Spline2D(splines[0],splines[1])
    
    def step( self, f, dt, c ):
        assert(f.shape==self._nPoints)
        self._interpolator.compute_interpolant(f,self._spline)
        
        #f[:]=self._spline.eval(self._points-c*dt)
