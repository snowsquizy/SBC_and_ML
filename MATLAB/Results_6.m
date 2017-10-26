%% ZEIT4500 Results Loading and Plotting
% SBLT Andrew Taylor - z3457431
%% TicTacToe Desktop

%% Prepare Workspace
close all;
clear;
clc

%% Global Variables
workers = 1;
test_runs = 6;
min_t = zeros(1,test_runs);
max_t = zeros(1,test_runs);
mean_t = zeros(1,length(workers));
sd = zeros(1,length(workers));
se = zeros(1,length(workers));

%% Loading Data in
load('6total_results.mat');

%% Split Data into worker Runs using average total run time
for j = 1:1:1
    time_t = total(1:test_runs*workers(j));
    total = total(test_runs*workers(j)+1:end);
    mean_t(j) = mean(time_t);
    sd(j) = std(time_t);
    se(j) = sd(j)/sqrt(6);
end
mean_t = fliplr(mean_t);
figure(6);
p2 = errorbar(mean_t,se,'k','linewidth',2);
xlabel('Test Run');
ylabel('Time (s)');
grid;
% xlim([0.5 13.5])
title('Desktop - 1 ps & 1 worker -- MNIST');
% set(gca, 'Xtick',1:1:13)
% set(gca,'XtickLabel',1:1:13)
%yyaxis right;
%p3 = plot([1 1 1 1 1 1 1 1 1 1 1 1 1],'b');
%p4 = plot([13 12 11 10 9 8 7 6 5 4 3 2 1],'-.r');
%ylabel('Parameter Servers');
%legend('Single Parameter Server','Multiple Parameter Servers',...
%    'Parameter Servers Fixed','Parameter Servers Increasing','location','northeast');