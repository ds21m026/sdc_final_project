# Abschlussprojekt zur LV "Solution Deployment & Communication"


### Aufgabenstellung:
- Teil 1 der Projektabgabe: Visualisierung und visuelle Auswertung eines Datensets, wie inhaltlich vorgetragen
- Teil 2 der Projektabgabe: Bereitstellung eines ML Modells via REST API, das kann sein Computer Vision, Objekt Classification , inkl. auto matisiertem Deployment
----------------------------------------------

### Milestones:
Für das Projekt wurden einige Milestones definiert, diese sind im Repository unter Issues --> Milestones abgebildet und dokumentiert.

----------------------------------------
### Details zur Umsetzung:

### Basis: 
Als Datengrundlage dient ein öffentlich verfügbares Datenset zur Titanic. Beim Untergang der RMS Titanic im Jahr 1912 starben insgesamt 1.495 Menschen, 712 überlebten. Es sind Daten zu den Passagieren erfasst, zB das Alter, die Kategorie, in der sie gereist sind und ob sie überlebt haben oder nicht.


### Interaktive Darstellung:
Für die Darstellungen wurden zwei Datensets von Kaggle verwendet:
1. Titanic Extended Dataset: https://www.kaggle.com/datasets/pavlofesenko/titanic-extended
2. Complete Titanic Dataset: https://www.kaggle.com/datasets/vinicius150987/titanic3

Das erste Datenset wurde für die Visualisierung verwendet. Es ist um einige Variablen aus der ofiziellen Passagierliste von Wikipedia bereichert. Allerdings wurde auch hier als Grundlage das Datenset aus der Titanic ML Learning  Challenge verwendet. Deshalb is die Variable "survived", also ob der Passagier überlebt hat nicht für alle verfügbar. Deswegen wurden die Daten mit dem zweiten Set kombiniert, dass in dieser Hinsicht vollständig ist.

Das Dashboard wurde mittels Streamlit realisiert. Man kann das Datenset nach verschiedenen Kriterien filtern:
- Embarkation Point: Stadt in der der Passagier das Schiff bestiegen hat.
- Geschelcht
- Passagierklasse
- Anzahl der Eltern/Kinder an Bord
- Anzahl der Geschwister/Ehepartner
- Überlebt/Gestorben

Alle 3 Darstellungen sind interaktiv und ändern sich je nach Auswahl.

1. Choropleth Karte

Auf dieser Karte wurden für die jeweilige Auswahl der Passagiere die verschiedenen Länder eingefärbt. Dafür wurd das Datenset mithilfe von Openrefine bereinigt und die Ländernamen vereinheitlicht. Weiter wurden Länderbezeichnungen von Staaten die es nicht mehr gibt aktualisiert. So wurde "Russian Empire" 
zu "Russia" und "Siam" zu "Thailand". Da die Grenzen der Staaten oft nicht mehr mit den modernen Staaten des 21. Jahunderts übereinstimmen, konnten nicht alle Passagiere ihrem Heimatland zugeordnet werden.

2. Balkendiagramm

Das Balkendiagramm zeigt die Befüllung der Rettungsboote an. Es ist in chronologischer Reihenfolge sortiert. Das heißt Rettungsboot 7, das als erstes zu Wasser gelassen wurde, wird als erstes Dargestellt. Die Farben zeigen die Geschlechtszugehörigkeit der Passagiere an.

3. Density Plots

Auf diesen Plots ist die Verteilung der Altersklassen nach Passagierklasse dargestellt. Jeweils ein Plot steht für eine Passagierklasse. In heller Farbe ist die Gesamtanzahl dargestellt, in dunkler der Anteil and Überlebenden. 

### REST API:
Um die Daten aus dem Frontend an das ML Modell übergeben zu können, wird eine FastAPI als REST-Schnittstelle verwendet.
Die Schnittstelle bekommt die Parameter von Streamlit übergeben und liefert einen numerischen Wert zurück. Zum besseren Verständnis der Schnittstelle kann über einen Button das JSON-Objekt angezeigt werden, das in der POST-Methode übergeben wird.

### ML Modell:
Als Modell wird das pickle-File von https://github.com/tlary/Kaggle_Titanic verwendet.
Als Eingabewerte werden das Alter, Größe der Familie, Klasse, Geschlecht und der Einstiegsort zum Schiff erwartet.
Aus diesen Werten berechnet das Modell eine Wahrscheinlichkeit, dass ein Passagier mit den gewählten Parametern das Schiffsunglück überlebt hätte.

### CI / CD Automation:
Die Builds für eine kontinuierliche Integration werden mittels Github-Action erstellt. Für Streamlit und FastAPI werden mit einem Dockerfile jeweils die Docker-Images erzeugt. Diese werden in ein öffentliches Docker-Hub Repository gepusht. Die einzelnen Steps der Builds werden in einem File "main.yml" definiert (diese sind im Repository unter Actions --> Workflows abgebildet und dokumentiert). Bei jedem Commit werden die Builds ausgeführt, sodass im Dockerhub immer die aktuellsten Images verfügbar sind. 
