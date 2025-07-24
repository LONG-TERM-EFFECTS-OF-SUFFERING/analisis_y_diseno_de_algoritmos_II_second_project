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
%                           PRECOMPUTED CONSTANTS                              %
% ---------------------------------------------------------------------------- %

% Precompute movement distance
array[1..m, 1..m] of int: d = array2d(1..m, 1..m, [ abs(i - j) | i in 1..m, j in 1..m ]);

% ---------------------------------------------------------------------------- %
%                                   VARIABLES                                  %
% ---------------------------------------------------------------------------- %

% Number of people moved from i to j
array[1..m, 1..m] of var 0..max(p): s :: add_to_output;

% Total movement-distance (|j - i| * s[i, j])
var int: total_moves;

% Total cost of all movements
var float: total_cost :: add_to_output;

% Aggregate extremism after movements
var float: extremism :: add_to_output;

% ---------------------------------------------------------------------------- %
%                                  CONSTRAINTS                                 %
% ---------------------------------------------------------------------------- %

% Flow conservation: everyone must be moved or stay
constraint forall(i in 1..m)(
	sum(j in 1..m)( s[i, j] ) = p[i]
);

% Bound each flow for tighter propagation
constraint forall(i, j in 1..m)(
	s[i, j] <= p[i]
);

% Limit total movement-distance
constraint total_moves = sum(i, j in 1..m)( d[i, j] * s[i, j] );
constraint total_moves <= M;

% Total cost including extra cost when destination is empty
constraint total_cost =
	sum(i, j in 1..m)(
		( c[i, j] * (1.0 + p[i] / n)
			+ ( if p[j] == 0 then ce[j] else 0.0 endif )
		) * s[i, j]
	);
constraint total_cost <= ct;

% ---------------------------------------------------------------------------- %
%                                TARGET FUNCTION                               %
% ---------------------------------------------------------------------------- %

constraint extremism = sum(i, j in 1..m)( s[i, j] * e[j] );
solve minimize extremism;

% ---------------------------------------------------------------------------- %
%                                    OUTPUT                                    %
% ---------------------------------------------------------------------------- %

array[1..m] of var 0..n: p_prime :: add_to_output;
constraint p_prime = [ sum(i in 1..m)( s[i, j] ) | j in 1..m ];
