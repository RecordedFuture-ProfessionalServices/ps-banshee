# Entity Matching

## Use Case Summary
Search and resolve Recorded Future Entities (Companies, Malware, Threat Actors, etc.) to ensure consistent referencing across Security Operations Center (SOC) tools and workflows.

For further information on Recorded Future entities click [here](https://support.recordedfuture.com/hc/en-us/articles/115001359567-What-is-an-Entity).

## Issue
Free-text names can cause mismatches between tools and Recorded Future. A Threat Actor entity can have the same name as a Username entity, but their entity IDs will be different, leading to confusion and incorrect threat intelligence associations.

## Solution
Search and resolve entities directly in PS Banshee using [`banshee entity`](../../reference/commands/#banshee-entity) commands. 

- Use [`banshee entity search`](../../reference/commands/#banshee-entity-search) when you have an entity name and/or type and need to find the corresponding entity ID. 

- Use [`banshee entity lookup`](../../reference/commands/#banshee-entity-lookup) when you have an entity ID and need to retrieve the name and type. 

Once you have the correct entity ID, utilize it in subsequent PS Banshee commands like [`banshee list add`](../../reference/commands/#banshee-list-add) to ensure accurate entity referencing in your organization's watchlists.