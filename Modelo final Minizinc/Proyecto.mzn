% The topics to generate pages
enum Topics;
% Min of pages per topic
array[Topics] of int: minPages;
% Max of pages per topic
array[Topics] of int: maxPages;
% Potencial readers for a page per topic
array[Topics] of int: potentialReaders;
int: limitTotalPages;

% Variables: Number of pages printed per topic
array[Topics] of var int: pages;

% Pages should be >= minPages[t] or don't printed at all
constraint forall (t in Topics) (     
      pages[t] >= minPages[t] \/ pages[t] == 0
);  
% Pages should be <= maxPages[t] 
constraint forall (t in Topics) (     
      pages[t] <= maxPages[t]
);  
constraint sum(t in Topics) (   pages[t] ) == limitTotalPages;  

solve maximize sum (t in Topics) (potentialReaders[t]*pages[t]);

