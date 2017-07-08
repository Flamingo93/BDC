linenumber = input('please input linenumber: ');
data = dlmread('dsjtzs_txfz_training.txt');
line = data(1:2:end, 2:end);
target = data(2:2:end, 1:2);
plot(line(linenumber, 1:3:end),line(linenumber, 2:3:end));
hold on;
plot(target(linenumber, 1),target(linenumber, 2),'r');

