restaurants
===========

unrealists Python Challenge.

# Installation & Running

```
# Asumming Ubuntu
sudo apt install fish virtualenv

virtualenv -p python3 env
source env/bin/activate

git clone git@github.com:wieczorek1990/restaurants.git
cd restaurants

./instal.fish

./run_dev.fish
# or
./run_prod.fish
```

# Docker

Host port is 80.

```
sudo apt install -y docker.io docker-compose
docker-compose up
```

# Routes

* `/restaurants/near/:lat/:lon`
* `/restaurants/near/:address`
* `/restaurants/combo/:cuisine_a/:cuisine_b`

# Sample queries

```
http GET 'localhost:5000/restaurants/near/52.538554/13.4102856'
http GET 'localhost:5000/restaurants/near/Berlin'
http GET 'localhost:5000/restaurants/combo/noodles/vietnamese'
```
