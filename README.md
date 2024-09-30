# Sonaric_Monitoring

## Installation

### Cloner le dépôt

git clone https://github.com/Sown21/Sonaric_Monitoring.git

### Installer les prérequis

pip install -r requirements.txt

### Ajouter vos nodes

Editer le script et modifier la ligne ci-dessous :
hosts = ["Your_Nodes_Names"]

Vous pouvez ajouter tous vos nodes en séparant par "," 
Example : hosts = ["Your_Node_Name1", "Your_Node_Name2"]

### Lancer le script

cd Sonaric_Monitoring
python3 sonaric.py
