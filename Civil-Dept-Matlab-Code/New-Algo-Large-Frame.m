close all
clear all
clc
format long

%=================PROBLEM DEFINITION===========================
noe=70;%number of elements
ndofpn=3; %number of degrees of freedoms per node
nonpe=2; %number of nodes per element
tdof=132;

%................Defining elements related vectors........................
%FIRST NUMBER THE COLUMNS
Last_column_number=40;
Column_height=3.2;
beam_length=5;
L=zeros(1,noe);
angle=zeros(1,noe);
width=zeros(noe,1); %width of an element in m
d=zeros(noe,1); %depth of an element in m
number_of_steel_layers=zeros(noe,1);
ysteel=zeros(noe,2); %distance to steel layers from middle(top to bottom), rows represent elements
nobars=zeros(noe,2); %columns represent layers, rows represent elements
dofbars=zeros(noe,2); %columns represent layers, rows represent elements
for xyz=1:noe
    if xyz<=Last_column_number
        
        L(1,xyz)=Column_height;
        angle(1,xyz)=pi/2; %In radians
        width(xyz,1)=0.4;
        d(xyz,1)=0.4;
        number_of_steel_layers(xyz,1)=2;
        ysteel(xyz,:)=[0.175 -0.175];
        nobars(xyz,:)=[4 4];
        dofbars(xyz,:)=[0.02 0.02];
    else
         L(1,xyz)=beam_length;
         angle(1,xyz)=0; %In radians
         width(xyz,1)=0.4;
         d(xyz,1)=0.6;
         number_of_steel_layers(xyz,1)=2;
         ysteel(xyz,:)=[0.275 -0.275];
         nobars(xyz,:)=[4 4];
         dofbars(xyz,:)=[0.02 0.02];
    end
end
% L=[ ]; %length of one element in m
BC=[1 2 3 34 35 36 67 68 69 100 101 102];%Boundary conditions (type the nodes in ascending order)
Load_applied_dof=31;
Load_vector=zeros(tdof,1);
Load_vector(Load_applied_dof,1)=1; %input the external load vector


ECM=[1 2 3 4 5 6 7 8 9 10 12 13 14 15 16 17 18 19 20 21 23 24 25 26 27 28 29 30 31 32 34 35 36 37 38 39 40 41 42 43 2 13 24 3 14 25 4 15 26 5 16 27 6 17 28 7 18 29 8 19 30 9 20 31 10 21 32 11 22 33; 2 3 4 5 6 7 8 9 10 11 13 14 15 16 17 18 19 20 21 22 24 25 26 27 28 29 30 31 32 33 35 36 37 38 39 40 41 42 43 44 13 24 35 14 25 36 15 26 37 16 27 38 17 28 39 18 29 40 19 30 41 20 31 42 21 32 43 22 33 44]; % element connectivity (Columns represent element number)

nIP=6; % number of integration points
if nIP==3
    wh=[1/3 4/3 1/3];
    x=[-1 0 1];
elseif nIP==4
    wh=[5/6 1/6 1/6 5/6];
    x=[-1 -0.447214 0.447214 1];
elseif nIP==5
    wh=[1/10 49/90 32/45 49/90 1/10];
    x=[-1 -0.654654 0 0.654654 1];
elseif nIP==6
    wh=[0.066667 0.378475 0.554858 0.554858 0.378475 0.066667];%weights for each integral point
    x=[-1 -0.765055 -0.285232 0.285232 0.765055 1]; %integral points locations
end
%............Fiber section...................................




nof=20; %number of fibers





%=================DATA FOR ITERATIONS===============================

displacement_step=0.0001;%Displacement increment in m (Put with the sign)
displacement_steps=500000;
max_i=100;
max_z=200;

....Newton raphson convergence criteria....
tol_force_i=10^(-10); %hhh=1

%....Section level convergence criteria.....
tol_force_z=10^(-10);





%===============MATERIAL MODELS=======================

%...........concrete.......... 

fc_dash= -42800; %in Kpa
ec_dash= -0.002;
fc_crack=(0.33*(-fc_dash*10^-3)^0.5)*1000;
npop=0.8+(-fc_dash*0.001/17);
E=fc_dash*((npop-1+(0/ec_dash)^(npop*1))*(npop/ec_dash)-npop*(0/ec_dash)*(npop*1*(0/ec_dash)^(npop*1-1)*(1/ec_dash)))/(npop-1+(0/ec_dash)^(npop*1))^2;
ec_crack=fc_crack/E;

