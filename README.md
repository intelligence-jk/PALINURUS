# boats-and-streams

Solve boats and streams problems exactly, and see the classic trap where swapping the two speeds gives a wrong answer that still "checks out".

## What it does
Give it the boat's speed in still water, the distance up the stream, the distance down, and the total time. It sets up the quadratic, keeps only the stream speeds that make sense (more than 0 and less than the boat's speed), says why the other root is thrown away, and checks the answer against the story. It also shows the swapped set-up trap with its own numbers, and can draw an ASCII timeline. Pure Python 3.10+, standard library only, exact `Fraction` arithmetic.

## Example
```bash
python -m boats 12 15 18 3 --timeline
```
```
Boat in still water: 12 km/h. Upstream 15 km, downstream 18 km, total 3 h.
Let the stream speed be s km/h.
Upstream the stream pushes against the boat: speed 12 - s.
Downstream the stream helps: speed 12 + s.
Time = distance / speed, so 15/(12 - s) + 18/(12 + s) = 3.
Multiply by (12 - s)(12 + s): 15(12 + s) + 18(12 - s) = 3(12^2 - s^2).
Rearranged: 3 s^2 + (-3) s + (-36) = 0.
Roots: -3, 4.
s = -3 is rejected: a speed cannot be negative or zero here (the stream runs against the boat going up).
Check s = 4: 15/8 + 18/16 = 3 h (matches).

The trap: swap the two speeds (use b + s going up and b - s going down).
That wrong equation also has a clean answer, s = 3, and it checks out in its own wrong equation.
But with s = 3 the real trip takes 43/15 h, not 3 h. Always check against the story, not against your own equation.

|<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>|
 up 15/8 h at 8 km/h  then  down 9/8 h at 16 km/h  = 3 h

Answer: the stream speed is 4 km/h.
```
Fractions work too, for example `python -m boats 7/2 5 6 4`. When no stream speed fits, it says so and exits with code 1.

## The maths behind it
Let b be the boat's speed in still water and s the stream speed, with 0 < s < b. Going up the boat's speed is b - s, going down it is b + s. With d_up and d_down the distances and T the total time:

```
d_up/(b - s) + d_down/(b + s) = T
d_up(b + s) + d_down(b - s) = T(b^2 - s^2)        (multiply by (b - s)(b + s))
T s^2 + (d_up - d_down) s + (d_up + d_down) b - T b^2 = 0
```

For b = 12, 15 km up, 18 km down, 3 h this is 3s^2 - 3s - 36 = 0, so s^2 - s - 12 = 0 and s = 4 or s = -3. A speed cannot be negative, so s = 4. The check: 15/8 + 18/16 = 15/8 + 9/8 = 3 h.

Roots are dropped when s <= 0 (the stream would run the wrong way) or s >= b (the boat could not go upstream). Occasionally two roots both fit (this can happen when the upstream distance is shorter than the downstream one), and then the data alone does not decide; `solve` refuses to guess and `solve_all` returns both.

The trap: use b + s going up and b - s going down. The equation becomes 3s^2 + 3s - 36 = 0, so s = 3, and 15/15 + 18/9 = 3 is true in that wrong equation. But the real trip with s = 3 takes 15/9 + 18/15 = 43/15 h, not 3 h. Always check an answer against the story, not against your own equation.

## Install and run
```bash
python -m pip install -e .
python -m boats 12 15 18 3
python -m pytest
```
In Python: `from boats import solve, wrong_setup, trip_time, explain, timeline`.

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
