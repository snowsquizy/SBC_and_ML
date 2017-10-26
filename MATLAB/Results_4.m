%% ZEIT4500 Results Loading and Plotting
% SBLT Andrew Taylor - z3457431
%% TicTacToe Raspberry Pi Cluster

%% Prepare Workspace
close all;
clear;
clc

%% Global Variables
workers = linspace(13,1,13);
test_runs = 6;
min_t = zeros(1,test_runs);
max_t = zeros(1,test_runs);
mean_t = zeros(1,length(workers));
sd = zeros(1,length(workers));
se = zeros(1,length(workers));

%% Loading Data in
load('4total_results.mat');

%% Split Data into worker Runs using average total run time
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
plot([1 13],[1/4.29 1/4.29],'--r','linewidth',2);
plot([1 13],[1/3.39 1/3.39],'-.g','linewidth',2);
plot(1./per_par,':k','linewidth',2);
legend('RPi3','Desktop','K40','Perfect Parallel','location','west');
xlabel('Workers (N)');
ylabel('Inverse Time (1/sec)');
grid on;
xlim([0.5 13.5]);
title({'Rpi3 vs Desktop vs K40'});
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');

subplot(121);
plot(mean_t,'b','linewidth',2);
hold on;
plot([1 13],[4.29 4.29],'--r','linewidth',2);
plot([1 13],[3.39 3.39],'-.g','linewidth',2);
plot(per_par,':k','linewidth',2);
xlabel('Workers (N)');
ylabel('Time (sec)');
grid on;
xlim([0.5 13.5]);
title('RPi3 vs Desktop vs K40');
legend('RPi3','Desktop','K40','Perfect Parallel','location','north');
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');