%----------Reinforcement details-----------
Esteel=200000000;
Strain_hardening=0.06;
yield_strain=0.0023;
% %top
% ntop=4;
% dtop=0.020;
% ytop=d/2-0.025-(dtop/2);
% Atop=(pi*ntop*dtop^2)/4;
% %bottom
% nbottom=2;
% dbottom=0.016;
% ybottom=-((d/2)-0.025-(dbottom/2));
% Abottom=(pi*nbottom*dbottom^2)/4;

%.......steel layer details..........


Areaoflayers=zeros(noe,max(number_of_steel_layers));
for eww=1:noe
    for ii=1:number_of_steel_layers(eww,1)
        Areaoflayers(eww,ii)=(pi*nobars(eww,ii)*(dofbars(eww,ii))^2)/4;
    end
end



%===================SOURCE CODE==================================



SC=[BC Load_applied_dof];

LCM=zeros(nonpe*ndofpn,noe);

B_C=zeros(tdof,1);
for yy=1:tdof
    B_C(yy,1)=yy;
end
B_C(SC,:)=[];

for eee=1:noe
    for ppp=1:nonpe
        for qqq=1:ndofpn
            LCM(3*ppp-3+qqq,eee)=3*ECM(ppp,eee)-2+qqq-1;
        end
    end
end






Kfull=zeros(tdof,tdof); %Kfull is the complete structural stiffness matrix
hipo_element_stiffness=cell(1,noe);
hipo_element_Ke=cell(1,noe);

%..........initial section flexibility matrix.............
hipo_section_flexibility=cell(noe,nIP);
for ew=1:noe
    Afib=width(ew,1)*d(ew,1)/nof; %Area of a fiber
    for sw=1:nIP
        Kseci=zeros(2,2);
         for fib=1:nof

            yoffib=(d(ew,1)/2)*(1-(1/nof)-2*(fib-1)/nof); %y of each fiber
            Kseci=Kseci+[1 -yoffib]'*E*Afib*[1 -yoffib];

        end
        for steelfib=1:number_of_steel_layers(ew,1)
            Kseci=Kseci+[1 -ysteel(ew,steelfib)]'*Esteel*Areaoflayers(1,steelfib)*[1 -ysteel(ew,steelfib)];
        end


        fseci=inv(Kseci);
        hipo_section_flexibility{ew,sw}=fseci;

        
    end
end
section_strain=zeros(nof,1);
section_strain_steel=zeros(max(number_of_steel_layers),1);

%--------------Deriving initial element and structure stiffnesses----------
for eeee=1:noe
    fb=zeros(3,3); %fb is the element flexibility matrix for basic system 
    for t=1:nIP
        Np=[0 0 1;((x(1,t)+1)/2)-1 (x(1,t)+1)/2 0];%Force interpolation matrix
        fb=fb+Np'*fseci*Np*wh(1,t)*(L(1,eeee)/2);
    end
    RBM=[0 1/L(1,eeee) 1 0 -1/L(1,eeee) 0; 0 1/L(1,eeee) 0 0 -1/L(1,eeee) 1; -1 0 0 1 0 0];     %Rigid body matrix
    ROT=[cos(angle(1,eeee)) sin(angle(1,eeee)) 0 0 0 0; 
        -sin(angle(1,eeee)) cos(angle(1,eeee)) 0 0 0 0; 
        0 0 1 0 0 0; 0 0 0 cos(angle(1,eeee)) sin(angle(1,eeee)) 0; 
        0 0 0 -sin(angle(1,eeee)) cos(angle(1,eeee)) 0;
        0 0 0 0 0 1];
    Kb=inv(fb);
    Ke_local=RBM'*Kb*RBM; %element stiffness matrix referring local coordiCAte system
    Ke=ROT'*Ke_local*ROT; %element stiffness matrix referring global coordiCAte system
    hipo_element_stiffness{1,eeee}=Kb;
    hipo_element_Ke{1,eeee}=Ke;
    
end
    


%------Assembling--------

for q=1:noe
    for loop1=1:ndofpn*nonpe
        i1=LCM(loop1,q);
        for loop2=1:ndofpn*nonpe
            i2=LCM(loop2,q);
            Kfull(i1,i2)=Kfull(i1,i2)+hipo_element_Ke{1,q}(loop1,loop2);
        end
    end
