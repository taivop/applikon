# Bioreactor data poller

This application requests data from Applikon bioreactors in the network and uploads it to an InfluxDB instance.



### Installation

Requirements:
* Python 3.9 (earlier might work)

```
pip install -r requirements.txt

cp .env.example .env
```

And then update the secret keys within `.env` file.

### Configuration
* Available bioreactors, their names and IP addresses can be configured in `reactors.json`.
* The environment can be configured in `.env`.

### Starting manually

```
python3 poll.py
```

### Starting automatically on boot

To setup the systemd daemon, do

```
# Link the file so git repo updates get applied.
sudo ln -s bioreactor.service /lib/systemd/system/bioreactor.service

sudo chmod 644 bioreactor.service

sudo systemctl daemon-reload

sudo systemctl enable bioreactor.service
sudo systemctl start bioreactor.service
```

### Development

1. Install `pre-commit` with `pip install pre-commit`.
2. Run `pre-commit install`.
