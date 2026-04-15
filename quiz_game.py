import json
import os
import random
import datetime
import subprocess
import time


def load_questions(difficulty):
    file = f'questions/{difficulty}.json'
    with open(file, 'r', encoding='cp850') as file:
            questions = json.load(file)

    random.shuffle(questions)
    return questions[:5]
    

def ask_question(question_obj):
    question = question_obj['question']
    options = question_obj['options']
    answer = question_obj['answer']

    random.shuffle(options)

    time.sleep(1)
    subprocess.run('cls', shell=True)

    print(f'\nQ: {question}')
    for i, option in enumerate(options, 1):
        print(f'{i}. {option}')
            
    while True:
        try:
            user_input = int(input())
            if 1 <= user_input <= len(options):
                break
            print(f'Please enter a number between 1 and {len(options)}.')
        except ValueError:
            print('Please enter a valid number.')
        
    user_answer = options[user_input - 1]

    print(f'Your answer: {user_input} - {user_answer}')

    if user_answer == answer:
         print('Correct! ✅')
         return True
    else:
         print(f'Incorrect! ❌ - The correct answer was {options.index(answer) + 1} - {answer}')
         return False


def check_if_highscore(difficulty, score, elapsed):
    file_name = f'score_tracker_{difficulty}.json'
    
    if not os.path.exists(file_name):
        with open(file_name, 'w', encoding='cp850') as f:
            json.dump([], f)
        return True

    with open(file_name, 'r', encoding='cp850') as f:
        scores = json.load(f)

    if len(scores) < 5:
        return True

    lowest = min(scores, key=lambda d: (d['score'], -d['seconds']))
    if score > lowest['score']:
        return True
    if score == lowest['score'] and elapsed < lowest['seconds']:
        return True
    return False


def run_quiz(difficulty):
    questions = load_questions(difficulty)
    score = 0
    start_time = datetime.datetime.now()

    for question in questions:
        correct = ask_question(question)
        if correct:
            score += 1

    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    elapsed_str = str(datetime.timedelta(seconds=int(elapsed)))
    
    time.sleep(1)
    subprocess.run('cls', shell=True)

    print(f'\nQuiz complete! You scored {score}/{len(questions)}.')
    if score == len(questions):
         print('Total expert! 😎')
    elif score >= len(questions) - 2:
         print('Wow, amazing! 🎉')
    elif score >= len(questions)/2:
         print('Not bad!')
    else:
         print('Keep practicing!')

    highscore = check_if_highscore(difficulty, score, elapsed)
    if highscore:
        print('\nNew highscore!!')

        while True:
            name = input('Enter your name: ').strip()
            if len(name) >= 1:
                break

        date = datetime.datetime.now().strftime('%c')

        user_data = {'date': date, 'name': name, 'score': score, 'time': elapsed_str, 'seconds': elapsed}
        
        with open(f'score_tracker_{difficulty}.json', 'r', encoding='cp850') as f:
            tracker_data = json.load(f)
        
        tracker_data.append(user_data)
        tracker_data = sorted(tracker_data, key=lambda d: (d['score'], -d['seconds']), reverse=True)
        tracker_data = tracker_data[:5]

        with open(f'score_tracker_{difficulty}.json', 'w', encoding='cp850') as f:
            json.dump(tracker_data, f, indent=2)

    with open(f'score_tracker_{difficulty}.json', 'r', encoding='cp850') as f:
            tracker_data = json.load(f)

    time.sleep(1)
    subprocess.run('cls', shell=True)

    print('---Leaderboard---')
    print(f'\n{'Rank':<6}{'Name':<20}{'Score':<10}{'Time':<12}{'Date'}')
    for i, record in enumerate(tracker_data, 1):
        print(f'{i:<6}{record['name']:<20}{record['score']:<10}{record['time']:<12}{record['date']}')


def play_again():
    print('\nWould you like to play again? (Y/n)')

    while True:
        user_input = input()
        if user_input in ('', 'y', 'Y'):
            return True
        elif user_input in ('n', 'N'):
            return False
        print('Please enter y or n')
    

def set_difficulty():
    print('Select a difficulty')
    difficulties  = []
    for dir_entry in os.scandir('questions'):
        if dir_entry.is_file():
            file_name, _ = os.path.splitext(dir_entry.name)
            difficulties.append(file_name)

    for i, difficulty in enumerate(difficulties, 1):
        print(f'{i}. {difficulty}')
    
    while True:
        try:
            user_input = int(input())
            if 1 <= user_input <= len(difficulties):
                break
            print(f'Please enter a number between 1 and {len(difficulties)}.')
        except ValueError:
            print('Please enter a valid number.')
    
    user_difficulty = difficulties[user_input - 1]
    print(f'{user_difficulty} mode selected')
    print('loading questions...')

    return user_difficulty

if __name__ == '__main__':
    try:
        playing = True
        while playing:
            print('\n--- Starting new game ---\n')
            difficulty = set_difficulty()
            run_quiz(difficulty)
            playing = play_again()
    except KeyboardInterrupt:
        pass

    print('\n--- Thanks for playing! ---\n')