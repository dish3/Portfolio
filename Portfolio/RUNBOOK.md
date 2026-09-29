# Operational Runbook — NOVA AI Portfolio OS

This document details remediation procedures for production anomalies across Vercel, Render, Supabase, and external connectors.

---

## 1. Webhook Stops Firing (GitHub)
- **Symptom**: New commits or releases pushed to monitored repos do not generate cards in `/admin/pending`.
- **Diagnostics**:
  1. Check GitHub App settings: Verify webhook delivery logs under **App Settings > Advanced**.
  2. Verify FastAPI logs on Render for `POST /webhooks/github` 401/403 HMAC errors.
  3. Ensure `GITHUB_WEBHOOK_SECRET` in Render environment matches the secret in GitHub.
- **Remediation**:
  - If a webhook was dropped, trigger the scheduled fallback manually via:
    `POST https://api.portfolio.os/internal/poll/github` with header `X-Internal-Secret: <INTERNAL_POLL_SECRET>`.

---

## 2. Platform Connector Starts Erroring (LeetCode)
- **Symptom**: `POST /internal/poll/leetcode` returns 500 or fails to capture stats.
- **Diagnostics**:
  1. LeetCode's public GraphQL schema is unofficial and may change field names.
  2. Inspect connector error logs in Render console.
- **Remediation**:
  - Update `LeetCodeConnector` query payload in `apps/api/app/connectors/` to align with the new schema.
  - Test locally with recorded mock responses before deploying.

---

## 3. Gemini Quota Limit Hit
- **Symptom**: Agent logs show `ResourceExhausted` (HTTP 429).
- **Diagnostics**:
  - Review Google AI Studio token quota dashboard.
- **Remediation**:
  - Verify that high-volume classification tasks are routed to `gemini-2.5-flash-lite` instead of heavier models.
  - Ingestion tasks will automatically back off; queue remains intact in database without loss of state.

---

## 4. Render Free Tier Cold Start Latency
- **Symptom**: First visitor chat request takes 50–70 seconds.
- **Expected Behavior**: Free tier instances spin down after 15 minutes of inactivity.
- **Mitigation**:
  - Public portfolio pages are served from Vercel edge cache (ISR) and do NOT wait for Render.
  - The chatbot UI explicitly displays a "Waking up server..." status message during cold starts.
  - Optional: Set up a free UptimeRobot monitor pinging `/health` every 10 minutes.

---

## 5. Rollback of an Incorrectly Approved Change
- **Procedure**:
  1. In the database or admin console, locate the `pending_changes` record for the item.
  2. Update the target entity (`projects`, `certificates`, etc.) status to `'archived'` or delete the record.
  3. Trigger Next.js on-demand ISR revalidation:
     `POST https://portfolio.os/api/revalidate?secret=<REVALIDATION_SECRET>&path=/projects/<slug>`.
  4. Vector embeddings for the removed entity will automatically dereference on next knowledge graph sync.
