function feature_matrix = feature_matrix(file)
[line_number, line, target, label] = data_prepare(file);
[vel, x_vel, y_vel, time_diff, x_diff, y_diff, theta] = compute_velocity(line);
stay_time = sum(vel==0, 2);
move_time = sum(vel>0, 2);
stay_percetage = stay_time./(stay_time + move_time);
max_vel = max(vel, [], 2);
vel_withoutnan = vel;
vel_withoutnan(isnan(vel_withoutnan)) = 0;
line_length = sum(vel>-100, 2);
average_vel = sum(abs(vel_withoutnan), 2)./line_length;

whole_time = sum(time_diff, 2);
max_time_diff = max(time_diff, [], 2);
min_time_diff = min(time_diff, [], 2);
max_x_diff = max(x_diff, [], 2);
max_y_diff = max(y_diff, [], 2);
min_x_diff = min(x_diff, [], 2);
min_y_diff = min(y_diff, [], 2);

vel_neg = sum(vel < 0, 2);
vel_pos = sum(vel >=0, 2);
vel_neg_percetage = vel_neg./(vel_neg + vel_pos);

start_x = line(:, 1);
start_y = line(:, 2);
middle_vel = [];
end_x = [];
end_y = [];
end_vel = [];
end3_vel = [];
%line_choose_matrix = zeros(size(line));
%vel_choose_matrix = zeros(size(vel));
%
%line_length1 = line_length*3 + 1;
%line_length2 = line_length*3 + 2;
%line_length_round = round(line_length/2);
%line_length_minus = line_length - 2;
for i = 1:size(label)
%	line_choose_matrix(i, line_length1(i)) = 1;
%	line_choose_matrix(i, line_length2(i)) = 1;
	end_x = [end_x; line(i, line_length(i)*3 + 1)];
	end_y = [end_y; line(i, line_length(i)*3 + 2)];
	middle_vel = [middle_vel; vel(i, max(1, round(line_length(i)/2)))];
	end_vel = [end_vel; vel(i, max(1, line_length(i)))];
	end3_vel = [end3_vel; vel(i, max(1, line_length(i) - 2))];
end
%for i = 1:size(label)
%	vel_choose_matrix(i, line_length_round(i)) = 1;	
%	vel_choose_matrix(i, line_length(i)) = 1;	
%	vel_choose_matrix(i, line_length_minus(i)) = 1;	
%end
%	line_choose_matrix > 0;
%	vel_choose_matrix > 0;
%	line_choose = line'(line_choose_matrix');
%	end_x = line_choose(1:2:end);
%	end_y = line_choose(2:2:end);
%	vel_choose = vel'(vel_choose_matrix');
%	middle_vel = vel_choose(1:3:end);
%	end3_vel = vel_choose(2:3:end);
%	end_vel = vel_choose(3:3:end);

	end_distance = abs(end_x - target(:, 1));
%end_distance = [];
start_vel = vel(:, 1);
start3_vel = vel(:, 3);

theta_delta = theta(:, 2:end) - theta(:, 1:end-1);
max_theta_delta = max(theta_delta, [], 2);
theta_delta_pos = sum(theta_delta > 0, 2);
theta_delta_neg = sum(theta_delta <= 0, 2);
theta_delta(isnan(theta_delta)) = 0;
theta_delta = theta_delta.^2;
theta_delta_sum = sum(theta_delta, 2);

theta_start_to_end = atan((end_y - start_y)./(end_x - start_x));
theta_compare = theta - theta_start_to_end;
theta_compare_pos = sum(theta_compare > 0, 2);
theta_compare_neg = sum(theta_compare <= 0, 2);
theta_compare(isnan(theta_compare)) = 0;
theta_compare = theta_compare.^2;
theta_compare_sum = sum(theta_compare, 2);

accerate_x = (x_vel(:, 2:end) - x_vel(:, 1:end-1))./time_diff(:, 2:end);
accerate_y = (y_vel(:, 2:end) - y_vel(:, 1:end-1))./time_diff(:, 2:end);
accerate = sqrt(accerate_x.^2 + accerate_y.^2);

middle_acc = [];
end_acc = [];
end3_acc = [];
for i = 1:size(label)
	middle_acc = [middle_acc; accerate(i, max(1, round(line_length(i)/2)))];
	end_acc = [end_acc; accerate(i, max(1, line_length(i) - 1))];
	end3_acc = [end3_acc; accerate(i,max(1, line_length(i) - 3))];
end
start_acc = accerate(:, 1);
start3_acc = accerate(:, 3);
line_length = line_length + 1;



feature_matrix = [line_number stay_percetage max_vel average_vel end_distance start_vel start3_vel middle_vel end_vel end3_vel vel_neg_percetage start_acc start3_acc middle_acc end_acc end3_acc theta_delta_pos theta_delta_neg theta_delta_sum theta_compare_sum line_length whole_time max_time_diff min_time_diff max_x_diff min_x_diff max_y_diff min_y_diff max_theta_delta label];

feature_matrix(isnan(feature_matrix)) = 0;
end