end
Ks=Kfull;

%Finding reduced structural stiffness matrix

for a=1:length(BC)
    for b=1:tdof 
       Ks(BC(a),b)=0;
       Ks(b,BC(a))=0;
    end
    Ks(BC(a),BC(a))=1;
end 


%..............Calculation of reference load vector............

ref_disp_vector=Ks\Load_vector;
ref_force_vector=Kfull*ref_disp_vector;
reference_load=ref_force_vector/abs(ref_force_vector(Load_applied_dof,1));


hipo_element_force=cell(1,noe);
hipo_element_deformation=cell(1,noe);
for dd=1:noe
    hipo_element_force{1,dd}=[0;0;0];
    hipo_element_deformation{1,dd}=[0;0;0];
end
Tangent_stiffnesses=zeros(nof,1);

curvature=zeros(noe,nIP);
hipo_section_force=cell(noe,nIP);
hipo_section_deformation=cell(noe,nIP);
hipo_deltaehs=cell(noe,nIP);
hipo_resisting_force=cell(noe,nIP);
section_steel_strain=zeros(2,1);
for dd=1:noe
    for ww=1:nIP
       hipo_section_force{dd,ww}=[0;0];
       hipo_section_deformation{dd,ww}=[0;0];
       hipo_deltaehs{dd,ww}=[0;0];
       hipo_resisting_force{dd,ww}=[0;0];
    end
end


Un=zeros(tdof,1);
Pn1=zeros(tdof,1);
section_sigma=zeros(nof,1);
hipo_section_sigma=cell(noe,nIP);
hipo_section_strain=cell(noe,nIP);

figure  
% subplot(2,2,1); 
grid on
Gstru=animatedline('Marker','.');
addpoints(Gstru,0,0)
% axis([0 0.005 0 460]);
title('Structure')


X=zeros(displacement_steps,1);
Y=zeros(displacement_steps,1);
XC=zeros(displacement_steps,1);
YC=zeros(displacement_steps,1);
XT=zeros(displacement_steps,1);
YT=zeros(displacement_steps,1);
SXT=zeros(displacement_steps,1);
SYT=zeros(displacement_steps,1);
SXB=zeros(displacement_steps,1);
SYB=zeros(displacement_steps,1);


