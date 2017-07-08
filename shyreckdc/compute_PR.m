function [P, R] = compute_PR(p, y)
	temp = 2*p - y;
	p0y0 = sum(temp == 0)
	p0y1 = sum(temp == -1)
	p1y0 = sum(temp == 2)
	p1y1 = sum(temp == 1)
	P = p0y0 / (p0y0 + p0y1);
	R = p0y0 / (p0y0 + p1y0);
end
