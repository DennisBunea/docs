from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


def setup(app):
    app.add_node(cardCollection_node, html=(visit_card_node, depart_card_node))
    app.add_directive('card_collection', CardCollectionDirective)
    return {'version': '0.1'}  # identifies the version of our extension


class cardCollection_node(nodes.Structural, nodes.Element):
    pass


def visit_card_node(self, node):
    pass


def depart_card_node(self, node):
    pass


class CardCollectionDirective(Directive):
    # defines the parameter the directive expects
    # directives.unchanged means you get the raw value from RST
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'bgcolor': directives.unchanged,
        'name': directives.unchanged,
        'title': directives.unchanged,
        'class': directives.unchanged,
        'subtitle': directives.unchanged,
        'subtitle_link': directives.unchanged,
    }
    has_content = True
    add_index = True

    def run(self):
        sett = self.state.document.settings
        language_code = sett.language_code
        env = self.state.document.settings.env

        # gives you access to the parameter stored
        # in the main configuration file (conf.py)
        config = env.config

        # gives you access to the options of the directive
        options = self.options

        # we create the content of the blog post
        # because it contains any kind of RST
        # we parse parse it with function nested_parse
        par = nodes.paragraph()
        self.state.nested_parse(self.content, self.content_offset, par)

        bgcolor = 'white'
        if 'bgcolor' in options:
            bgcolor = options['bgcolor']

        # we create a card and we add the section
        rowContainer = nodes.container()
        rowContainer['classes'].append('{0}-container-fluid row-center'.format(bgcolor))

        if 'class' in options:
            rowContainer['classes'].append(options['class'])

        bootstrapContainer = nodes.container()
        bootstrapContainer['classes'].append('bs-container')

        if 'title' in options:
            bootstrapContainer += nodes.raw(text='<h2 style="margin-bottom:5px;">{0}</h2>'.format(options['title']),
                                            format='html')
            if 'subtitle' in options:
                if 'subtitle_link' in options:
                    bootstrapContainer += nodes.raw(
                        text='<p><a href="{0}" class="text-muted" style="text-decoration:none;">{1}</a><br /></p>'.format(
                            options['subtitle_link'], options['subtitle']), format='html')
                else:
                    bootstrapContainer += nodes.raw(
                        text='<p class="text-muted">{0}<br /></p>'.format(options['subtitle']), format='html')
            else:
                bootstrapContainer += nodes.raw(text='<br />', format='html')

        cardCollectionContainer = nodes.container(ids=[options['name']])
        cardCollectionContainer['classes'].append('vh-card-group')

        cardCollectionContainer += par
        bootstrapContainer += cardCollectionContainer

        rowContainer += bootstrapContainer

        # we return the result
        return [rowContainer]
