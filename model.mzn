% ---------------------------------------------------------------------------- %
%                                  INPUT DATA                                  %
% ---------------------------------------------------------------------------- %
int: n; % Total amount of people
int: m; % Total amount of opinions
array[1..m] of int: p; % Vector with the distribution of people per opinion
array[1..m] of float: e; % Vector with the values of extremism of the opinions
array[1..m, 1..m] of float: c; % Cost matrix
array[1..m] of float: ce; % Extra cost matrix
float: ct; % Total allowed cost
int: M; % Maximum number of moves allowed

% ---------------------------------------------------------------------------- %
%                                   VARIABLES                                  %
% ---------------------------------------------------------------------------- %

array[1..m, 1..m] of var 0..n: s :: add_to_output; % s_(ij) people moved from i to j
array[1..m] of var 0..n: p_prime :: add_to_output; % Vector with the distribution of people after applying the movements
                                                   % of s

% ---------------------------------------------------------------------------- %
%                                  CONSTRAINTS                                 %
% ---------------------------------------------------------------------------- %

% ----------------------------- FLOW CONSERVATION ---------------------------- %

constraint forall(i in 1..m) (
	sum(j in 1..m) (s[i, j]) = p[i]
);

% ---------------------------- P_PRIME CALCULATION --------------------------- %

constraint forall(j in 1..m) (
	p_prime[j] = sum(i in 1..m) (s[i, j]) % Arriving people (that includes s[j, j])
);

% ---------------------------- NUMBER OF MOVEMENTS --------------------------- %

constraint sum(i in 1..m, j in 1..m) (abs(j - i) * s[i, j]) <= M;

% -------------------------------- TOTAL COST -------------------------------- %

var float: total_cost :: add_to_output;
constraint total_cost == sum(i,j in 1..m)(
	c[i,j] * (1.0 + p[i]/n) * s[i,j] +
	(if p[j]==0 then ce[j] * s[i,j] else 0.0 endif)
);
constraint total_cost <= ct;

% ---------------------------------------------------------------------------- %
%                                TARGET FUNCTION                               %
% ---------------------------------------------------------------------------- %

var float: extremism :: add_to_output;
extremism = sum(i in 1..m) (
	p_prime[i] * e[i]
);

solve minimize extremism;
