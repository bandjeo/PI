# Poređenje pretraživača zakona Republike Srbije

Potrebni alati:
- Python 3.8.3+ (Pip)
- [Elasticsearch](https://www.elastic.co/)

### Pokretanje:
- Instalirati potrebne pakete iz requirements.txt `pip install -r requirements.txt`
- Pokrenuti *elasticsearch.bat* iz bin direktorijuma instalacije *Elasticsearch*
- Pokrenuti *migrate.py* iz direktorijuma *Elasticsearch*
- Unutar direktorijuma *webapp* pokrenuti komandu `flask run`
- Frontend aplikacije se nalazi na http://localhost:5000/public/index.html

### Upotreba aplikacije
- Izabrati pretraživač iz liste pretraživača
- Uneti upit
- Pokrenuti pretragu, koja vraća 10 rezultata odabranog pretraživača za dati upit.

### Ostale datoteke
- U direktorijumu *Notebooks* nalaze se jupyter datoteke sa kodom za treniranje modela.
- U direktorijumu *evaluation* nalazi se skripta *evaluation.py* i skup podataka za evaluaciju. Pokretanje skripte generiše csv datoteke sa rezultatima evaluacije
