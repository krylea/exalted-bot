import numpy as np

DEFAULT_VALS = np.array([0,0,0,0,0,0,0,1,1,1,2])


class Session(object):
    def __init__(self):
        self.die_size = 10
        self.target = 7
        self.default_values = DEFAULT_VALS

    def is_command(self, query):
        return query[:2] == "/r"

    def parse_roll(self, query):
        commands = [cmd for cmd in query.split(" ") if cmd is not ""]

        n = int(commands[0])

        values = self.default_values.copy()
        d = self.die_size
        t = self.target
        ro = []
        ra = []
        ex = []
        rn = 0

        for cmd in commands[1:]:
            prefix, suffix = parse_command(cmd)
            if prefix is None or suffix is None:
                raise NotImplementedError
            if prefix == 't':
                t = suffix
            elif prefix == '+':
                values[suffix] += 1
            elif prefix == '-':
                values[suffix] -= 1
            elif prefix == '!':
                ex.append(suffix)
            elif prefix == 'ro':
                ro.append(suffix)
            elif prefix == 'ra':
                ra.append(suffix)
            elif prefix == 'rn':
                rn = suffix
            elif prefix == 'd':
                d = suffix

        return n, values, ro, ra, ex, rn, d, t

    def execute_command(self, query):
        n, values, ro, ra, ex, rn, d, t = self.parse_roll(query)
        adjust_target(values, t)
        buckets, successes = roll(n, values, rn, ro, ra, ex, d)
        dice = buckets_to_dice(buckets)
        output = self.format_output(n, dice, successes)
        return output

    def format_output(self, n, dice, successes):
        str_dice = [str(x) for x in dice]
        dice_out = ",".join(str_dice)
        output = "Rolling %d dice...\nResults: " % (n) + dice_out + "\n%d successes total." % (successes)
        return output


def roll(n, values=DEFAULT_VALS, reroll_n=0, reroll_one=[], reroll_all=[], explode=[], d=10):
    buckets = roll_once(n, d)

    if len(reroll_one) > 0:
        reroll_number(buckets, reroll_one, d)

    if reroll_n > 0:
        target = (values != 0).argmax()
        reroll_fail(buckets ,reroll_n, d, target)

    if len(reroll_all) > 0:
        done=False
        while not done:
            reroll_number(buckets, reroll_all, d)
            done = True
            for x in reroll_all:
                if buckets[x] > 0:
                    done=False

    if len(explode) > 0:
        n_ex = 0
        for x in explode:
            n_ex += buckets[x]
        buckets += roll_once(n_ex, d)

    successes = buckets.dot(values)
    return buckets, successes


#
#   Rolling utilities
#

def roll_once(n, d):
    rolls = np.random.randint(1, d+1, size=(n))
    return np.bincount(rolls, minlength=d+1)


def reroll_number(buckets, nums, d):
    n = 0
    for x in nums:
        n += buckets[x]
        buckets[x] = 0

    buckets += roll_once(n, d)


def reroll_fail(buckets, n, d, target):
    n_left = n
    count=1
    while n_left > 0:
        m = min(n_left, buckets[count])
        n_left -= m
        buckets[count] -= m

        count += 1
        if count >= target:
            break

    x = n - n_left
    buckets += roll_once(x, d)

def buckets_to_dice(buckets):
    tot = np.sum(buckets)
    dice = np.zeros(tot,dtype=np.int)
    n=0
    k=len(buckets)-1
    for i in range(k):
        b = buckets[k-i]
        dice[n:n+b] = k-i
        n += b
    return dice

#
#   Parsing utilities
#

ROLL_PREFIXES=['+','-','!','ro','ra','rn','d','t']
CONFIG_PREFIXES = ['d', 't', ]

def parse_command(command, prefix_tokens=ROLL_PREFIXES):
    #n = len(command)
    prefix=""
    for p in prefix_tokens:
        n = len(p)
        if command[:n] == p:
            prefix = p
            break
    n = len(prefix)
    suffix = command[n:]

    valid_suffix = str.isdigit(suffix)
    if n <= 0 or not valid_suffix:
        return None, None
    else:
        return prefix, int(suffix)


def adjust_target(values, target):
    for v in values[target:]:
        if v < 1:
            v = 1



