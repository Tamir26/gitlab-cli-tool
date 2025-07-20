import gitlab
import os 
from datetime import datetime
import argparse


GITLAB_URL = os.getenv('GITLAB_URL')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
if not GITLAB_TOKEN:
    raise ValueError("GITLAB_TOKEN environment variable is not set")

if not GITLAB_URL:
    raise ValueError("GITLAB_URL environment variable is not set")

gl = gitlab.Gitlab(url=GITLAB_URL, private_token=GITLAB_TOKEN,keep_base_url=True)
gl.auth()   

def get_user(username: str) -> object:
    users = gl.users.list(username=username)
    if not users:
        raise ValueError(f"User {username} not found")
    user = users[0]

    return user
def get_project_by_name(project_name: str):
    projects = gl.projects.list(search=project_name)
    return projects[0] if projects else None

def get_user_group_by_name(user_group_name: str):
    user_groups = gl.groups.list(search=user_group_name)
    return user_groups[0] if user_groups else None
        
def get_access_level_from_role(role: str) -> int:
    
    role_map = {
        "no access": 0,
        "minimal access": 5,
        "guest": 10,
        "reporter": 20,
        "developer": 30,
        "maintainer": 40,
        "owner": 50
    }
    role = role.lower()
    if role not in role_map:
        raise ValueError(f"Invalid role: {role}")
    access_level = role_map[role]
    return access_level

def function_1(username: str,name: str, role: str)->None:
    user= get_user(username=username)
    project = get_project_by_name(project_name=name)
    user_group=get_user_group_by_name(user_group_name=name)
    desired_access_level=get_access_level_from_role(role=role)
    
    if not project and not user_group:
        raise ValueError(f"No project or group found with name '{name}'")
    
    if project:
        try:
            member=project.members.get(user.id)
            if member.access_level != desired_access_level:
                member.access_level = desired_access_level
                member.save()
                print(f"Updated user '{username}' role in project '{name}' to {role}")
            else:
                print(f"User '{username}' already has the correct role in project '{name}'")
        except gitlab.exceptions.GitlabGetError:
            try:
                project.members.create({'user_id':user.id, 'access_level':desired_access_level})
                print(f"Added user '{username}' to project '{name}' as {role}")
            except gitlab.exceptions.GitlabCreateError as e:
                    print(f"Error adding to project: {e}")

    if user_group:
        try:
            member=user_group.members.get(user.id)
            if member.access_level != desired_access_level:
                member.access_level = desired_access_level
                member.save()
                print(f"Updated user '{username}' role in user group '{name}' to {role}")
            else:
                 print(f"User '{username}' already has the correct role in group '{name}'")
        except gitlab.exceptions.GitlabGetError:
            try:
                user_group.members.create({'user_id':user.id,'access_level':desired_access_level})
                print(f"Added user '{username}' to user group '{name}' as {role}")
            except gitlab.exceptions.GitlabCreateError as e:
                print(f"Error adding to group: {e}")

def validate_and_parse_year(year_input: int) -> tuple[datetime,datetime]:
    year = int(year_input)
    if year < 1000 or year > 9999:
        raise ValueError("Year must be a 4-digit number.")
    start_of_year = datetime(year, 1, 1)
    start_of_next_year = datetime(year + 1, 1, 1)
    return start_of_year,start_of_next_year

def function_2(item_type: str, year: int)-> list:
    if item_type.lower() not in ['merge_requests','issues']:
        raise ValueError('item type do not match please enter only merge_requests or issues')
    
    if not isinstance(year, int):
        raise ValueError("Year must be an integer")
    start_of_the_desired_year, end_of_the_desired_year,=validate_and_parse_year(year_input=year)

    results = []
    projects=gl.projects.list(iterator=True)
    for project in projects:
        if item_type == 'merge_requests':
            for mr in project.mergerequests.list(created_after=start_of_the_desired_year
                                            ,created_before=end_of_the_desired_year,
                                            iterator=True):
                print(f"\nLooking at MR {mr.id}")
                print(f"\t{mr.created_at}")
                results.append((project.name,mr))

        else:
            for issue in project.issues.list(created_after=start_of_the_desired_year
                                        ,created_before=end_of_the_desired_year,
                                        iterator=True):
                print(f"\nLooking at issue {issue.id}")
                print(f"\t{issue.created_at}")
                results.append((project.name,issue))
    
    if not results:
        print(f"No {item_type} found from the year {year}.")
        
    return results


    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="GitLab role manager and activity fetcher")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for function_1
    parser_role = subparsers.add_parser("function_1", help="Set or update a user's role")
    parser_role.add_argument("--username", type=str, help="GitLab username",required=True)
    parser_role.add_argument("--name", type=str, help="Project or group name",required=True)
    parser_role.add_argument("--role",choices=["no access","minimal access","guest","reporter","developer" ,"maintainer","owner"], type=str, help="Role to assign (e.g. developer, guest, etc.)",required=True)

    # Subparser for function_2
    parser_list = subparsers.add_parser("function_2", help="List issues or MRs from a specific year")
    parser_list.add_argument("--item_type", type=str,choices=['merge_requests','issues'], help="Type: issues or merge_requests",required=True)
    parser_list.add_argument("--year", type=int, help="Year to filter by (4-digit)",required=True)

    args = parser.parse_args()

    if args.command == "function_1":
        function_1(args.username, args.name, args.role)
    elif args.command == "function_2":
        function_2(args.item_type, args.year)
    else:
        parser.print_help()
