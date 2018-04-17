from mpi4py import MPI
import numpy as np
from functools import reduce
import pytest

from  .setups                 import setupGrid
from  ..model.grid            import Layout

@pytest.mark.serial
def test_FieldAligned_setup():
    nr=10
    ntheta=20
    nz=10
    nv=10
    setupGrid(nr, ntheta, nz, nv, Layout.FIELD_ALIGNED)

@pytest.mark.serial
def test_Poloidal_setup():
    nr=10
    ntheta=20
    nz=10
    nv=10
    setupGrid(nr, ntheta, nz, nv, Layout.POLOIDAL)

@pytest.mark.serial
def test_vParallel_setup():
    nr=10
    ntheta=20
    nz=10
    nv=10
    setupGrid(nr, ntheta, nz, nv, Layout.V_PARALLEL)

@pytest.mark.parallel
@pytest.mark.parametrize("splitN", [1,2,3,4,5,6])
def test_FieldAligned_setup_parallel(splitN):
    nr=10
    ntheta=20
    nz=10
    nv=10
    size=MPI.COMM_WORLD.Get_size()
    n1=max(size//splitN,1)
    n2=size//n1
    if (n1*n2!=size):
        return
    
    setupGrid(nr, ntheta, nz, nv, Layout.FIELD_ALIGNED,nProcR=n1,nProcV=n2)

@pytest.mark.parallel
@pytest.mark.parametrize("splitN", [1,2,3,4,5,6])
def test_Poloidal_setup_parallel(splitN):
    nr=10
    ntheta=20
    nz=10
    nv=10
    size=MPI.COMM_WORLD.Get_size()
    n1=max(size//splitN,1)
    n2=size//n1
    if (n1*n2!=size):
        return
    
    setupGrid(nr, ntheta, nz, nv, Layout.POLOIDAL,nProcZ=n1,nProcV=n2)

@pytest.mark.parallel
@pytest.mark.parametrize("splitN", [1,2,3,4,5,6])
def test_vParallel_setup_parallel(splitN):
    nr=10
    ntheta=20
    nz=10
    nv=10
    size=MPI.COMM_WORLD.Get_size()
    n1=max(size//splitN,1)
    n2=size//n1
    if (n1*n2!=size):
        return
    
    setupGrid(nr, ntheta, nz, nv, Layout.V_PARALLEL,nProcR=n1,nProcZ=n2)
