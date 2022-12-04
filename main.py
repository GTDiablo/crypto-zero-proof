from math import sqrt
from typing import List
from random import randint

# https://medium.com/asecuritysite-when-bob-met-alice/feige-fiat-shamir-and-zero-knowledge-proof-cdd2a972237c


def gcd(p, q) -> int:
    # Create the gcd of two positive integers.
    while q != 0:
        p, q = q, p % q
    return p


def is_coprime(x, y) -> bool:
    return gcd(x, y) == 1


def is_prime(n) -> bool:
    prime_flag = 0

    if (n > 1):
        for i in range(2, int(sqrt(n)) + 1):
            if (n % i == 0):
                prime_flag = 1
                break
        if (prime_flag == 0):
            return True
        else:
            return False
    else:
        return False


def product(n: List[int]) -> int:
    res = 1

    for x in n:
        res *= x

    return res


class Verifier:
    """"""
    CHALLENGE_SIZE = 10

    def __init__(self, n: int) -> None:
        self.n = n
        self.challenges = self._generate_challenges()

    def _generate_challenges(self) -> List[int]:
        return [randint(0, 1) for _ in range(Verifier.CHALLENGE_SIZE)]
        # return [1, 0, 1]

    def send_x(self, x: int) -> None:
        self.x = x

    def send_y1(self, y1: int) -> None:
        self.y1 = y1

    def calculate_y(self, v: List[int]) -> int:
        pairs = zip(v, self.challenges)
        return (self.x * product([pow(pair[0], pair[1]) for pair in pairs])) % self.n


class Prover:
    """"""
    SECRET_SIZE = 10

    def __init__(self, n: int) -> None:
        self.n = n
        self.secrets: List[int] = self._gen_secrets()
        self.r = 13  # randint(0, 10_000_000)
        self.x = (self.r ** 2) % n
        self.v = self._calculate_v()

    def _gen_secrets(self) -> List[int]:
        # return [5, 7, 3]
        res = []
        while len(res) != Prover.SECRET_SIZE:
            last_res = 3 if len(res) == 0 else res[-1]
            for i in range(last_res, 10_000_000):
                if is_prime(i) and is_coprime(self.n, i) and (i not in res):
                    res.append(i)
                    break
        return res

    def calculate_y1(self, challenges: List[int]) -> int:
        pairs = zip(self.secrets, challenges)
        return (self.r * product([pow(pair[0], pair[1]) for pair in pairs])) % self.n

    def _calculate_v(self) -> List[int]:
        return [((s**2) % self.n) for s in self.secrets]


class App:
    def __init__(self, q: int, p: int) -> None:
        assert is_prime(q) == True
        assert is_prime(p) == True
        self.q = q
        self.p = p
        self.n = p*q

        self.proofer = Prover(self.n)
        self.verifier = Verifier(self.n)

    def start_proof(self) -> List[int]:
        self.verifier.send_x(self.proofer.x)
        y1 = self.proofer.calculate_y1(self.verifier.challenges)
        y = self.verifier.calculate_y(self.proofer.v)
        return ((y1**2) % self.n, (y1**2) % self.n)


def main() -> None:
    app = App(101, 23)
    could_proof = app.start_proof()
    print(could_proof)


if __name__ == '__main__':
    main()


# n = 101*23
# r = 13
# s1 = 5
# s2 = 7
# s3 = 3
# a1 = 1
# a2 = 0
# a3 = 1
# print('N=', n)
# x = (r**2) % n
# print('x=', x)
# print('s1=', s1, 's2=', s2, 's3=', s3)
# print('a1=', a1, 'a2=', a2, 'a3=', a3)
# y = (r * ((s1**a1) * (s2**a2) * (s3**a3))) % n
# print('Y=', y, ' y^2 mod n = ', (y**2 % n))
# v1 = (s1**2) % n
# v2 = (s2**2) % n
# v3 = (s3**2) % n
# y2 = (x * ((v1**a1) * (v2**a2) * (v3**a3))) % n
# print('Y=', (y**2) % n)
