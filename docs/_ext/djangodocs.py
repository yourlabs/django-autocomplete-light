def setup(app):
    app.add_crossref_type(
        directivename = "setting",
        rolename = "setting",
        indextemplate = "pair: %s; setting",
    )
    app.add_crossref_type(
        directivename = "ref",
        rolename = "ref",
        indextemplate = "pair: %s; ref",
    )
    app.add_crossref_type(
        directivename = "doc",
        rolename = "doc",
        indextemplate = "pair: %s; doc",
    )
    app.add_crossref_type(
        directivename = "label",
        rolename = "label",
        indextemplate = "pair: %s; label",
    )