for n=1:displacement_steps%Displacement step

   number_of_displacement_steps = sprintf(' number_of_displacement_steps = %g', n);
    disp(number_of_displacement_steps)
    K11=Ks;
    K11(:,SC)=[];
    K11(SC,:)=[];
    
    K12=Ks;
    K12=K12(:,Load_applied_dof);
    K12(SC,:)=[];
    
    K21=Ks;
    K21=K21(Load_applied_dof,:);
    K21(:,SC)=[];
    
   
    K22=Ks(Load_applied_dof,Load_applied_dof);
    
    P1=reference_load;
    P1(SC,:)=[];
    
    P2=reference_load(Load_applied_dof,1);
    
    deltaUI=K11\P1;
    deltaUII=K11\(-K12*displacement_step);
    deltalamda=(K21*deltaUII+K22*displacement_step)/(P2-K21*deltaUI);
    lamda=deltalamda;
    deltaUi11=deltalamda*deltaUI+deltaUII;
    deltaUi=zeros(tdof,1);
    for qqq=1:length(B_C)
        deltaUi(B_C(qqq,1),1)=deltaUi11(qqq,1);
    end
    deltaUi(Load_applied_dof,1)=displacement_step;
    
    Ui=deltaUi;
    deltaUi_stiffness_cal=deltaUi;
    for i=1:max_i % Structure state determination
        
        Kfull=zeros(tdof,tdof);
        
        
        for e=1:noe %choosing the element
            Afib=width(e,1)*d(e,1)/nof; %Area of a fiber
            RBM=[0 1/L(1,e) 1 0 -1/L(1,e) 0; 0 1/L(1,e) 0 0 -1/L(1,e) 1; -1 0 0 1 0 0];     %Rigid body matrix
            
            ROT=[cos(angle(1,e)) sin(angle(1,e)) 0 0 0 0; 
                -sin(angle(1,e)) cos(angle(1,e)) 0 0 0 0; 
                0 0 1 0 0 0; 
                0 0 0 cos(angle(1,e)) sin(angle(1,e)) 0; 
                0 0 0 -sin(angle(1,e)) cos(angle(1,e)) 0;
                0 0 0 0 0 1];      % Rotational matrix
            
            deltaqerbm_global=deltaUi_stiffness_cal(LCM(:,e),1);
            deltaqerbm=ROT*deltaqerbm_global;
            deltaqe=RBM*deltaqerbm;
            fb=zeros(3,3);
            deltaQe=hipo_element_stiffness{1,e}*deltaqe; 

            for h=1:nIP %section level
                Np=[0 0 1;((x(1,h)+1)/2)-1 (x(1,h)+1)/2 0];
                deltaShs=Np*deltaQe;               
                hipo_section_force{e,h}= hipo_section_force{e,h}+deltaShs;
                
                for z=1:max_z
                    
                    Shsres=zeros(2,1);
                    Ksec=zeros(2,2);
                    deltaehs=hipo_section_flexibility{e,h}*deltaShs;
                   
                    hipo_section_deformation{e,h}=hipo_section_deformation{e,h}+deltaehs;
               
                    for fib=1:nof

                        yoffib=(d(e,1)/2)*(1-(1/nof)-2*(fib-1)/nof); %y of each fiber
                        strainfib=[1 -yoffib]*hipo_section_deformation{e,h};
                        section_strain(fib,1)=strainfib;
                        if strainfib<0
                            
                             npop=0.8+(-fc_dash*0.001/17);
                             if (strainfib/ec_dash)<1
                                kpop=1;
                              elseif (strainfib/ec_dash)>1  
                                 kpop=0.67+(-fc_dash*0.001/62);
                             end
                             sigmafib=fc_dash*((npop*(strainfib/ec_dash))/(npop-1+(strainfib/ec_dash)^(npop*kpop)));
                             Etangent=fc_dash*((npop-1+(strainfib/ec_dash)^(npop*kpop))*(npop/ec_dash)-npop*(strainfib/ec_dash)*(npop*kpop*(strainfib/ec_dash)^(npop*kpop-1)*(1/ec_dash)))/(npop-1+(strainfib/ec_dash)^(npop*kpop))^2;
                        
                            
                        else

                            if strainfib<=ec_crack
                               Etangent=E;
                               sigmafib=Etangent*strainfib;

                            else

                              sigmafib=fc_crack/(1+(200*strainfib)^0.5);   
                              Etangent=-(fc_crack*(200)^0.5)/(2*((strainfib)^0.5)*(1+(200*strainfib)^0.5)^2);

                            end
                            
                        end
                        
                        %Obtaining fibre stresses for a section 
                        section_sigma(fib,1)=sigmafib;
                        
                        Shsres= Shsres+[sigmafib*Afib; -sigmafib*Afib*(yoffib)];
                        Ksec=Ksec+[1 -(yoffib)]'*Etangent*Afib*[1 -(yoffib)];
                 
                        Tangent_stiffnesses(fib,1)=Etangent;
                        if h==1 && fib==nof
                            comfib_strain(n,1)=strainfib;
                            comfib_stress(n,1)=sigmafib;
                        end
                        if h==2 && fib==1
                            tenfib_strain(n,1)=strainfib;
                            tenfib_stress(n,1)=sigmafib;
                        end
                        
                    end
                    if h==1
                       strain_sec1=section_strain;
                       stress_sec1=section_sigma;
                    elseif h==2
                        strain_sec2=section_strain;
                       stress_sec2=section_sigma;
                    elseif h==3
                        strain_sec3=section_strain;
                       stress_sec3=section_sigma;    
                    elseif h==4
                        strain_sec4=section_strain;
                       stress_sec4=section_sigma;
                    elseif h==5
                        strain_sec5=section_strain;
                       stress_sec5=section_sigma;
                    elseif h==6
                        strain_sec6=section_strain;
                       stress_sec6=section_sigma;
                    end
                            
                    
                    
                        for steelfib=1:number_of_steel_layers(e,1)
                        strainfib_steel=[1 -(ysteel(e,steelfib))]*hipo_section_deformation{e,h};
                        section_strain_steel(steelfib,1)=strainfib_steel;

                            if abs(strainfib_steel)<=yield_strain
                                Esteelcode=Esteel;
                                sigmafib_steel=Esteelcode*strainfib_steel;
                            elseif strainfib_steel>0

                                   Esteelcode=Esteel*Strain_hardening;

                                   sigmafib_steel=Esteelcode*(abs(strainfib_steel)-yield_strain)+Esteel*yield_strain;
                            else
                                    Esteelcode=Esteel*Strain_hardening;
                                    sigmafib_steel=-Esteelcode*(abs(strainfib_steel)-yield_strain)-Esteel*yield_strain;


                            end

                            Shsres= Shsres+[sigmafib_steel*Areaoflayers(e,steelfib); -sigmafib_steel*Areaoflayers(e,steelfib)*(ysteel(e,steelfib))];
                            Ksec=Ksec+[1 -(ysteel(e,steelfib))]'*Esteelcode*Areaoflayers(e,steelfib)*[1 -(ysteel(e,steelfib))];
                            if h==1 && steelfib==number_of_steel_layers(e,1)
                                comfibsteel_strain(n,1)=strainfib_steel;
                                comfibsteel_stress(n,1)=sigmafib_steel;
                            end
                            if h==1 && steelfib==1
                                tenfibsteel_strain(n,1)=strainfib_steel;
                                tenfibsteel_stress(n,1)=sigmafib_steel;
                            end


                        end
