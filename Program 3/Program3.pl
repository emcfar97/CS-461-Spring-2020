use_module(library(clpfd)).

write_to_file(File, Text) :-
    open(File, write, Stream),
    write(Stream, Text), nl,
    close(Stream).

solve(Solution) :-
    maplist( init_dom(1..5),
        [[Accounting,  Computer_science,  Engineering,  History, English],% Majors
         [Ford, Chevy, Nissan, Toyota, Tesla],     % Cars
         [Royals, Chiefs, Yankees, Broncos, Cubs], % Sports
         [Classical, Country, Jazz, Rock, Techno], % Music
         [Coke, Coffee, Tea, Milk, Water]]),       % Drinks

    Computer_science #= 3,               % Hint 1
    History #= Jazz,                     % Hint 2
    Yankees #= Toyota,                   % Hint 3
    Accounting #= Coke - 1 ,             % Hint 4
    Engineering #= Coffee,               % Hint 5
    neighbor(Computer_science, History), % Hint 6
    Classical #= 5,                      % Hint 7
    Tea #= Tesla,                        % Hint 8
    neighbor(Classical, Jazz),           % Hint 9
    English in 3..5,                  % Hint 10
    Royals #= Tesla,                     % Hint 11
    Cubs #= Jazz,                        % Hint 12
    Engineering #= Chiefs,               % Hint 13
    Broncos #= 1,                        % Hint 14
    Coke #= Nissan,                      % Hint 15
    neighbor(Country, Techno),           % Hint 16
    Accounting #= 1,                     % Hint 17
    neighbor(Chiefs, Royals),            % Hint 18
    Accounting #= Rock,                  % Hint 19
    Yankees #= Milk,                     % Hint 20
    Chevy #= Country,                    % Hint 21
    Jazz #= Ford,                        % Hint 22

    memberchk(Solution-Solution[
        Accounting-accounting, Computer_science-computer_science, Engineering-engineering, History-history, English-english
        ]).

init_dom(R, L) :-
    all_distinct(L),
    L ins R.

neighbor(X, Y) :-
    (X #= (Y - 1)) #\/ (X #= (Y + 1)).

