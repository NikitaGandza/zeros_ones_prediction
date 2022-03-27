class UserInputPrediction:
    def __init__(self):
        self.main_string = ""
        self.triads_dict = {"000": [0, 0],
                            "001": [0, 0],
                            "010": [0, 0],
                            "011": [0, 0],
                            "100": [0, 0],
                            "101": [0, 0],
                            "110": [0, 0],
                            "111": [0, 0],
                            }

    def process_user_input(self, user_input):
        """
        Function deletes everything except 1, 0 from the user input. Checks if round is first or not. If first user
        should input 100+ correct character, if not first then 10+ characters. After processing, cleaned string is
        appending to the main string
        :param user_input: first round: user input to create main string, for nex round input which will be predicted by
        the script
        :return: cleared string with 1 and 0 only
        """
        cleared_input = ""
        if len(self.main_string) == 0:
            minimum_chars = 100
        else:
            minimum_chars = 10
        while len(cleared_input) < minimum_chars:
            for i in user_input:
                try:
                    if int(i) > 1:
                        user_input = user_input[:user_input.index(i)] + user_input[user_input.index(i) + 1:]
                except ValueError:
                    user_input = user_input[:user_input.index(i)] + user_input[user_input.index(i) + 1:]

            cleared_input += user_input
            if len(cleared_input) < minimum_chars:
                print(f"Current data length is {len(cleared_input)}, {minimum_chars - len(cleared_input)} symbols left")
                user_input = input("Type a random string containing 0 or 1:\n")
            else:
                self.main_string += cleared_input
        return cleared_input

    def generate_triads(self):
        """
        From the main string triads are generated, which will be used to predict next character. E.g "101": [5, 2] means
        that in the main string after sequence 101 0 follows 5 times and 1 follows 2 times
        :return: dictionary with triads
        """
        first_char = 0
        last_char = 3
        for _ in range(len(self.main_string) - 2):
            triad = self.main_string[first_char:last_char]
            next_char = self.main_string[first_char:last_char + 1]
            if len(next_char) == 3:
                continue
            else:
                next_char = next_char[-1]
                if next_char == "1":
                    self.triads_dict[triad][1] += 1
                elif next_char == "0":
                    self.triads_dict[triad][0] += 1
            first_char += 1
            last_char += 1

        return self.triads_dict

    def prediction_round(self, user_input):
        """
        Script uses triads to generate string with the same length as new user input. After that calculates percentage
        of correct guesses
        :param user_input: input from user which should be predicted
        :return: nothing
        """
        first_triad = ""
        triad_sum = 0
        for triad in self.triads_dict:
            if sum(self.triads_dict[triad]) > triad_sum:
                triad_sum = sum(self.triads_dict[triad])
                first_triad = triad
        print("prediction:")
        first_char = 0
        last_char = 3
        for _ in range(len(user_input) - 3):
            triad = user_input[first_char:last_char]
            if self.triads_dict[triad][0] > self.triads_dict[triad][1]:
                first_triad += "0"
            else:
                first_triad += "1"
            first_char += 1
            last_char += 1
        print(first_triad)
        correct_guess_counter = 0
        for x, y in zip(first_triad[3:], user_input[3:]):
            if x == y:
                correct_guess_counter += 1

        total_chars = len(user_input)
        percentage = round((correct_guess_counter / total_chars) * 100, 2)

        print(
            f"Computer guessed right {correct_guess_counter} out of {len(user_input)} symbols ({percentage} %)\n")


def main():
    prediction = UserInputPrediction()
    first_input = input("Type a random string containing 0 or 1:\n")
    prediction.process_user_input(first_input)
    prediction.generate_triads()

    # First round of prediction
    round_input = input("Type a random string containing 0 or 1, the script will try to predict it:\n")
    cleared_input = prediction.process_user_input(round_input)
    prediction.generate_triads()
    prediction.prediction_round(cleared_input)

    while True:
        ask_for_another_round = input("Another round? [Y/n]\n")
        while ask_for_another_round not in ["Y", "n"]:
            ask_for_another_round = input("Sorry, I don't understand. Do you wanna play another round? [Y/n]\n")
        if ask_for_another_round == "Y":
            round_input = input("Type a random string containing 0 or 1, the script will try to predict it:\n")
            cleared_input = prediction.process_user_input(round_input)
            prediction.generate_triads()
            prediction.prediction_round(cleared_input)

        elif ask_for_another_round == "n":
            print("Thank you for the game! See you next time!")
            break


if __name__ == "__main__":
    main()
