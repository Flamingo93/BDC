function [vel, x_vel, y_vel, time_diff, x_diff, y_diff, theta] = compute_velocity(line)
difference = [];
for i = 1:size(line, 2) - 3
	difference = [difference line(:, 3+i)-line(:, i)];
end
x_diff = difference(:, 1:3:end);
y_diff = difference(:, 2:3:end);
theta = atan(y_diff./x_diff);
time_diff = difference(:, 3:3:end);
time_diff(time_diff == 0) = 20;
time_flag = time_diff < 0;

x_vel = x_diff./time_diff;
y_vel = y_diff./time_diff;
vel = sqrt(x_vel.^2 + y_vel.^2);

end

	
