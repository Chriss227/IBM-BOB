# 🚀 Deployment Runbook

## Bob Onboarding Accelerator - Production Deployment Guide

**Version:** 1.0.0  
**Last Updated:** 2026-05-17  
**Owner:** DevOps Team

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deployment Steps](#deployment-steps)
3. [Post-Deployment Validation](#post-deployment-validation)
4. [Rollback Procedure](#rollback-procedure)
5. [Troubleshooting](#troubleshooting)
6. [Emergency Contacts](#emergency-contacts)

---

## Pre-Deployment Checklist

### Code Readiness
- [ ] All tests passing (backend + frontend)
- [ ] Code review approved by 2+ reviewers
- [ ] Security scan clean (Bandit, Safety)
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Version tagged in Git

### Infrastructure Readiness
- [ ] Staging environment validated
- [ ] Production environment provisioned
- [ ] DNS configured correctly
- [ ] SSL certificates valid (>30 days remaining)
- [ ] Secrets stored in secrets manager
- [ ] Monitoring and alerting configured
- [ ] Rollback procedure tested

### Team Readiness
- [ ] On-call engineer assigned
- [ ] Stakeholders notified (24h advance notice)
- [ ] Deployment window scheduled
- [ ] Runbook reviewed by team

---

## Deployment Steps

### Step 1: Pre-Deployment Verification

```bash
# Verify current production status
kubectl get pods -n production
kubectl get deployments -n production

# Check current version
kubectl describe deployment bob-onboarding-backend -n production | grep Image

# Verify health
curl https://api.bob-onboarding.com/health
```

### Step 2: Build and Tag Docker Image

```bash
# Build Docker image
docker build -t bob-onboarding:v1.2.0 .

# Tag for registry
docker tag bob-onboarding:v1.2.0 your-registry/bob-onboarding:v1.2.0
docker tag bob-onboarding:v1.2.0 your-registry/bob-onboarding:latest

# Push to registry
docker push your-registry/bob-onboarding:v1.2.0
docker push your-registry/bob-onboarding:latest
```

### Step 3: Deploy to Production (Blue-Green)

```bash
# Update deployment with new image
kubectl set image deployment/bob-onboarding-backend \
  backend=your-registry/bob-onboarding:v1.2.0 \
  -n production

# Watch rollout status
kubectl rollout status deployment/bob-onboarding-backend -n production

# Verify new pods are running
kubectl get pods -n production -l app=bob-onboarding
```

### Step 4: Gradual Traffic Migration

```bash
# Start with 10% traffic to new version
kubectl patch service bob-onboarding-backend -n production \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor for 5 minutes
# Check error rates, response times, logs

# If stable, increase to 25%, then 50%, then 100%
# Monitor at each step
```

### Step 5: Run Smoke Tests

```bash
# Run automated smoke tests
./scripts/smoke-test.sh https://api.bob-onboarding.com

# Manual verification
curl https://api.bob-onboarding.com/health
```

---

## Post-Deployment Validation

### Automated Checks

```bash
# Health check
curl https://api.bob-onboarding.com/health

# Test analyze endpoint
curl -X POST https://api.bob-onboarding.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/octocat/Hello-World"}'
```

### Manual Verification

1. **Frontend Access**
   - Navigate to https://bob-onboarding.com
   - Verify page loads correctly
   - Test repository analysis flow

2. **Backend API**
   - Check `/health` endpoint returns 200
   - Verify `/analyze` endpoint works
   - Check response times (P95 < 60s)

3. **Monitoring**
   - Check Grafana dashboards
   - Verify metrics are being collected
   - Confirm no error spikes

4. **Logs**
   ```bash
   # Check application logs
   kubectl logs -f deployment/bob-onboarding-backend -n production
   
   # Check for errors
   kubectl logs deployment/bob-onboarding-backend -n production | grep ERROR
   ```

### Success Criteria

- ✅ Health check returns 200
- ✅ Error rate < 1%
- ✅ Response time P95 < 60s
- ✅ No 5xx errors
- ✅ All pods healthy
- ✅ Smoke tests pass

---

## Rollback Procedure

### Automated Rollback (Triggered by Alerts)

Rollback triggers:
- Error rate > 5% for 5 minutes
- Response time P95 > 5s for 5 minutes
- Health check failures > 50%

### Manual Rollback

```bash
# Immediate rollback to previous version
kubectl rollout undo deployment/bob-onboarding-backend -n production

# Verify rollback
kubectl rollout status deployment/bob-onboarding-backend -n production

# Check pods are running
kubectl get pods -n production -l app=bob-onboarding

# Run smoke tests
./scripts/smoke-test.sh https://api.bob-onboarding.com
```

### Rollback to Specific Version

```bash
# View rollout history
kubectl rollout history deployment/bob-onboarding-backend -n production

# Rollback to specific revision
kubectl rollout undo deployment/bob-onboarding-backend \
  --to-revision=3 -n production
```

### Post-Rollback Actions

1. Notify stakeholders
2. Create incident report
3. Analyze logs and metrics
4. Identify root cause
5. Create fix plan
6. Schedule retry

---

## Troubleshooting

### Issue: Pods Not Starting

```bash
# Check pod status
kubectl get pods -n production

# Describe pod for events
kubectl describe pod <pod-name> -n production

# Check logs
kubectl logs <pod-name> -n production

# Common causes:
# - Image pull errors
# - Resource limits
# - Configuration errors
# - Health check failures
```

### Issue: High Error Rate

```bash
# Check application logs
kubectl logs deployment/bob-onboarding-backend -n production | grep ERROR

# Check Bob API connectivity
kubectl exec -it <pod-name> -n production -- \
  curl -v $BOB_API_ENDPOINT

# Verify environment variables
kubectl exec -it <pod-name> -n production -- env | grep BOB
```

### Issue: Slow Response Times

```bash
# Check resource usage
kubectl top pods -n production

# Check HPA status
kubectl get hpa -n production

# Scale manually if needed
kubectl scale deployment bob-onboarding-backend --replicas=5 -n production
```

### Issue: Database/External Service Issues

```bash
# Check Bob API status
curl -v $BOB_API_ENDPOINT

# Check network connectivity
kubectl exec -it <pod-name> -n production -- \
  ping api.ibm.com

# Verify secrets
kubectl get secret bob-secrets -n production -o yaml
```

---

## Emergency Contacts

### On-Call Rotation
- **Primary:** DevOps Engineer (Slack: @devops-oncall)
- **Secondary:** Backend Lead (Slack: @backend-lead)
- **Escalation:** Engineering Manager (Slack: @eng-manager)

### External Contacts
- **IBM Bob Support:** support@ibm.com
- **Cloud Provider:** support@cloudprovider.com

### Communication Channels
- **Incidents:** #incidents (Slack)
- **Deployments:** #deployments (Slack)
- **Status Page:** https://status.bob-onboarding.com

---

## Deployment Timeline

| Time | Action | Duration |
|------|--------|----------|
| T-24h | Notify stakeholders | - |
| T-1h | Pre-deployment checks | 15 min |
| T-0 | Start deployment | - |
| T+5min | Deploy to production | 5 min |
| T+10min | Run smoke tests | 5 min |
| T+15min | Monitor metrics | 10 min |
| T+30min | Gradual traffic migration | 15 min |
| T+45min | Full traffic cutover | - |
| T+1h | Post-deployment validation | 15 min |
| T+24h | Remove old deployment | - |

---

## Monitoring Dashboards

- **Grafana:** https://grafana.bob-onboarding.com
- **Logs:** https://logs.bob-onboarding.com
- **Metrics:** https://metrics.bob-onboarding.com
- **Alerts:** https://alerts.bob-onboarding.com

---

## Notes

- Always deploy during low-traffic hours (2-4 AM UTC)
- Keep deployment window to < 1 hour
- Have rollback plan ready before starting
- Document any deviations from this runbook
- Update runbook after each deployment

---

**Last Deployment:** TBD  
**Next Scheduled Deployment:** TBD  
**Deployment Frequency:** Weekly (Thursdays 2 AM UTC)