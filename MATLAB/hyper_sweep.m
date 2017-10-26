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
load('sweep_k40.mat');
neurons = [9,18,27,36,45,54,63,72,81];
neurons = [neurons,neurons,neurons,neurons,neurons,neurons];
layers = [1,2,3];
s_cluster = sortrows(cluster, [2,3,4,1]);
fastest = 10000000;
slowest = 0;
k = 1;
p = 1;
c_mins = zeros(1,13);
c_maxs = zeros(1,13);
times_c_m = zeros(1,54);
times_c_x = zeros(1,54);

for j = 1:length(s_cluster)
   if s_cluster(j,4) == neurons(k)
       fastest = min(fastest,s_cluster(j,6));
   else
       times_c_m(k) = fastest;
       fastest = 1000000;
       k = k + 1;
       fastest = min(fastest,s_cluster(j,6));
   end
end
times_c_m(k) = fastest;

for h = 1:length(s_cluster)
   if s_cluster(h,4) == neurons(p)
       slowest = max(slowest,s_cluster(h,6));
   else
       times_c_x(p) = slowest;
       slowest = 0;
       p = p + 1;
       slowest = max(slowest,s_cluster(h,6));
   end
end
times_c_x(k) = slowest;

times_d = desktop(:,6)';
ttime_c_m = sum(times_c_m);
ttime_c_x = sum(times_c_x);
ttime_d = sum(times_d);

for m = 2:14
    temp = zeros(1,m);
    for n = 1:54
        temp(rem(n,m)+1) = temp(rem(n,m)+1) + times_c_m(n);
    end
    c_mins(m-1) = max(temp);
end

for m = 2:14
    temp = zeros(1,m);
    for n = 1:54
        temp(rem(n,m)+1) = temp(rem(n,m)+1) + times_c_x(n);
    end
    c_maxs(m-1) = max(temp);
end

ttime_k = sum(k40);
plot_min = [ttime_c_m,c_mins];
plot_max = [ttime_c_x,c_maxs];
per_par = zeros(1,22);
for g = 1:22
    per_par(g) = plot_min(1)/g;
end

figure(8);
plot(1./plot_min,'b','linewidth',2);
hold all;
plot([1 14],[1/ttime_d 1/ttime_d],'--r','linewidth',2);
plot([1 14],[1/ttime_k 1/ttime_k],'-.g','linewidth',2);
plot(1./per_par(1:14),':k','linewidth',2);
xlim([0.5 14.5]);
grid on;
set(gca,'Xtick',1:1:14);
set(gca,'XtickLabel',1:1:14);
set(gca,'fontweight','bold');
xlabel('Workers (N)');
ylabel('Inverse Time (1/sec)');
title({'RPi3 vs Desktop vs K40'});
legend('RPi3','Desktop','K40','Perfect Parallel Performance','location','west');

%% Cost Comparison
% 6 Raspberry Pi's will beat the Desktop
% 22 Raspberry Pi's will beat the Desktop