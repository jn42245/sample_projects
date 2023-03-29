# Created by Thierry Tran
# Created on 24 December 2022
# Create functions to generate text


def compare_data_text(first_number: float, last_number: float, first_year: int, last_year: int, name: str, metric: str):
    if first_number < last_number * 0.99:
        variation = 'increase'
    elif first_number > last_number * 1.01:
        variation = 'decrease'
    else:
        sentence = 'Between {fy} and {ly}, there was no significant change in {met} in {nam}.'.format(fy=first_year,
                                                                                                        ly=last_year,
                                                                                                        met=metric,
                                                                                                        nam=name)
        return sentence
    sentence = 'Between {fy} and {ly}, there was an {var} of {pc} % in {met} in {nam}. ' \
               'This represents a change of {delta} units.'.format(fy=first_year,
                                                                   ly=last_year,
                                                                   pc=round((last_number-first_number)/first_number*100,
                                                                            2),
                                                                   nam=name,
                                                                   met=metric,
                                                                   delta=round((last_number-first_number), 2),
                                                                   var=variation)
    return sentence


def countries_highlighted_text(input_list: list):
    if len(input_list) == 1:
        sentence = 'The country highlighted is {}.'.format(input_list[0])
        return sentence
    elif len(input_list) == 2:
        sentence = 'The countries highligted are {} and {}.'.format(input_list[0], input_list[1])
        return sentence
    else:
        first_temp_list = input_list[:-2]
        temp_sentence = ''
        for ele in first_temp_list:
            temp_sentence = temp_sentence + ele + ', '
        sentence = 'The countries highlighted are {}{} and {}.'.format(temp_sentence, input_list[-2], input_list[-1])
        return sentence


if __name__ == '__main__':
    print(compare_data_text(10, 100, 2021, 2022, 'sales', 'France'))
    print(compare_data_text(10, 10, 2021, 2022, 'sales', 'France'))
    print(compare_data_text(10, 0, 2021, 2022, 'sales', 'France'))
    print(countries_highlighted_text(['France', 'Italy', 'Germany', 'China']))
