%% Hyper Parameter Sweep - 2 Layer
%

%% Prepoare Workspace
close all;
clear;
clc;

% Variables
file_name = '9log_a.dat';
delimiter_inline = ',';
layer_2 = importdata(file_name,delimiter_inline);
clear file_name delimiter_inline;
neurons = [5,10,20,50,100,500,1000,5,10,20,50,100,500,1000];
mv = zeros(1,length(neurons));
sd = zeros(1,length(neurons));
se = zeros(1,length(neurons));
% Sort Data
layer2 = sortrows(layer_2, [2 3 4]);

% Counters
count1 = 1;
count2 = 1;

% Iterate through data
for i = 1:length(layer2)
    if neurons(count1) == layer2(i,4)
        t_sum(count2) = layer2(i,5); 
        count2 = count2 + 1;
    else
        mv(count1) = mean(t_sum);
        sd(count1) = std(t_sum);
        se(count1) = sd(count1)/length(t_sum);
        count1 = count1 + 1;
        count2 = 1; 
        t_sum(count2) = layer2(i,5);
    end
    if i == length(layer2)
        mv(count1) = mean(t_sum);
        sd(count1) = std(t_sum);
        se(count1) = sd(count1)/length(t_sum);
    end
end

% Plot Layer 2 Data

figure(1);
y1 = errorbar(neurons(1:7),mv(1:7),se(1:7),'b');
hold on;
grid minor;
errorbar(neurons(8:end),mv(8:end),se(8:end),'r');
legend('TANH','SIGMOID','location','northeast');
title('Activation vs Neurons - 2 Layer');
set(get(y1,'Parent'), 'XScale', 'log')
xlim([1 2000]);
xlabel('Neurons (N)');
ylabel('Seconds (s)');