import requests
import json

BASE_URL = 'http://localhost:8000/api/'  # Replace with your backend API URL
USERNAME = 'admin'  # Replace with the username of the user with access
PASSWORD = '123'  # Replace with the user's password

def get_jwt_token():
    # Authenticate the user and retrieve the JWT token
    response = requests.post(BASE_URL + 'token/', data={
        'username': USERNAME,
        'password': PASSWORD,
    })
    if response.status_code == 200:
        data = response.json()
        return data['access']
    else:
        print("Failed to get JWT token.")
        return None

def post_question_and_choices(jwt_token, questions_and_choices):
    headers = {'Authorization': f'Bearer {jwt_token}'}

    for data in questions_and_choices:
        # Post the question
        question_response = requests.post(BASE_URL + 'questions/', headers=headers, data=data)
        if question_response.status_code == 201:
            question_data = question_response.json()
            question_id = question_data['id']

            # Post the choices for each question
            for choice_data in data['choices']:
                choice_data['question'] = question_id
                choice_response = requests.post(BASE_URL + 'choices/', headers=headers, data=choice_data)
                if choice_response.status_code != 201:
                    print(f"Failed to post choice for question {question_id}.")
        else:
            print("Failed to post question.")

def simulate_quiz():
    jwt_token = get_jwt_token()
    if jwt_token:
        for x in range(1,11):
            with open(f'questions_and_choices_level{x}.json') as f:
                questions_and_choices = json.load(f)
            post_question_and_choices(jwt_token, questions_and_choices)

if __name__ == "__main__":
    simulate_quiz()
