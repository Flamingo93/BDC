clear all;
clc;

load feature_matrix28.txt;
data = ans;
X_test = data(:, [2:size(data,2)-1]);

%load('theta_black.txt');
load('theta_black_and_white.txt');
[p, p_raw] = predict(theta, X_test);
sum(p_raw<0.5)
line_number = data(:, 1);
submit_numbers = line_number(p_raw < 0.5);
%submit = [line_number p_raw];
%submit_sorted = sortrows(submit, 2);
%submit_numbers = submit_sorted(1:20000, 1);
submit_numbers = sort(submit_numbers);
fid = fopen('BDC0664_20170708.txt', 'wt');
fprintf(fid,'%g\n', submit_numbers);
fclose(fid);
