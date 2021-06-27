import random


class WinOrLoseError(Exception):
    pass


class Game:

    def __init__(self):

        self.COMMAND_MAP = {
            'w': self.top,
            's': self.down,
            'a': self.left,
            'd': self.right
        }

        self.data = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

    @staticmethod
    def random_one_to_four():
        return random.randint(0, 3)

    def init(self):
        line = self.random_one_to_four()
        col = self.random_one_to_four()
        self.data[line][col] = 2

    def set_value(self):
        zero_position = []
        for row, i in enumerate(self.data):
            for col, j in enumerate(i):
                if j == 0:
                    zero_position.append((row, col))

        if not zero_position:
            self.check()
        row, col = random.choice(zero_position)
        self.data[row][col] = 2

    def is_win(self):
        for i in self.data:
            for j in i:
                if j >= 2048:
                    raise WinOrLoseError('你赢了')

    def is_lose(self):
        try:
            for _, method in self.COMMAND_MAP.items():
                method(check=True)
        except WinOrLoseError:
            return
        raise WinOrLoseError('你输了')

    @staticmethod
    def _merge_row(row, reverse=True, check=False):
        if not reverse:
            row.reverse()
        first_point = 0
        second_point = 1
        changed = False
        hsa_value = False
        while second_point < len(row):
            if row[first_point] != 0 and row[second_point] == row[first_point]:
                if check:
                    raise WinOrLoseError()
                row[first_point] = row[first_point] * 2
                row[second_point] = 0
                changed = True
                hsa_value = True

            if row[first_point] == 0 and row[second_point] != 0:
                if check:
                    raise WinOrLoseError()
                changed = True
                row[first_point], row[second_point] = row[second_point], row[first_point]

                if first_point != 0 and not hsa_value:
                    first_point -= 1
                    second_point -= 1
                    continue

            first_point += 1
            second_point += 1
        if not reverse:
            row.reverse()
        return changed

    def left(self, check=False):
        self._left_or_right(left=True, check=check)

    def right(self, check=False):
        self._left_or_right(left=False, check=check)

    def _left_or_right(self, left=True, check=False):
        changed = False
        for row in self.data:
            _changed = self._merge_row(row, reverse=left, check=check)
            changed = changed or _changed
        if changed:
            self.set_value()

    def top(self, check=False):
        self._down_or_top(top=True, check=check)

    def _down_or_top(self, top=True, check=False):
        changed = False
        for data_index in range(4):
            row = []
            for i in self.data:
                row.append(i[data_index])
            _changed = self._merge_row(row, reverse=top, check=check)
            if _changed:
                for row_index, i in enumerate(row):
                    self.data[row_index][data_index] = i

            changed = changed or _changed
        if changed:
            self.set_value()

    def down(self, check=False):
        self._down_or_top(top=False, check=check)

    def start(self):
        self.init()
        while True:
            try:
                self.show_data()
                command = input()
                self.run(command)
                self.check()
            except WinOrLoseError as e:
                print(e)
                break

    def check(self):
        self.is_lose()
        self.is_win()

    def run(self, command):
        method = self.COMMAND_MAP.get(command)
        if not method:
            return
        else:
            method()

    def show_data(self):
        for i in self.data:
            print(i)


if __name__ == '__main__':
    game = Game()
    game.start()
