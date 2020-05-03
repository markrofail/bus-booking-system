<!-- PROJECT SHIELDS -->
[![Made With Django][django-shield]][django-shield]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<p align="center">
  <a href="https://github.com/markrofail/bus-booking-system">
    <img src="doc/assets/logo.svg" alt="Logo" width="100" height="100">
  </a>

  <!-- PROJECT TITLE -->
  <h3 align="center">Bus Reservation System</h3>

  <!-- PROJECT LINKS -->
  <p align="center">
    The is an implementation of a bus reservationsystem backend API
    <br />
    To be consumed by a web or mobile frontend
    <br />
    <a href="https://github.com/markrofail/bus-booking-system">View Demo</a>
    ·
    <a href="https://github.com/markrofail/bus-booking-system/issues">Report Bug</a>
    ·
    <a href="https://github.com/markrofail/bus-booking-system/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

- [Installation](#installation)
  - [The Docker way](#the-docker-way)
  - [The Hard way](#the-hard-way)
- [Usage](#usage)
  - [Endpoints](#endpoints)
  - [Loading Demo Data](#loading-demo-data)
  - [Admin Dashboard](#admin-dashboard)
- [Roadmap](#roadmap)
  - [Software Requirements Specification](#software-requirements-specification)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

<!-- GETTING STARTED -->
## Installation

This repo is configured to use docker.

### The Docker way

```bash
    docker-compose up --build
```

### The Hard way

#### Prequesities

- PostgreSQL
- Python 3.6+

#### Dependencies

```bash
    pip install -r requirements.txt
```

#### Migrations

```python
    python manage.py makemigrations
    python manage.py migrate
```

Now you are ready to use the system. It is easier to test the system after populating it with demo data. [Follow the steps here.](#loading-demo-data)

## Usage

To run the server on `localhost:8000`

```bash
    python manage.py runserver
```

### Endpoints

There are **6** endpoints implemented

#### Index Endpoint

- `GET /`
  - returns `{"healthCheck": "ok"}` to ensure system is up
![endpoint-gif-index][endpoint-gif-index]

#### Token Endpoints

`access` token has a liftime of 5 minutes while the `refresh` token lasts one day

- `POST api/v1/token/`
  - request body should contain `username` and `password` fields
  - returns json with `access` token and `refresh` token
![endpoint-gif-token][endpoint-gif-token]

- `POST api/v1/token/refresh`
  - request body should contain `refresh` token
  - returns json with refreshed `access` token
![endpoint-gif-token-refresh][endpoint-gif-token-refresh]

#### ReservationSystem Endpoints

- `GET api/v1/reservationsystem/stations`
  - returns all stations in the database
![endpoint-gif-stations][endpoint-gif-stations]

- `GET api/v1/reservationsystem/trips`
  - query params should contain `date_from`, `date_to`, `departure_station` and `arrival_station`
  - returns all available trips within the mentioned time range going from `departure_station` to `arrival_station`
  - `departure_station` and `arrival_station` ids should be obtained from `GET /stations`
![endpoint-gif-trips][endpoint-gif-trips]


- `POST api/v1/reservationsystem/reservation`
  - request body should contain `trip` corresponding to the desired trip id
  - the `trip` id should be obtained from `GET /trips`
![endpoint-gif-reservations][endpoint-gif-reservations]

### Loading Demo Data

```bash
  docker-compose run backend python manage.py loaddata customers busstations buses triproutes tripstops trips
```

The system is loaded with **30** Trips with **8** different routes, **42** different bus stations, **4** buses

#### Users

- Admin
  - role: SuperUser
  - username: `admin`
  - pass: `heavybat38`

- Alice
  - role: Customer
  - username: `alice`
  - pass: `bentpump66`

- Bob
  - role: Customer
  - username: `bob`
  - pass: `loudreptile70`

### Admin Dashboard

The Django admin dashboard can be found at `/admin`
please use the Admin's crentials above to login.

## Roadmap

This section talks about how I arrived to the end product delivered

### Software Requirements Specification

#### User Stories

Two Basic Functionalities are required

- As a Customer, I can get a list of available seats to be booked for his trip by sending start and end stations.
- As a Customer, I can book a seat if there is an available seat.

#### Database Design

![UML Diagram][uml-diagram]

Customer Relationships

- A Customer can have many Reservations, but a Reservation can only one Customer

Trip Relationships

- A Trip can have one Bus, but a Bus can have many Buses
- A Trip can have multiple Reservations, but a Reservations can only have one Trip
- A Trip can have one TripRoute, but a a TripRoute can belong to multiple Trips
- A TripRoute has multiple TripStops, but a TripStop can only belong to one TripRoute
- A TripStop can only have one BusStation, but a BusStation can belong to multiple TripStops.

##### Pros of Design

- A new Trip can be easily created by choosing a predefined TripRoute
- We can define the TripLine as an ordered sequence of TripStops incontrast to a currentStop, nextStop kind-of-architecture to avoid linked list architecture
- A Trip can be uniquly defined by its `TravelLine` and `departure_date`

##### Cons of Design

- To access a BusStation name you need to access `Trip.TripRoute.TripStop.BusStation.name`
- The Trip does all the work. A single point of responsibility issue.

### Currnet Limitaions

- If a Trip is going from A to B to C and a customer makes a reservation from A to B, the bus seat is not released. If someone tries to book it from B to C it is unavailable. More time needs to go into this.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Acknowledgements

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Simple JWT](]https://django-rest-framework-simplejwt.readthedocs.io/en/latest)
- Django Styleguide by [HackSoftware](https://github.com/HackSoftware/Django-Styleguide)
- Project Logo made by [Darius Dan](https://www.flaticon.com/authors/darius-dan)

## License

[MIT](https://choosealicense.com/licenses/mit/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/markrofail/bus-booking-system.svg?style=flat-square
[contributors-url]: https://github.com/markrofail/bus-booking-system/graphs/contributors
[heroku-url]: http://heroku-badge.herokuapp.com/?app=bus-reservation-system&style=flat
[forks-shield]: https://img.shields.io/github/forks/markrofail/bus-booking-system.svg?style=flat-square
[forks-url]: https://github.com/markrofail/bus-booking-system/network/members
[stars-shield]: https://img.shields.io/github/stars/markrofail/bus-booking-system.svg?style=flat-square
[stars-url]: https://github.com/markrofail/bus-booking-system/stargazers
[issues-shield]: https://img.shields.io/github/issues/markrofail/bus-booking-system.svg?style=flat-square
[issues-url]: https://github.com/markrofail/bus-booking-system/issues
[license-shield]: https://img.shields.io/github/license/markrofail/bus-booking-system.svg?style=flat-square
[license-url]: https://github.com/markrofail/bus-booking-system/blob/master/LICENSE
[django-shield]: https://img.shields.io/badge/Made%20With-Django-blue.svg?style=flat-square
[uml-diagram]: doc/assets/images/uml_diagram.png
[endpoint-gif-index]: doc/assets/images/endpoint-index-v2-min.gif
[endpoint-gif-token]: doc/assets/images/endpoint-token-v2-min.gif
[endpoint-gif-trips]: doc/assets/images/endpoint-trips-v2-min.gif
[endpoint-gif-stations]: doc/assets/images/endpoint-stations-v2-min.gif
[endpoint-gif-reservations]: doc/assets/images/endpoint-reservations-v2-min.gif
[endpoint-gif-token-refresh]: doc/assets/images/endpoint-token-refresh-v2-min.gif
