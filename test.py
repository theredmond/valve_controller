def find_all(sum_dig, digs):
    test_digit = int("".join(["1"]*digs))
    answers = []
    while test_digit:

        if get_sum(test_digit) is sum_dig:
            answers.append(test_digit)
        
        test_digit = increment(test_digit)
    if answers:
        return [
            len(answers) or 1,
            answers[0] or 999,
            answers[-1] or 999
        ]
    else:
        return answers

def get_sum(num):
    test_sum = 0
    while num > 0:
        test_sum += num % 10
        num = num // 10
    return test_sum

def increment(num):
    if num % 10 < 9:
        return num + 1
    
    digits = [int(i) for i in str(num)]
    digits.reverse()
    for idx, digit in enumerate(digits):
        if digit < 9:
            new_lowest = digits[idx] + 1
            digits[idx] = new_lowest
            for sub_idx in range(0, idx):
                digits[sub_idx] = new_lowest
            digits.reverse()
            s = ''.join(map(str, digits))
            return int(s)
        else:
            pass

print(find_all(10, 3))
print(find_all(27, 3))
