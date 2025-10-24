#!/bin/bash
# Quick start script for running delist integration tests

set -e

echo "=========================================="
echo "Delist Integration Test - Quick Start"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not found${NC}"
    exit 1
fi

# Set environment to TEST
export ENVIRONMENT=TEST

echo -e "${YELLOW}Starting required Docker services...${NC}"
docker-compose up -d db api delist

echo -e "${YELLOW}Waiting for services to be ready (20 seconds)...${NC}"
sleep 20

# Check if services are running
echo -e "${YELLOW}Checking service status...${NC}"
docker-compose ps

# Check API health from inside Docker network
echo -e "${YELLOW}Checking API health...${NC}"
API_CHECK=$(docker-compose exec -T api curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null || echo "000")
if [ "$API_CHECK" = "200" ]; then
    echo -e "${GREEN}✓ API is accessible${NC}"
else
    echo -e "${YELLOW}⚠ API check returned $API_CHECK (will retry from test container)${NC}"
fi

# Check delist service
echo -e "${YELLOW}Checking delist service...${NC}"
if docker-compose ps delist | grep -q "Up"; then
    echo -e "${GREEN}✓ Delist service is running${NC}"
else
    echo -e "${RED}✗ Delist service is not running${NC}"
    echo "Please check: docker-compose logs delist"
    exit 1
fi

# Run tests in Docker container
echo ""
echo -e "${GREEN}=========================================="
echo "Running Integration Tests (in Docker)"
echo -e "==========================================${NC}"
echo ""

# Pass arguments to the test container
docker-compose run --rm \
    -e ENVIRONMENT=TEST \
    integration_test \
    python main/tests/integration/delist_integration_test.py "$@"

TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================="
    echo "All tests PASSED! ✅"
    echo -e "==========================================${NC}"
else
    echo ""
    echo -e "${RED}=========================================="
    echo "Some tests FAILED! ❌"
    echo -e "==========================================${NC}"
    echo ""
    echo "To debug:"
    echo "  - Check delist logs: docker-compose logs delist"
    echo "  - Check database: docker exec -it noshirt-postgres psql -U postgres -d noshirt"
    echo "  - Run with --no-cleanup to inspect data after tests"
fi

exit $TEST_RESULT
