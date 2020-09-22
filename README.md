# 🏥 Infirmary

Welcome to "Infirmary", the [ReST-based](https://restfulapi.net/) [application programming interface](https://www.mulesoft.com/resources/api/what-is-an-api) for the [Clinical Data component](https://github.com/MCLConsortium/clinical-data) of the the [Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions](https://mcl.nci.nih.gov/). This project, along with [Sickbay](https://github.com/MCLConsortium/clinical-data/tree/master/sickbay) form a database for discovering clinical data.


## ⚙️ Endpoints

Once deployed, this package provides the following ReST API endpoints:

| Endpoint                          | Auth | Purpose                                                        |
| :-------------------------------- | :--: | :------------------------------------------------------------- |
| `/ping`                           |      | Test if the server is working                                  |
| `/hello/{greeting}`               |  🔐  | Test if authentication is working                              |
| `/clinicalCores`                  |  🔐  | Return all Clinical Cores in the database, fully serialized    |
| `/clinicalCores/{participant_ID}` |  🔐  | Return the single Clinical Core for the named `participant_ID` |
| `/organs`                         |  🔐  | Return all organs in the database                              |
| `/organs/{identifier}`            |  🔐  | Return the single organ with the numeric `identifier`          |
| `/specimens`                      |  🔐  | Return all biospecimens in the database                        |
| `/specimens/{specimen_ID}`        |  🔐  | Return the single biospecimen with the given `specimen_ID`     |
| `/genomics`                       |  🔐  | Return all genomics in the database                            |
| `/genomics/{specimen_ID}`         |  🔐  | Return the genomics information with the given `specimens_ID`  |
| `/images`                         |  🔐  | Return all imaging information in the database                 | 
| `/images/{identifier}`            |  🔐  | Return the imaging information with the numeric `identifier`   |

For those endpoints where the "Auth" column is dispays 🔐, you must provide an HTTP Basic Authentication header with a username and password of a member of the Consortium for Molecular and Cellular Characterization of Screen-Detected Lesions. All of the endpoints return a JSON payload.


## 🔧 Development

To develop locally with a local Postgres database:

```console
python3 bootstrap.py
bin/buildout
bin/infirmary --debug
```

To create and register the image:

```console
docker image build --tag mcl-infirmary:latest .
docker image tag mcl-infirmary:latest nutjob4life/mcl-infirmary:latest
docker login
docker image push nutjob4life/mcl-infirmary:latest
```

To explore the image:

    docker container run --rm --interactive --tty --entrypoint /bin/sh mcl-infirmary:latest
