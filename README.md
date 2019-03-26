# What's this?

Source code of Twitter bot to tweet price fluctuation of cryptocurrency.

https://twitter.com/CoinPriceAlert

# Source of the price chart

- Zaif
- Coincheck

# How to use

## 1. clone

```
git clone <this>
cd coin-price-alert
```

## 2. Create Twitter consumer key file

Please create consumer.json file in reference to consumer.sample.json

## 3. Create Twitter token key file

```
python get_token.py
```

## 4. Run container

```
sudo docker build -t redshoga/coin-price-alert .
sudo docker run -d -v /path/to/coin-price-alert:/main redshoga/coin-price-alert
```

# Memo

I made it several years ago, so the API might not be able to use.

# License

MIT License

