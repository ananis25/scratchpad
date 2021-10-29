// Forth code for a 2d snake game
// following this tutorial - https://skilldrick.github.io/easyforth/

: convert-x-y ( x y -- offset ) 24 * + ;
: draw ( color x y -- ) convert-x-y graphics + ! ;
: draw-white ( x y -- ) 1 rot rot draw ;
: draw-black ( x y -- ) 0 rot rot draw ;

variable snake-x-head
500 allot
variable snake-y-head
500 allot

variable apple-x
variable apple-y

0 constant left
1 constant up
2 constant right
3 constant down

24 constant width 
24 constant height 

variable direction 
variable length

: snake-x ( offset -- addr ) snake-x-head + ;
: snake-y ( offset -- addr ) snake-y-head + ;

: draw-walls
  width 0 do
    i 0 draw-black
    i height 1 - draw-black
  loop
  height 0 do
  	0 i draw-black
  	width 1 - i draw-black
  loop ;

: set-apple-position ( x y -- ) apple-x ! apple-y ! ;
: initialize-apple 4 4 set-apple-position ;

: initialize-snake
  4 length !
  length @ 1 + 0 do 
    12 i - i snake-x !
    12 i snake-y !
  loop 
  right direction ! ;
  
: move-up -1 snake-y-head +! ;
: move-left -1 snake-x-head +! ;
: move-down 1 snake-y-head +! ;
: move-right 1 snake-x-head +! ;

: move-snake-head direction @
  dup left = if move-left else 
  dup right = if move-right else 
  dup down = if move-down else 
  dup up = if move-up 
  then then then then drop ;
  
: move-snake-tail 0 length @ do
  i snake-x @ i 1 + snake-x ! 
  i snake-y @ i 1 + snake-y !
-1 +loop ;

: is-horizontal direction @ dup 
  left = swap 
  right = or ;
  
: is-vertical direction @ dup 
  up = swap 
  down = or ;

: turn-up is-horizontal if up direction ! then ;
: turn-down is-horizontal if down direction ! then ;
: turn-left is-vertical if left direction ! then ;
: turn-right is-vertical if right direction ! then ;

: change-direction ( key -- )
  dup 37 = if turn-left else 
  dup 38 = if turn-up else
  dup 39 = if turn-right else 
  dup 40 = if turn-down 
  then then then then drop ;
  
: check-input 
  last-key @ change-direction
  0 last-key ! ;
  
: random-position ( -- pos )
  width 4 - random 2 + ;
  
: move-apple 
  apple-x @ apple-y @ draw-white
  random-position random-position
  set-apple-position ;
  
: grow-snake 1 length +! ;

: check-apple ( -- flag )
  snake-x-head @ apple-x @ = 
  snake-y-head @ apple-y @ =
  and if 
    move-apple
    grow-snake
  then ;
  
: check-collision ( -- flag )
  snake-x-head @ snake-y-head @ 
  convert-x-y graphics + @ 
  0 = ;
  
: draw-apple 
  apple-x @ apple-y @ draw-black ;
  
: draw-snake 
  length @ 0 do 
    i snake-x @ i snake-y @ draw-black
  loop
  length @ snake-x @ length @ snake-y @ draw-white ;
  
: clearall
  width 0 do
    height 0 do
      j i draw-white
    loop
  loop ;

: initialize
  clearall
  draw-walls 
  initialize-apple
  initialize-snake ;
  
: game-loop ( -- ) 
  begin
    draw-apple 
    draw-snake
    1000 sleep 
    check-input 
    move-snake-tail 
    move-snake-head 
    check-apple 
    check-collision 
  until
  ." Game over!" ;
  
: start initialize game-loop ;