%                     if e==1 && h==6 &&  z==1
%                         Shsres
%                        end

                    hipo_resisting_force{e,h}=Shsres;
                    if z==1 && abs(hipo_section_force{e,h}(2,1))<abs(hipo_resisting_force{e,h}(2,1))
                        uiuhfv=0;
                    end
               
                    hipo_section_sigma{e,h}=section_sigma;
                    hipo_section_strain{e,h}=section_strain;
                    
                    hipo_section_flexibility{e,h}=inv(Ksec); 
                   
                    dbstop if warning
                    Shsunb=hipo_section_force{e,h}-Shsres;
%                     if e==1 && h==4
%                     
%                         Section_force_11 = hipo_section_force{e,h}
%                         Shsres
%                         Shsunb
%                       
%                         inv(hipo_section_flexibility{e,h})
%                         section_deformation_11=hipo_section_deformation{e,h}
%                       
%                     end
                    
                    if max(abs(Shsunb))<tol_force_z
                        break
                    end
                    
                    deltaShs=Shsunb;
                end
                number_of_section_level_iterations = sprintf(' number_of_section_level_iterations = %g', z);
                disp(number_of_section_level_iterations)
                if z==max_z
                     disp('section level convergence cannot be achieved')
                     return 
                end
                
%                 if e==1 && h==6
% %                     deltaQe
% %                     Section_force_11 = hipo_section_force{1,h+(e-1)*6}
% %                     Shsres
% %                     Shsunb
%                       n
%                       inv(hipo_section_flexibility{1,h+(e-1)*6})
%                       hipo_section_deformation{1,h+(e-1)*6}
%                       hipo_resisting_force{1,h+(e-1)*6}
%                 end
                fb=fb+Np'*hipo_section_flexibility{e,h}*Np*wh(1,h)*(L(1,e)/2); 
                
            end
            hipo_element_stiffness{1,e}=inv(fb);
            
            Ke_local=RBM'* hipo_element_stiffness{1,e}*RBM;
            Ke=ROT'*Ke_local*ROT;
            for loop1=1:ndofpn*nonpe
                i1=LCM(loop1,e);
                for loop2=1:ndofpn*nonpe
                    i2=LCM(loop2,e);
                    Kfull(i1,i2)=Kfull(i1,i2)+Ke(loop1,loop2);
                end
            end 
        end
             
         Ks=Kfull;
        %Finding reduced structural stiffness matrix
         for a=1:length(BC)
             for b=1:tdof
                 Ks(BC(a),b)=0;
                 Ks(b,BC(a))=0; 
             end
                Ks(BC(a),BC(a))=1;
         end 
         
        Pres=Kfull*deltaUi;
        Rstr1=Pres;
        Rstr1(SC,:)=[];
         
        Rstr2=Pres(Load_applied_dof,1);
        if i==1
            Out_of_balance_force=lamda-Rstr2;
        else
            Out_of_balance_force=Out_of_balance_force+deltalamda-Rstr2;
        end
        
 
         
         R1=P1;
         R2=Out_of_balance_force;
         
         K11=Ks;
         K11(:,SC)=[];
         K11(SC,:)=[];

         K12=Ks;
         K12=K12(:,Load_applied_dof);
         K12(SC,:)=[];

         K21=Ks;
         K21=K21(Load_applied_dof,:);
         K21(:,SC)=[];


         K22=Ks(Load_applied_dof,Load_applied_dof);

         P1=reference_load;
         P1(SC,:)=[];

         P2=reference_load(Load_applied_dof,1);

         deltaUI=K11\P1;
         deltaUII=K11\(R1);
         deltalamda=(-R2+K21*deltaUII)/(P2-K21*deltaUI);
