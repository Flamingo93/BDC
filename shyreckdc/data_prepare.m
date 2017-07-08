function [line_number, line, target, label] = data_prepare(file)

data = dlmread(file);

%load training_with_black_and_white.txt;
%load training_with_black.txt;
%data = append_white(data);
%save training_with_black_and_white.txt data;


number_of_samples = size(data, 1)/2;
random_sequence = randperm(number_of_samples);
data_combined = [data(1:2:end, :) data(2:2:end, 1:3)];
data_combined = data_combined(random_sequence, :);
data_length = size(data_combined, 2);

line_number = data_combined(:, 1);
line = data_combined(:, 2:data_length-3);
line(line==0) = NaN;
target = data_combined(:, data_length-2:data_length-1);
label = data_combined(:, data_length);

end
