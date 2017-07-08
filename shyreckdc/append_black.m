function new_data = append_black(data)
	load black_mostly.txt;
	choose_matrix = zeros(size(black)*2, 1); 
	for i = 1:size(black)
		choose_matrix(2*i-1) = black(i)*2-1;
		choose_matrix(2*i) = black(i)*2;
	end
	all_test = dlmread('dsjtzs_txfz_test1.txt');
	black = all_test(choose_matrix,:);
	size(black, 2)
	size(data, 2)
	new_data = [data; black];
end		
