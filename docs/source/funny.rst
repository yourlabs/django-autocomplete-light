Doing funny things
==================

My client wanted me to do funny things, so that's the reason I needed an
autocomplete app that's simple enought to stay out of my way. You could replace
the term 'funny' by 'painful'.

Let's review some of the funny things you could do.

Overriding autocomplete or deck options
---------------------------------------

Behind the scenes, deck.js initializes a deck for each autocomplete widget, and
the autocomplete for the text input in that widget. Default options are passed.

In the default result template, autocomplete_light/result.html, you can see
that the result tag has a special attribute, *data-value*::

    <li class="result" data-value="{{ result.pk }}">

Which works well because the default getValue callback for the deck is::

    'getValue': function(deck, result) {
        return result.data('value');
    },

Let's say that it gets in your way, that it's not what you want. That you want
to implement your own getValue callback because you want to satisfy your funny
client.

Remember when you've read that that deck.js initializes a deck for all autocomplete widgets ? Well that's not completely true.

In deck.js, you can see how it's bootstrapped with no custom options::

    $('.autocompleteselectwidget_light[data-bootstrap=normal]').each(function() {
        $(this).yourlabs_deck();
    });

Note that it only bootstraps widgets with data-bootstrap=normal. So, suppose
that your channel class has a bootstrap attribute as such::

    class FunnyChannel(ChannelBase):
        bootstrap = 'funny'

Then, deck.js will not initialize the deck and autocomplete for widgets using
this channel. Which means that you could safely initialize the deck with the
options you want::

    $(document).ready(function() {
        $('.autocompleteselectwidget_light[data-bootstrap=funny]').each(function() {
            $(this).yourlabs_deck({
                getValue: function(deck, result) {
                    // find funny ways to return the value (object pk in most cases)
                    return ...;
                },
                autocompleteOptions: {
                    defaultValue: 'Welcome to the funny autocomplete',
                },
            });
        });
    });

Funny example: results with no pk
---------------------------------

So, I had a very funny requirement: propose results in the autocomplete that
are in a remote database, and import them as needed.

For example, websiteInsane has the following authors:

- Hunter S. Thompson
- Daniel Montbars

And websiteHumanist has authors:

- Giovanni Pico della Mirandola
- Dante Alighieri

Well in both websites, the autocomplete should propose all 4 authors. So
websiteHumanist should propose two results which don't have a pk in its
database and vice-versa.

That's what RemoteChannel looks like::

    class RemoteChannel(autocomplete_light.JSONChannelBase):
        bootstrap = 'remote'

        def get_results(self, pks=None):
            # get the local results ...
            results = super(RemoteChannel, self).get_results(pks)

            if pks is None:
                # if pks was something, then it would mean that this function is called
                # by are_valid() rather than render_autocomplete

                results += self.get_remote_results()
            return results

        def get_remote_results(self):
            # use some api to return results
            results = self.fetch_results()

            # don't forget to clear the pk of the remote models as they don't
            # exist in the local database !!
            for result in results:
                result._remote_pk = result.pk
                result.pk = None

            return results

        def result_as_dict(self, result):
            remote_pk = getattr(result, '_remote_pk', None)

            if not remote_pk:
                # result is local, it has a pk here
                return super(RemoteChannel, self).result_as_dict(result)

            # result comes from elsewhere, we need a url from our site, that is
            # able to import it from the other site, and respond with the local
            # pk
            url = 'someurl' + '?' + urllib.urlencode({'pk': remote_pk})

            return {
                'import_url': url # local import url
            }

That's what the view of the import url looks like::

    class ApiView(generic.View):
        def post(self, request, *args, **kwargs):
            # some security checks here ...
            
            # get the model class from the url
            self.model_class = get_model(kwargs['app_label'],
                kwargs['module_name'])

            # make the remote url
            url = '/api/%s/%s/%s/?format=json' % (
                kwargs['app_label'],
                kwargs['module_name'],
                request.GET['pk'],
            )
            url = 'http://' + settings.DATA_MASTER + url

            obj = self.fetch(url)

            return http.HttpResponse(obj.pk)

        def fetch(self, url):
            # in case you're wondering, we're talking with djangorestframework here
            app_name = url.split('/')[-4]
            model_name = url.split('/')[-3]
            model_class = get_model(app_name, model_name)

            fh = urllib.urlopen(url)
            data = simplejson.loads(fh.read())
            fh.close()

            for key, value in data.items():
                if isinstance(value, str) and settings.DATA_MASTER in value:
                    data[key] = self.fetch(value)
            model, created = model_class.objects.get_or_create(**data)
            return model

And (a lot of fun later), that's what it's bootstrapping javascript code looks like::

    $(document).ready(function() {
        $('.autocompleteselectwidget_light[data-bootstrap=remote]').each(function() {
            $(this).yourlabs_deck({
                'getValue': function(deck, result) {
                    // autocomplete_light/result_with_json.html stacks the json
                    // in a hidden textarea by default, let's parse it
                    data = $.parseJSON(result.find('textarea').html());
                    
                    // in the case of a local result, we already have a value
                    if (data.value) {
                        return data.value;
                    }   
                    
                    // otherwise, we have an url that will import the model and return
                    // the local pk
                    if (data.import_url) {
                        var value = false;
                        $.ajax(data.import_url, {
                            async: false, // important to block everything
                            type: 'post',
                            success: function(text, jqXHR, textStatus) {
                                value = text;
                            },  
                        }); 
                        return value;
                    }   
                }   
            }); 
        }); 
    }); 

Think of it as you want, it's far from as buggy and ugly as it was when I had
ajax_selects all monkey patched to achieve the same result, in an horrible way.

I hope you like it, and if you do: please read the code.

When things go wrong
--------------------

If you don't know how to debug, you should learn to use:

Firebug javascript debugger
    Open the script tab, select a script, click on the left of the code to
    place a breakpoint

Ipdb python debugger
    Install ipdb with pip, and place in your python code: import ipdb; ipdb.set_trace()

If you are able to do that, then you are a professional, enjoy autocomplete_light !!!
