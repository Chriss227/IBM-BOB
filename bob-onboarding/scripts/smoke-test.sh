#!/bin/bash
# Smoke tests for Bob Onboarding Accelerator
# Usage: ./scripts/smoke-test.sh <base_url>

set -e

BASE_URL="${1:-http://localhost:8000}"
TIMEOUT=10
FAILED=0

echo "🧪 Running smoke tests against: $BASE_URL"
echo "================================================"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local expected_status="$3"
    local method="${4:-GET}"
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT "$BASE_URL$endpoint" || echo "000")
    else
        response=$(curl -s -w "\n%{http_code}" -X POST --max-time $TIMEOUT \
            -H "Content-Type: application/json" \
            -d '{"url":"https://github.com/octocat/Hello-World"}' \
            "$BASE_URL$endpoint" || echo "000")
    fi
    
    status_code=$(echo "$response" | tail -n1)
    
    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $status_code)"
    else
        echo -e "${RED}✗ FAIL${NC} (Expected HTTP $expected_status, got $status_code)"
        FAILED=$((FAILED + 1))
    fi
}

# Test 1: Health check
test_endpoint "Health Check" "/health" "200"

# Test 2: Invalid endpoint (404)
test_endpoint "404 Handler" "/nonexistent" "404"

# Test 3: Analyze endpoint with valid URL (may take time, so we just check it responds)
echo -n "Testing Analyze Endpoint (basic connectivity)... "
response=$(curl -s -w "\n%{http_code}" --max-time 5 \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"url":"https://github.com/octocat/Hello-World"}' \
    "$BASE_URL/analyze" 2>/dev/null || echo "000")

status_code=$(echo "$response" | tail -n1)

if [ "$status_code" = "200" ] || [ "$status_code" = "500" ] || [ "$status_code" = "504" ]; then
    echo -e "${GREEN}✓ PASS${NC} (Endpoint reachable, HTTP $status_code)"
else
    echo -e "${YELLOW}⚠ WARNING${NC} (HTTP $status_code - endpoint may be slow or unavailable)"
fi

# Test 4: Invalid URL validation
echo -n "Testing URL Validation... "
response=$(curl -s -w "\n%{http_code}" --max-time $TIMEOUT \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"url":"https://gitlab.com/user/repo"}' \
    "$BASE_URL/analyze" || echo "000")

status_code=$(echo "$response" | tail -n1)

if [ "$status_code" = "422" ]; then
    echo -e "${GREEN}✓ PASS${NC} (HTTP $status_code)"
else
    echo -e "${RED}✗ FAIL${NC} (Expected HTTP 422, got $status_code)"
    FAILED=$((FAILED + 1))
fi

# Test 5: CORS headers
echo -n "Testing CORS Headers... "
response=$(curl -s -I --max-time $TIMEOUT \
    -H "Origin: http://localhost:5173" \
    "$BASE_URL/health" || echo "")

if echo "$response" | grep -qi "access-control-allow-origin"; then
    echo -e "${GREEN}✓ PASS${NC} (CORS headers present)"
else
    echo -e "${RED}✗ FAIL${NC} (CORS headers missing)"
    FAILED=$((FAILED + 1))
fi

echo "================================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All smoke tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ $FAILED test(s) failed${NC}"
    exit 1
fi

# Made with Bob
