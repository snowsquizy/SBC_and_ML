%% ZEIT4500 Results Loading and Plotting
% SBLT Andrew Taylor - z3457431
%% MNIST Raspberry Pi Cluster

%% Prepare Workspace
close all;
clear;
clc

%% Global Variables
workers = linspace(13,1,13);
test_runs = 6;
mean_t = zeros(1,length(workers));
sd = zeros(1,length(workers));
se = zeros(1,length(workers));

%% Loading Data in
load('2total_results.mat');

%% Split Data into worker Runs
for j = 1:1:13
    time_t = total(1:test_runs*workers(j));
    total = total(test_runs*workers(j)+1:end);
    mean_t(j) = mean(time_t);
    sd(j) = std(time_t);
    se(j) = sd(j)/sqrt(6);
end
mean_t = fliplr(mean_t);
per_par = zeros(1,13);
for g = 1:13
    per_par(g) = mean_t(1)/g;
end

figure(1);
subplot(122);
plot(1./mean_t,'b','linewidth',2);
hold on;
plot([1 13],[1/12.02 1/12.02],'--r','linewidth',2);
plot([1 13],[1/2.54 1/2.54],'-.g','linewidth',2);
plot(1./per_par,':k','linewidth',2);
xlabel('Workers (N)');
ylabel('Inverse Time (1/sec)');
grid;
xlim([0.5 13.5]);
title({'RPi3 vs Desktop vs K40'});
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');
legend('RPi3','Desktop','K40','Perfect Parallel Performance',...
    'location','northeast');
subplot(121);
plot(mean_t,'b','linewidth',2);
hold on;
plot([1 13],[12.02 12.02],'--r','linewidth',2);
plot([1 13],[2.54 2.54],'-.g','linewidth',2);
plot(per_par,':k','linewidth',2);
xlabel('Workers (N)');
ylabel('Time (sec)');
grid;
xlim([0.5 13.5]);
title({'RPi3 vs Desktop vs K40'});
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');
legend('RPi3','Desktop','K40','Perfect Parallel Performance',...
    'location','northeast');