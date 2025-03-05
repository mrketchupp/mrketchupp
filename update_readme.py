import requests
import os

def get_latest_repos(username, token=None):
    """Obtiene los dos repositorios más recientes de un usuario de GitHub."""
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&direction=desc"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return repos[:2]  # Devuelve los dos primeros repositorios
    else:
        print(f"Error al obtener repositorios: {response.status_code}")
        return None

def update_readme(username):
    """Actualiza el README.md con los dos repositorios más recientes."""
    repos = get_latest_repos(username)
    if not repos:
        return  # Sale si no se pueden obtener los repositorios

    # Prepara la lista de repositorios con emojis
    repo_list = []
    if repos:
        repo_list.append(f"- 🔬 [{repos[0]['name']}](https://github.com/{username}/{repos[0]['name']})")
    if len(repos) > 1:
        repo_list.append(f"- 🛠️ [{repos[1]['name']}](https://github.com/{username}/{repos[1]['name']})")

    # Lee el contenido actual del README
    with open("README.md", "r") as file:
        readme_content = file.readlines()

    # Encuentra la sección "Ongoing Experiments" y actualízala
    start_updating = False
    new_readme_content = []
    for line in readme_content:
        if "#### Ongoing Experiments" in line:
            new_readme_content.append(line)
            new_readme_content.extend([f"{repo}\n" for repo in repo_list])
            start_updating = True
        elif start_updating and line.startswith("####"):
            new_readme_content.extend(readme_content[readme_content.index(line):])
            break
        elif not start_updating:
            new_readme_content.append(line)

    # Escribe el nuevo contenido en README.md
    with open("README.md", "w") as file:
        file.writelines(new_readme_content)

if __name__ == "__main__":
    username = "mrketchupp"  # Reemplaza con tu nombre de usuario de GitHub
    token = os.getenv("GITHUB_TOKEN")  # Obtiene el token de GitHub Actions, si está disponible
    update_readme(username)
    print("README actualizado con éxito.")
