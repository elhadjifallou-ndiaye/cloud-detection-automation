# Playbook: Incident Automation (Azure Sentinel)

**Objective:** Automate alert enrichment and notification when a new Sentinel incident is triggered.

### Trigger:
- When an Azure Sentinel alert is triggered.

### Actions:
1. Parse JSON alert payload.
2. Notify security team via Microsoft Teams (summary and severity).
3. Upload the alert body to Azure Blob Storage for evidence.
4. (Optional) Create ServiceNow or Jira ticket.

### Security Notes:
- Connections secured via Azure Key Vault.
- No destructive actions.
- Suitable for demonstration or lab use.
