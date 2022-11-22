%I -> Cantidad de páginas de noticias Internacionales
%N -> Cantidad de páginas de noticias Nacionales
%L -> Cantidad de páginas de noticias Locales
%D -> Cantidad de páginas de noticias de Deportes
%C -> Cantidad de páginas de noticias de Cultura

var int: I; var int: N; var int: L; var int: D; var int: C;

constraint (I >= 5 \/ I == 0) /\ I<= 9 ;
constraint (N >= 4 \/ N == 0) /\ N<= 7;
constraint (L >= 2 \/ L == 0) /\ L<= 5;
constraint (D >= 2 \/ D == 0) /\ D<= 4;
constraint (C >= 1 \/ C == 0) /\ C<= 3 ;
constraint I+N+L+D+C == 10; % Páginas en períodico

solve maximize 1500*I + 2000*N + 1000*L + 1500*D + 750*C;

output ["I=\(I)\t N=\(N)\t L=\(L)\t D=\(D)\t C=\(C)\n"];