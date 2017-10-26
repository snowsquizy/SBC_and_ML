%% ZEIT4500 Results Loading and Plotting
% SBLT Andrew Taylor - z3457431
%% TicTacToe Raspberry Pi Cluster

%% Prepare Workspace
close all;
clear;
clc

%% Loading Data in
load('10by10_results.mat');

mean_d = mean(time_d);
mean_k = mean(time_k);
per_par = zeros(1,13);
for g = 1:13
    per_par(g) = mean_r(1)/g;
end


figure(1);
subplot(121);
plot(mean_r,'b','linewidth',2);
hold on;
plot([1 13],[mean_d mean_d],'--r','linewidth',2);
plot([1 13],[mean_k mean_k],'-.g','linewidth',2);
plot(per_par,':k','linewidth',2);
xlabel('Workers (N)');
ylabel('Time (sec)');
grid on;
xlim([0.5 13.5]);
title({'RPi3 vs Desktop vs K40'});
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');
legend('RPi3','Desktop','K40','Perfect Parallel Performance',...
    'location','east');

subplot(122);
plot(1./mean_r,'b','linewidth',2);
hold on;
plot([1 13],[1./mean_d 1./mean_d],'--r','linewidth',2);
plot([1 13],[1./mean_k 1./mean_k],'-.g','linewidth',2);
plot(1./per_par,':k','linewidth',2);
xlabel('Workers (N)');
ylabel('Inverse Time (1/sec)');
grid on;
xlim([0.5 13.5]);
title({'RPi3 vs Desktop vs K40'});
set(gca,'Xtick',1:1:13);
set(gca,'XtickLabel',1:1:13);
set(gca,'fontweight','bold');
legend('RPi3','Desktop','K40','Perfect Parallel Performance',...
    'location','northwest');