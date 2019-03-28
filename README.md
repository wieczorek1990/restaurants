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

./run.fish

```

# Routes

* `/restaurants/near/:lat/:lon`
* `/restaurants/near/:address`
* `/restaurants/combo/:cuisine_a/:cuisine_b`