%          deltaF=deltalamda*reference_load;
         lamda=lamda+deltalamda;
         deltaUi11=deltalamda*deltaUI+deltaUII;
         deltaUi=zeros(tdof,1);
         for qqq=1:length(B_C)
             deltaUi(B_C(qqq,1),1)=deltaUi11(qqq,1);
         end
         deltaUi(Load_applied_dof,1)=0;
         Ui=Ui+deltaUi;
         Pcorrective=deltalamda*reference_load;
         
        for aa=1:length(BC)
            Pcorrective(BC(aa),1)=0;
        end
        Energy_tol_force=Out_of_balance_force;
        for bb=1:length(BC)
            Energy_tol_force(BC(bb),1)=0;
        end
        deltaU_corrective=Ks\Pcorrective;
        deltaUi_stiffness_cal=deltaU_corrective;
         if max(abs(Out_of_balance_force))<tol_force_i
             break
         end
%          if 0.5*(Ks\ Energy_tol_force)'*Out_of_balance_force<tol_Energy_i
%              break
%          end
        
       
    end
 %...........Updating reference load vector................
    ref_disp_vector=Ks\Load_vector;
    ref_force_vector=Kfull*ref_disp_vector;
    reference_load=ref_force_vector/abs(ref_force_vector(Load_applied_dof,1));
    Pn1=Pn1+lamda*reference_load;
    Un=Un+Ui;
    number_of_NR = sprintf(' number_of_NR = %g', i);
    disp(number_of_NR)
    if i==max_i
        disp('structure level convergence cannot be achieved')
        return
    end
    
%    %---------------plotting fibre stresses of sections for each load step--------
%    y21=zeros(nof,1);
%    for u=1:nof
%        y21(u,1)=(d/2)*(1-(1/nof)-2*(u-1)/nof);
%    end
%......section fiber stress strain variation.......


% for ee=1:noe
%     for hh=1:nIP
%         figure(4+n)
%         
%         subplot(noe,2,2*ee-1)
%         plot(hipo_section_strain{ee,hh},y21)
%         hold on 
%         title('Axial Strain')
%         grid on
%         xlabel('ex') % x-axis label
%         ylabel('Depth (m)') % y-axis label
%         
%         subplot(noe,2,2*ee)
%         plot(hipo_section_sigma{ee,hh},y21)
%         hold on 
%         title('Axial Stress')
%         grid on
%         xlabel('fcx') % x-axis label
%         ylabel('Depth (m)') % y-axis label     
%         
%         
%            
%     end
% end
% 
% 
% fpath = 'D:\images\Journal';
% fCAme = sprintf('FIG%d.png',n);
% saveas(gca, fullfile(fpath, fCAme), 'png');
% close(figure(2+n))

   
  % ------------plotting section curvature variation along the member------
% for ee=1:noe
%    figure(10000)
%    
%    subplot(noe,1,ee)
%    plot(([0; 0.234945; 0.714768; 1.285232; 1.765055; 2]*L(1,ee)/2),curvature(ee,:))
%    grid on
%    hold on
%    title(['Curvature Variation along element' num2str(ee)])
%     
% end


%.............Pushover curve......................
    X(n,1)=abs(Un(Load_applied_dof,1));
    Y(n,1)=abs(Pn1(Load_applied_dof,1));
    addpoints(Gstru,abs(Un(Load_applied_dof,1)),abs(Pn1(Load_applied_dof,1)));
    drawnow limitrate

if n==42
    jjjjj=0;
end
% Pn1
% Un
% hipo_resisting_force{1,1}
% hipo_section_deformation{1,1}
% inv(hipo_section_flexibility{1,1})

% AAA(n,1)=(-(Pn1(8,1)*2))+hipo_section_force{1,1}(2,1);

end

    
            
                
                       
                        
                
                
            
            
                    
            
            
        
        
   