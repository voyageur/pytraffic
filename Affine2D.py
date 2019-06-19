# Vector is encoded as (x,y).
# Matrix is encoded as (a11,a12,a21,a22)
# Affine transform as (a11, a12, a21, a22, tx, ty)

identity_matrix=(1,0,0,1)
identity_affine=(1,0,0,1,0,0)
zero_matrix=(0,0,0,0)
zero_vector=(0,0)

import math

def add_vector_vector(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

def add_vector(*v):
    if v==[]:
        return zero_vector
    result=v[0]
    for v1 in v[1:]:
        result=add_vector_vector(result,v1)
    return result

def multiply_scalar_vector(s,v):
    return (s*v[0],s*v[1])

def multiply_matrix_vector(m,v):
    return (m[0]*v[0]+m[1]*v[1],m[2]*v[0]+m[3]*v[1])

def multiply_matrix_matrix(m1,m2):
    return (m1[0]*m2[0]+m1[1]*m2[2],
            m1[0]*m2[1]+m1[1]*m2[3],
            m1[2]*m2[0]+m1[3]*m2[2],
            m1[2]*m2[1]+m1[3]*m2[3])

def multiply_matrix(*m):
    if m==[]:
        return identity_matrix
    result=m[0]
    for m1 in m[1:]:
        result=multiply_matrix_matrix(result,m1)
    return result

def determinant_matrix(m):
    return m[0]*m[3]-m[1]*m[2]

def inverse_matrix(m):
    d=float(determinant_matrix(m))
    return (m[3]/d,-m[1]/d,-m[2]/d,m[0]/d)

def multiply_affine_vector(a,v):
    m=a[0:4]
    t=a[4:6]
    v1=multiply_matrix_vector(m,v)
    return add_vector_vector(v1,t)

def multiply_affine_affine(a1,a2):
    m1=a1[0:4]
    t1=a1[4:6]
    m2=a2[0:4]
    t2=a2[4:6]
    m=multiply_matrix_matrix(m1,m2)
    t=multiply_affine_vector(a1,t2)
    return m+t

def multiply_affine(*a):
    if a==[]:
        return identity_affine
    result=a[0]
    for a1 in a[1:]:
        result=multiply_affine_affine(result,a1)
    return result
    

def inverse_affine(a):
    m=a[0:4]
    t=a[4:6]
    m1=inverse_matrix(m)
    t1=multiply_scalar_vector(-1,multiply_matrix_vector(m1,t))
    return m1+t1

def rotation_matrix(angle):
    return (math.cos(angle),-math.sin(angle),math.sin(angle),math.cos(angle))

def rotation_affine(angle):
    return rotation_matrix(angle)+zero_vector

def translation_affine(v):
    return identity_matrix+v

def scale_matrix(m,n):
    return (m,0,0,n)

def scale_affine(m,n):
    return (m,0,0,n,0,0)

    
