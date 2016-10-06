from import_export import fields, resources


class GamesPlayedResource(resources.Resource):

    game = fields.Field(attribute='game__name', column_name='game')
    time = fields.Field(attribute='time', column_name='time (hours)')
    num_players = fields.Field(attribute='num_players', column_name='num_players')

    class Meta:
        export_order = ['game', 'time', 'num_players']

    def dehydrate_game(self, obj):
        return obj['game__name']

    def dehydrate_time(self, obj):
        return obj['time'].total_seconds() / 3600

    def dehydrate_num_players(self, obj):
        return obj['num_players']
