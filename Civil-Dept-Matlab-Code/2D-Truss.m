clc
clear all

%Nodal coordinates
%-----------------

x=[0 6 12 18 24 18 12 6];
y=[0 0 0 0 0 6 6 6];

%Element connectivity(ECM)
%-------------------------

ECM=[1 2 3 4 5 6 7 1 2 2 3 4 4
     2 3 4 5 6 7 8 8 8 7 7 7 6];
 
%Material properites
%-------------------

E=200*10^6;

%Geomatric properties
%---------------------

CArea=[.0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012 .0012]; %cross sec area
L=[6 6 6 6 6*sqrt(2) 6 6 6*sqrt(2) 6 6*sqrt(2) 6 6*sqrt(2) 6];

%Additional input parameters required for coding
%-----------------------------------------------

nn=8;  %number of nodes
nel=13;  %number of elements
nen=2; %number of nodes in an element
ndof=2; %number of dof per node

tdof=nn*ndof;
Ang=[0 0 0 0 pi/4*3 pi pi pi/4 pi/2 pi/4 pi/2 pi/4*3 pi/2]; 
LCM=zeros(2*ndof,nel); %Local Coo matrix
K=zeros(nn*ndof,nn*ndof); % Global stiffness matrix

%Restrained DOF to Apply BC
%---------------------------

BC=[1 2 10]; %restrained dof

%Plotting the truss
%------------------

for i=1:nel
    xx=[x(ECM(1,i)) x(ECM(2,i)) x(ECM(1,i))];
    yy=[y(ECM(1,i)) y(ECM(2,i)) y(ECM(1,i))];
    line(xx,yy);hold on;
end    

%Local coordinate matrix (LCM)
%-----------------------------

for e=1:nel;
    for j=1:nen;
        for m=1:ndof;
            ind=(j-1)*ndof+m;
            LCM(ind,e)=ndof*ECM(j,e)-ndof+m;
        end
    end
end
LCM;

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

%Applying Boundary conditions
%----------------------------

for p=1:length(BC);
    for q=1:tdof;
        K(BC(p),q)=0;
    end
    K(BC(p),BC(p))=1;
end
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
     
    

