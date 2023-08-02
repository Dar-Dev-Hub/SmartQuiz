import requests

BASE_URL = 'http://localhost:8000/api/'  # Replace with your backend API URL
USERNAME = 'admin'  # Replace with the username of the user you want to simulate

def get_jwt_token():
    # Authenticate the user and retrieve the JWT token
    response = requests.post(BASE_URL + 'token/', data={
        'username': USERNAME,
        'password': '123',  # Replace with the user's password
    })
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        return data['access']
    else:
        print("Failed to get JWT token.")
        return None

def start_quiz(jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.post(BASE_URL + 'init-quiz/', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("Starting Quiz...")
        return data
    else:
        print("Failed to start the quiz.")
        return None

def submit_answer(jwt_token, quiz_submission_id, question_id, choice_id, is_correct):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.post(BASE_URL + f'quiz-submissions/{quiz_submission_id}/submit/', headers=headers, data={
        'question': question_id,
        'choice': choice_id,
        'is_correct': is_correct
    })
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        if 'next_question' in data:
            return data['next_question']
        else:
            print("Quiz completed. Your final score:", data['score'])
    else:
        print("Failed to submit the answer.")
    return None

def simulate_quiz():
    jwt_token = get_jwt_token()
    if jwt_token:
        quiz_data = start_quiz(jwt_token)
        if quiz_data:
            quiz_submission_id = quiz_data['quiz_submission_id']
            question_data = quiz_data['question']
            while question_data:
                print("Question:", question_data['content'])
                for choice in question_data['choices']:
                    print(f"{choice['id']}: {choice['content']}")
                choice_id = int(input("Enter your choice (by ID): "))
                validate_choice = requests.get(BASE_URL + f'choices/{choice_id}/',headers={'Authorization': f'Bearer {jwt_token}'})
                is_correct = validate_choice.json()['is_correct']
                next_question = submit_answer(jwt_token, quiz_submission_id, question_data['id'], choice_id,is_correct)
                if not next_question:
                    break
                question_data = next_question

if __name__ == "__main__":
    simulate_quiz()