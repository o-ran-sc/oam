import csv
import json
from argparse import ArgumentParser

from jinja2 import Template


class UserCreator:
    template_str = """
    {
      "users": [
        {% for user in users %}
        {
          "firstName": "{{ user.firstName }}",
          "lastName": "{{ user.lastName }}",
          "email": "{{ user.email }}",
          "enabled": "{{ user.enabled }}",
          "username": "{{ user.username }}",
          "credentials": [
            {
              "type": "password",
              "value": "{{ user.password }}",
              {% if force_pwd_change is false %}
              "temporary": "{{ user.force_pwd_change }}"
              {% else %}
              "temporary": "true"
              {% endif %}
            }
          ],
          "requiredActions": [
            "UPDATE_PASSWORD"
          ]
        }{% if not loop.last %},{% endif %}
        {% endfor %}
      ],
      "grants": [
        {% for user in users %}
        {
          "username": "{{ user.username }}",
          "role": "{{ user.role }}"
        }{% if not loop.last %},{% endif %}
        {% endfor %}
      ]
    }
    """

    def __init__(self, csv_file: str):
        self.csv_file_path: str = csv_file

    def get_users_from_csv(self) -> list[dict]:
        """
        Get the users from the CSV file
        @return: list of users
        """
        users: list[dict] = []
        with open(self.csv_file_path, "r") as file:
            dict_reader: csv.DictReader = csv.DictReader(file)
            for row in dict_reader:
                users.append(row)
        return users

    def create_users_json(self, users: list[dict], output_json_path: str, force_pwd_change: bool ) -> None:
        """
        Create the users JSON from the users list. Uses Jinja2 template to create the JSON.
        @param users: list of users to create the JSON
        @param output_json_path: path to the output JSON file
        @return: JSON string
        """
        if force_pwd_change is True:
            print("Enforce password change for all users!")
        template = Template(self.template_str)
        users_json: str = template.render(users=users, force_pwd_change=force_pwd_change)
        with open(output_json_path, 'w') as f:
            json.dump(json.loads(users_json), f, indent=4)
        print(f"Users JSON file created at {output_json_path}")


if __name__ == '__main__':
    parser = ArgumentParser(description="Create users JSON file from CSV file")
    parser.add_argument("csv_file_path", type=str, help="Path to the CSV file containing the users data")
    parser.add_argument("--output", "-o", type=str, required=False, default="authentication.json",
                        help="Path to the output JSON file e.g. authentication.json")
    parser.add_argument("--force-pwd-change","-f", action='store_true', help="Enforce password change for all users, overwrites value in user data" )

    args = parser.parse_args()
    user_creator = UserCreator(args.csv_file_path)
    user_list = user_creator.get_users_from_csv()
    user_creator.create_users_json(user_list, args.output, args.force_pwd_change)
