from import_export import fields, resources


class GamesPlayedResource(resources.Resource):

    game = fields.Field(attribute='game__name', column_name='game')
    time = fields.Field(attribute='time', column_name='time (hours)')
    num_players = fields.Field(attribute='num_players', column_name='num_players')

    class Meta:
        export_order = ['game', 'time', 'num_players']
