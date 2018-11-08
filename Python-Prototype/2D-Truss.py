from func import *
import numpy as np

# Nodal coordinates
# -----------------

x, y = getCordinates()

# Element connectivity(ECM)
# -------------------------

ECM = getECM()
print ("ECM", ECM)

# Material properites
# -------------------

E=200*10^6

# Geomatric properties
# ---------------------

A = np.array([.0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012])
L = np.array([6, 6, 6, 6, 6*2**.5, 6, 6, 6*2**.5, 6, 6*2**.5, 6, 6*2**.5, 6])

# Additional input parameters required for coding
# -----------------------------------------------

nn=8	#;  %number of nodes
nel=13	#;  %number of elements
nen=2	#; %number of nodes in an element
ndof=2	#; %number of dof per node
n_n = nn
n_el = nel
n_en = nen
n_dof = ndof


t_dof=nn*ndof
pi = np.pi
ang = np.array([0, 0, 0, 0, pi/4*3, pi, pi, pi/4, pi/2, pi/4, pi/2, pi/4*3, pi/2])
# LCM = np.zeros((2*ndof,nel))	#; %Local Coo matrix
# K = np.zeros((nn*ndof,nn*ndof))	#; % Global stiffness matrix

# %Restrained DOF to Apply BC
# %---------------------------

BC=np.array([1, 2, 10], dtype=int)	#; %restrained dof

# %Plotting the truss
# %------------------

# for i=1:nel
#     xx=[x(ECM(1,i)) x(ECM(2,i)) x(ECM(1,i))];
#     yy=[y(ECM(1,i)) y(ECM(2,i)) y(ECM(1,i))];
#     line(xx,yy);hold on;
# end

# %Local coordinate matrix (LCM)
# %-----------------------------


dof_node = (np.arange(n_dof * n_n).reshape((n_n, n_dof)))

LCM = dof_node[ECM, :]
# LCM = (LCM.reshape(n_el, n_en*n_dof)).T

'''
%Element local stiffness matrix ke
%---------------------------------

for k=1:nel
    c=cos(Ang(k));
    s=sin(Ang(k));
    const=CArea(k)*E/L(k);
    ke=const*[c*c c*s -c*c -c*s;
        c*s s*s -c*s -s*s;
        -c*c -c*s c*c c*s;
        -c*s -s*s c*s s*s]
    
        %Structure Global stiffenss matrix
        %---------------------------------
        
        for loop1=1:nen*ndof
            i=LCM(loop1,k);
            for loop2=1:nen*ndof
                j=LCM(loop2,k);
                K(i,j)=K(i,j)+ke(loop1,loop2);
            end
        end
end
K;
inv(K);
Kf=K
'''

k_local = get_k_global(A, E, L, ang)

K = np.zeros((t_dof, t_dof))

k = np.arange(n_el, dtype=int)
cc = c*c
cs = c*s
ss = s*s

sub_arr =

'''

%Applying Boundary conditions
%----------------------------

for p=1:length(BC);
    for q=1:tdof;
        K(BC(p),q)=0;
    end
    K(BC(p),BC(p))=1;
end

'''

z = np.zeros((t_dof), dtype=int)

K[BC] = zv v

'''
K

%Force vector
%------------

f=[0;0;0;-200;0;-100;0;-100;0;0;0;0;0;0;0;0];

%Displacement vector
%-------------------

d=K\f 

%Reaction forces
%---------------

fr=Kf*d

%Axial forces
%------------

for e=1:nel
    de=d(LCM(:,e));   %displacement of the current element
    const=CArea(e)*E/L(e); %constant parameter with in the elementt
    p=Ang(e);
    c=cos(e);
    force(e)=const*[-c -s c s]*de;
end

%Plotting the axial force
%------------------------

for i=1:nel
     xx=[x(ECM(1,i)) x(ECM(2,i))];
     yy=[y(ECM(1,i)) y(ECM(2,i))];
     xm=[x(ECM(1,i))+x(ECM(2,i))]/2;
     ym=[y(ECM(1,i))+y(ECM(2,i))]/2;
     line(xx,yy);hold on;
     text(xm,ym,sprintf('%0.5g',force(i)));
end
'''
    

