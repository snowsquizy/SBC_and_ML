%% Hyper Parameter Sweep Data Plot
%
% SBLT Andrew Taylor - z3457431

%% Prepare Workspace
close all;
clear;
clc;

%% Variables
load('sweep_cluster.mat');
load('sweep_desktop.mat');

neurons = [9,18,27,36,45,54,63,72,81];
neurons = [neurons,neurons,neurons,neurons,neurons,neurons];
layers = [1,2,3];
s_cluster = sortrows(cluster, [2,3,4,1]);

slowest  = 0;
k = 1;
times_c_x = zeros(1,54);

for j = 1:length(s_cluster)
   if s_cluster(j,4) == neurons(k)
       slowest = max(slowest,s_cluster(j,6));
   else
       times_c_x(k) = slowest;
       slowest = 0;
       k = k + 1;
       slowest = max(slowest,s_cluster(j,6));
   end
end
times_c_x(k) = slowest;

times_d = desktop(:,6)';
ttime_c = sum(times_c_x);
ttime_d = sum(times_d);
adding = zeros(1,13);

for m = 2:14
    temp = zeros(1,m);
    for n = 1:54
        temp(rem(n,m)+1) = temp(rem(n,m)+1) + times_c_x(n);
    end
    adding(m-1) = max(temp);
end

plot_data = [ttime_c,adding];

figure(7);
plot(1./plot_data,'k','linewidth',2);
hold on;
grid minor;
plot(14, 1/ttime_d,'*k','linewidth',2);
xlim([0.5 14.5]);
set(gca,'Xtick',1:1:14);
set(gca,'XtickLabel',1:1:14);
set(gca,'fontweight','bold');
xlabel('RPi3 Platforms');
ylabel('Inverse Time (1/seconds)');
title('RPi3 Max Time vs Desktop - HP Sweep');
legend('RPi3','Desktop','location','northwest');
saveas(gcf,'HP_Sweep_Max.png')