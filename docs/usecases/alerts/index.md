# Alert Management

## Use Case Summary
Manage, triage, and bulk update Recorded Future alerts (Classic & Playbook) directly from the terminal to accelerate Security Operations Center (SOC) response and investigation workflows.

## Issue
Switching to the UI for every alert delays investigation, resulting in analyst fatigue and inconsistent alert handling. Manual triage processes slow down incident response and create bottlenecks in security operations workflows.

## Solution
Retrieve and manage Recorded Future alerts directly from the terminal using [`banshee ca`](../../reference/commands/#banshee-ca) and [`banshee pba`](../../reference/commands/#banshee-pba) commands. 

- For Classic Alerts, use [`banshee ca search`](../../reference/commands/#banshee-ca-search) with time filters and [`banshee ca update`](../../reference/commands/#banshee-ca-update) for bulk status changes, note additions, and assignee updates. 

- For Playbook Alerts, leverage [`banshee pba search`](../../reference/commands/#banshee-pba-search) with category and priority filters, then use [`banshee pba update`](../../reference/commands/#banshee-pba-update) to modify status, add comments, assign users, and set reopen strategies. 


This approach speeds up triage, maintains alert consistency, and enables analysts to update multiple alerts simultaneously through bulk operations.