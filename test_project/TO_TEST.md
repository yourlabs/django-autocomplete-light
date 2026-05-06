# dal_alight — Features to Test

## Done
- [x] **alight_foreign_key** — Basic FK single-select, search, create (inline + popup), save, inline
- [x] **alight_one_to_one** — Same as FK; self-ref and already-linked items shown (matches select2 behaviour)
- [x] **alight_many_to_many** — Multi-select chips, remove with ×, save/reload, inline
- [x] **alight_list** — Dynamic list from DB (fused with select2_list_tmodel); create new entry; save; for_inline selector present
- [x] **alight_linked_data** — Forwarding works; owner filters test dropdown correctly
- [x] **alight_forward_different_fields** — Forwarded dict visible in dropdown; all field types (checkbox, select, radio, multiselect, JS handlers, Self) arrive correctly; select-a-valid-choice on submit is expected (no choice_list set, diagnostic app)

## Remaining

- [x] **alight_rename_forward** — Forward with a renamed destination key (forwarding works; text search intentionally unfiltered — diagnostic app)

- [x] **alight_secure_data** — Filters by owner; anonymous returns empty; save_model auto-assigns owner on create

- [x] **alight_generic_foreign_key** — Both GFK fields work; grouping, filtering, save/reload all good

- [x] **alight_djhacker_formfield** — Main form gets alight widget via djhacker without any form= declaration; inline plain select is parity with select2

- [x] **alight_nestedadmin** — Forwarding across nested inline levels works; fixed prefix-aware field lookup in dal-django.js

- [x] **alight_taggit** — Tag selection, multiple tags, save/reload all work

- [x] **alight_outside_admin** — Widget renders and functions correctly outside Django admin

- [x] **alight_tag** — Free-text tag autocomplete, create new tags, saves as comma-separated string
