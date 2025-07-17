# Minimizing the extremism present in a population

## Input

- $n \in \mathbb{ N }$: the total amount of people.

- $m \in \mathbb{ N }$: the total amount of opinions.

- $p$: the vector with the distribution of people per opinion, where $p_i$ is the number of people who initially have the opinion $i \in 1\dots m$.

- $e$: the vector with the values of extremism of the opinions, where $e_i \in [0,1]$ is the extremism value of the opinion $i \in 1\dots m$.

- $c$: the cost matrix, where $c_{ i,j } \in \mathbb{ R }^+$ is the cost of moving a person from opinion $i$ to opinion $j$ $i,j \in 1\dots m$.

	> $c_{ i,i } = 0$.

- $ce$: the extra cost matrix, where ${ ce }_i \in \mathbb{ R }^+$ is the extra cost of moving a person to opinion $i$ if that opinion was initially empty $i \in 1\dots m$.

- $ct \in \mathbb{ R }^+$: the total allowed cost.

- $M \in \mathbb{ R }^+$: the maximum number of moves allowed.

## Metrics

- Movement: moving a person from opinion $i$ to opinion $j$ will count as $|j - i|$ movements, so the movement value of a movement of $x$ people from opinion $i$ to opinion $j$ is

$$
|j - i| * x
$$

- Cost of the movement: the cost of a movement of $x$ people from opinion $i$ to opinion $j$ is

$$
\begin{align}
	c_{ i,j } \left ( 1 + \frac{ p_i }{ n } \right ) * x \quad p_j > 0 \\
	c_{ i,j } \left ( 1 + \frac{ p_i }{ n } \right ) * x + { ce }_j * x \quad p_j = 0 \\
\end{align}
$$
