Omschrijving verwijderde bestanden.

learn-subset-test-one.py:

Opzet experiment: we werken met de niet gesplitte data (train-test) en selecteren eerst een aanval.
Vervolgens selecteren we random evenveel in instanties uit de benign dataset en dit vormt onze test dataset.
De rest vormt de train-dataset. Dit doen we voor alle aanvallen. Ik merkte in dit bestand dat 2_Preprocessed_DDoS niet bestond.

transfer-learning attack-learning.py:

We gaan weer alle aanvallen langs net als de vorige keer. 
We selecteren als train een aanval en al het benign verkeer en als test een aanval met hetzelfde normale verkeer.
Je merkt al dat dit niet klopt omdat je dus hetzelfde normale verkeer gebruikt. 
Hier zat nog een module met het zoeken naar de beste hyperparameters

increase-train-samples:

Toevoegen van samples om te kijken wat de f1 score wordt als we meer samples in onze aanvallen zetten. Eigenlijk dus active learning idee

experimental_setup_2:

Zit dicht tegen learn-subset-test-one aan

