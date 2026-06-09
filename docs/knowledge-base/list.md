# list

> See [index.md](index.md) for authentication, readiness checks, output conventions, and shared LLM notes.

### `banshee list create NAME [LIST_TYPE]`

Create a new list.

| Argument/Option | Default | Description |
|-----------------|---------|-------------|
| `NAME` (required) | | Name of the list |
| `LIST_TYPE` | `entity` | One of: `entity`, `source`, `text` |
| `--pretty` / `-p` | | Pretty print |

```bash
banshee list create coolbeans
banshee list create coolsources source -p
```

---

### `banshee list search [NAME]`

Search for lists by name and/or type.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `NAME` (optional) | | | Filter by list name |
| `--list-type` | `-t` | | One of: `entity`, `source`, `text`, `custom`, `ip`, `domain`, `tech_stack`, `industry`, `brand`, `partner`, `industry_peer`, `location`, `supplier`, `vulnerability`, `company`, `hash`, `operation`, `attacker`, `target`, `method`, `executive` |
| `--limit INTEGER` | `-l` | `1000` | Max results (1–3000) |
| `--pretty` | `-p` | | Pretty print |

```bash
banshee list search -l 1500 -p
banshee list search -t vulnerability
banshee list search Attacker
banshee list search ernest -t entity -p -l 3
```

**Response shape:** Returns a flat JSON array. Each item has:

| Field | Description |
|-------|-------------|
| `.id` | List ID (e.g. `report:-19oM7`) |
| `.name` | List name |
| `.type` | List type: `entity`, `source`, `text`, etc. |
| `.created` | Creation timestamp (ISO 8601) |
| `.updated` | Last updated timestamp (ISO 8601) |
| `.owner_id` | Owner uhash ID |
| `.owner_name` | Owner display name |
| `.owner_organisation_details` | Organisation ownership info |

---

### `banshee list info LIST_ID`

Get metadata about a list.

```bash
banshee list info 1b0tFN
banshee list info 1b0tFN -p
```

**Response shape:** Returns a single JSON object — same field set as items in `list search`: `id`, `name`, `type`, `created`, `updated`, `owner_id`, `owner_name`, `organisation_id`, `organisation_name`, `owner_organisation_details`.

---

### `banshee list status LIST_ID`

Get processing/sync status of a list.

```bash
banshee list status 1b0tFN
```

**Response shape:** Returns a single JSON object with two fields:

| Field | Description |
|-------|-------------|
| `.status` | Processing status string (e.g. `"ready"`) |
| `.size` | Number of entities currently on the list |

---

### `banshee list entities LIST_ID`

Retrieve all entities currently on a list.

```bash
banshee list entities 1b0s1q
```

**Response shape:** Returns a flat JSON array. Each item has:

| Field | Description |
|-------|-------------|
| `.entity.id` | RF entity ID |
| `.entity.name` | Entity display name |
| `.entity.type` | Entity type string |
| `.status` | Entity status on the list (e.g. `"ready"`) |
| `.added` | Timestamp when entity was added (ISO 8601) |

```bash
# Extract all entity IDs on a list
banshee list entities report:6P8708 | jq -r '.[].entity.id'

# Get entity names and types
banshee list entities report:6P8708 | jq '[.[] | {name: .entity.name, type: .entity.type}]'
```

---

### `banshee list entries LIST_ID`

Retrieve text match entries on a list (for `text`-type lists).

```bash
banshee list entries 1b0s1q
```

---

### `banshee list add LIST_ID ENTITY_ID [PROPERTIES]`

Add a single entity to a list.

| Argument | Description |
|----------|-------------|
| `LIST_ID` (required) | List ID |
| `ENTITY_ID` (required) | RF entity ID (e.g. `SoA6SP`) OR `name,type` pair (e.g. `wannacry,malware`) |
| `PROPERTIES` (optional) | Use `annotation=<text>` to attach a note that appears on the Recorded Future platform for this entity. Quote the value if it contains spaces. |

```bash
banshee list add 1b0s1q lYNvCK
banshee list add 1b0s1q lYNvCK 'annotation=C2 server seen during incident X-1234'
```

---

### `banshee list bulk-add LIST_ID [ENTITY_INPUT]...`

Add multiple entities to a list. Accepts entity IDs, `name,type` pairs, or `type:value` pairs.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | off | Overwrite mode: keep entities present in the supplied input, add new ones, and remove any entities currently on the list that are **not** in the input. Without it, the command only appends new entities and never removes existing ones. |

**Input formats:**
- RF entity ID: `SoA6SP`
- Name + type: `wannacry,malware` or `www.duckdns.org,InternetDomainName`
- Type-prefixed value: `ip:8.8.8.8`

```bash
banshee list bulk-add report:21YKUC SoA6SP lYNvCK
banshee list bulk-add 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# Overwrite mode: make the list match exactly the entities supplied (adds missing, removes stale)
banshee list bulk-add 21YKUC SoA6SP lYNvCK --overwrite

# From file (one entity per line)
banshee list bulk-add 21YKUC < entities.txt
cat entities.txt | banshee list bulk-add 21YKUC
```

**Response:** Plain text grouped by outcome — `ADDED:`, `REMOVED:` (overwrite only), and `UNCHANGED:` blocks listing the affected entities. Not JSON; do not pipe to `jq`.

---

### `banshee list remove LIST_ID ENTITY_ID`

Remove a single entity from a list.

```bash
banshee list remove 1b0s1q lYNvCK
```

---

### `banshee list bulk-remove LIST_ID [ENTITY_INPUT]...`

Remove multiple entities from a list. Same input formats as `bulk-add`.

```bash
banshee list bulk-remove 21YKUC JLHNoH lYNvCK
banshee list bulk-remove 21YKUC ip:8.8.8.8 www.duckdns.org,InternetDomainName

# From file
banshee list bulk-remove 21YKUC < entities.txt
cat entities.txt | banshee list bulk-remove 21YKUC
```

---

### `banshee list copy SOURCE_LIST_ID DESTINATION_LIST_ID`

Copy the entities from one list to another. The source list's entities are read and added to the destination.

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--overwrite` | `-o` | off | Overwrite mode: keep entities present in both lists, add new ones, and remove any entities on the destination that are **not** in the source. Without it, entities are only appended to the destination and nothing is removed. |

If the source list is empty the command exits without modifying the destination, even with `--overwrite`.

```bash
banshee list copy 1b0s1q 21YKUC

# Make the destination mirror the source exactly (adds missing, removes stale)
banshee list copy 1b0s1q 21YKUC --overwrite
```

**Response:** Plain text grouped by outcome — `ADDED:`, `REMOVED:` (overwrite only), and `UNCHANGED:` blocks listing the affected entities. Not JSON; do not pipe to `jq`.

---

### `banshee list clear LIST_ID`

Remove **all** entities from a list (destructive — use with care). Text-match entries cannot be removed via the API. The list itself is not deleted; only its entities are removed.

```bash
banshee list clear 1b0s1q
```

**Response:** Plain text. Prints `No entities to remove` when the list is already empty, `Successfully removed <N> entities` on success, or — if any removals fail — `<N> entities were not removed from the list:` followed by the still-present entities. Not JSON.
