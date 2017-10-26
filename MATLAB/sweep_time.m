%% Hyper Sweep Time Plot

%% prepare workspace
close all;
clear;
clc;

% Load data
load('sweep_time.mat')

% plot data
figure(1);
semilogy(D_time(1:14),'-r');
hold on;
semilogy(D_time(15:28),'--r');
semilogy(D_time(29:42),':r');
semilogy(R_time(1:14),'-b');
semilogy(R_time(15:28),'--b');
semilogy(R_time(29:42),':b');
xlim([1 14]);
grid minor;
xlabel('Combination Number');
ylabel('Time Taken');
title('Hyper Parameter Sweep');
legend('Desktop-1 Layer','Desktop-2 Layers','Desktop-3 Layers',...
    'RPi-1 Layer','RPi-2Layers','RPi-3Layers',...
    'location','northwest');
    