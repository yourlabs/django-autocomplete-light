# dal_alight — Features to Test

## Done
- [x] **alight_foreign_key** — Basic FK single-select, search, create (inline + popup), save, inline
- [x] **alight_one_to_one** — Same as FK; self-ref and already-linked items shown (matches select2 behaviour)
- [x] **alight_many_to_many** — Multi-select chips, remove with ×, save/reload, inline

## Remaining

- [x] **alight_list** — Dynamic list from DB (fused with select2_list_tmodel); create new entry; save; for_inline selector present

- [x] **alight_linked_data** — Forwarding works; owner filters test dropdown correctly

- [ ] **alight_forward_different_fields** — Forward a value from a non-FK field to the autocomplete view
  - URL: /admin/alight_forward_different_fields/tmodel/

- [ ] **alight_rename_forward** — Forward with a renamed destination key
  - URL: /admin/alight_rename_forward/tmodel/

- [ ] **alight_secure_data** — Autocomplete requires login; anonymous access returns no results or 403
  - URL: /admin/alight_secure_data/tmodel/
  - Check: autocomplete URL rejects unauthenticated requests

- [ ] **alight_generic_foreign_key** — GenericForeignKey: content-type selector + object picker
  - URL: /admin/alight_generic_foreign_key/tmodel/
  - Check: both GFK fields (test and test2) work independently

- [ ] **alight_djhacker_formfield** — Widget overridden via djhacker (not declared in the form)
  - URL: /admin/alight_djhacker_formfield/tmodel/

- [ ] **alight_nestedadmin** — Three levels of nested inlines, each with autocomplete
  - URL: /admin/alight_nestedadmin/tmodelone/
  - Check: autocomplete works in deeply nested inline rows

- [ ] **alight_taggit** — django-taggit tag field via autocomplete
  - URL: /admin/alight_taggit/tmodel/
  - Check: type a tag, select or create it; multiple tags; save and reload

- [ ] **alight_outside_admin** — Widget used on a non-admin page
  - URL: /alight_outside_admin/ (or similar)
  - Check: widget renders and functions outside Django admin context

- [ ] **alight_tag** — Free-text tag field (comma-separated, no model backing)
  - URL: /admin/alight_tag/tmodel/
  - Check: type tags, create new ones, save as comma-separated string
