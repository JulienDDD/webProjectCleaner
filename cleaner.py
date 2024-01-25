import os
import re
import shutil


""" 
La fonction list_all_files prend un parametre le dossier ou se trouve tout les fichiers
la fonction va recuperer chaque fichier dans chaque dossiers / sous dossier
    
"""
def list_all_files(directory):

    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.relpath(os.path.join(root, file), directory))
    return files_list

""" 
La fonction find_included_files prend un parametre le fichier et le repertoire
la fonction va verifier si le fichier est utilisé quelque part dans le projet 
    
"""
def find_included_files(file, base_dir):

    included_files = []
    with open(os.path.join(base_dir, file), 'r', encoding='utf-8') as f:
        content = f.read()
        patterns = {
            '.html': [r'href="([^"]+)"', r'src="([^"]+)"'],
            '.css': [r'url\(([^)]+)\)'],
            '.js': [r'src="([^"]+)"'],
            '.php': [r'include\("([^"]+)"\)', r'require\("([^"]+)"\)', r'include_once\("([^"]+)"\)', r'require_once\("([^"]+)"\)'],
        }

        for ext, ext_patterns in patterns.items():
            for pattern in ext_patterns:
                for match in re.findall(pattern, content):
                    match = match.strip('"').strip("'")
                    if not os.path.isabs(match):
                        match = os.path.normpath(os.path.join(os.path.dirname(file), match))
                    if match.endswith(ext):
                        included_files.append(match)

    return included_files
    """
la fonction copy_project va copier le contenu de inputFolder et le mettre dans outputFolder (pour pouvoir agir directement dans outputfolder)
    
    """
def copy_project(input_project, output_project):

    if os.path.exists(output_project):
        shutil.rmtree(output_project)
    shutil.copytree(input_project, output_project)

def main(input_project, output_project):

    copy_project(input_project, output_project)

    all_files = set(list_all_files(output_project))
    used_files = set()

    # Analyser chaque fichier dans output_project
    for file in all_files:
        file_ext = os.path.splitext(file)[1]
        if file_ext in ['.html', '.css', '.js', '.php']:
            used_files.add(file)
            included_files = find_included_files(file, output_project)
            used_files.update(included_files)

    # Supprimer les fichiers inutilisés dans output_project
    for file in all_files - used_files:
        full_path = os.path.join(output_project, file)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Supprimé de outputProject: {file}")

if __name__ == "__main__":
    input_project = 'inputProject'
    output_project = 'outputProject'
    main(input_project, output_project)
