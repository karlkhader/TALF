function developlsystem(lsystem, iterations)
## Examples:
##   developlsystem('creeping_plant', 2);
##   developlsystem('climbing_plant', 3);
##
## Read more about L-Systems in
##  https://riuma.uma.es/xmlui/bitstream/handle/10630/12647/paper%20GECCO09.pdf
##
## ===============================================================
##
##   fjv, 20/10/2019
##
## ===============================================================

  ## reach for json utilities
  addpath('../');

  if ischar(lsystem)
    ## read from JSON file (FastArrayParser = 0 avoids replacing '[' by '{')
    lsystem = loadrepresentation('grammars', lsystem);
  end

  ## starting string
  string = lsystem.S;

  ## iterations (choose only from 1 to 7, >= 8 critical,
  ## depends on the string and on the computer !!
  if !exist('iterations', 'var')
    iterations = 3;
  end

  ## rewrite axiom a number of times
  for iditeration = 1 : iterations
    ## start from current string
    ## non-terminal capital letters to small letters
    production = tolower(string);
    ## rewrite each small letter with the RHS of the corresponding rule
    for idN = 1 : numel(lsystem.N)
      symbol = lsystem.P{idN}{1};
      production = strrep(production, tolower(symbol), lsystem.P{idN}{2});
    end
    string = production;
  end

  ## draw resulting structure with turtle method
  drawtree(string);

end
