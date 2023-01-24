# Abschlussprojekt zur LV "Solution Deployment & Communication"


### Aufgabenstellung:
- Teil 1 der Projektabgabe: Visualisierung und visuelle Auswertung eines Datensets, wie inhaltlich vorgetragen
- Teil 2 der Projektabgabe: Bereitstellung eines ML Modells via REST API, das kann sein Computer Vision, Objekt Classification , inkl. automatisiertem Deployment
----------------------------------------------

### Milestones:
Für das Projekt wurden einige Milestones definiert, diese sind im Repository unter Issues --> Milestones abgebildet und dokumentiert.

----------------------------------------
### Details zur Umsetzung:

### Basis: 
Als Datengrundlage dient ein öffentlich verfügbares Datenset zur Titanic. Beim Untergang der RMS Titanic im Jahr 1912 starben insgesamt 1.495 Menschen, 712 überlebten. Es sind Daten zu den Passagieren erfasst, zB das Alter, die Kategorie, in der sie gereist sind und ob sie überlebt haben oder nicht.


### interaktive Darstellung:
- TODO
- Beschreibung Dashboard / Plots etc.
- interaktiver Umgang mit dem Dashboard (diverse Aus-wahlen und Reaktionen darauf)

### REST API:
Um die Daten aus dem Frontend an das ML Modell übergeben zu können, wird eine FastAPI als REST-Schnittstelle verwendet.
Die Schnittstelle bekommt die Parameter von Streamlit übergeben und liefert einen numerischen Wert zurück. Zum besseren Verständnis der Schnittstelle kann über einen Button das JSON-Objekt angezeigt werden, das in der POST-Methode übergeben wird.

### ML Modell:
Als Modell wird das pickle-File von https://github.com/tlary/Kaggle_Titanic verwendet.
Als Eingabewerte werden das Alter, Größe der Familie, Klasse, Geschlecht und der Einstiegsort zum Schiff erwartet.
Aus diesen Werten berechnet das Modell eine Wahrscheinlichkeit, dass ein Passagier mit den gewählten Parametern das Schiffsunglück überlebt hätte.

### CI / CD Automation:
Die Builds für eine kontinuierliche Integration werden mittels Github-Action erstellt. Für Streamlit und FastAPI werden mit einem Dockerfile jeweils die Docker-Images erzeugt. Diese werden in ein öffentliches Docker-Hub Repository gepusht. Die einzelnen Steps der Builds werden in einem File "main.yml" definiert (diese sind im Repository unter Actions --> Workflows abgebildet und dokumentiert). Bei jedem Commit werden die Builds ausgeführt, sodass im Dockerhub immer die aktuellsten Images verfügbar sind. 
