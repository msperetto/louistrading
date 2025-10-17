#!/bin/bash
# Run a single test manually using Docker

if [ $# -lt 4 ]; then
    echo "Usage: ./run_single_test.sh 'Title' YYYY-MM-DD COIN1 COIN2 ..."
    echo ""
    echo "Example:"
    echo "  ./run_single_test.sh 'Binance Will Delist BTC, ETH on 2025-12-31' 2025-12-31 BTC ETH"
    exit 1
fi

TITLE="$1"
DATE="$2"
shift 2
COINS="$@"

# Convert coins to JSON array
COINS_JSON="["
for coin in $COINS; do
    COINS_JSON+="\"$coin\","
done
COINS_JSON="${COINS_JSON%,}]"  # Remove trailing comma

echo "Creating test announcement..."
echo "Title: $TITLE"
echo "Date: $DATE"
echo "Coins: $COINS_JSON"
echo ""

# Run quick_test.py inside Docker
docker-compose run --rm integration_test \
    python main/tests/integration/quick_test.py create "$TITLE" "$DATE" $COINS

echo ""
echo "Now watch delist logs:"
echo "  docker-compose logs -f delist"
