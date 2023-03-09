from ._builtin import Page, WaitPage


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        if self.session.config['assign_groups']:
            Klee_group = []
            Kandinsky_group = []
            send_home = []
            for player in self.subsession.get_players():
                # print(player.participant.vars)
                if player.participant.vars['artist'] == 'Klee':
                    player.assigned_group = True
                    player.Klee = True
                elif player.participant.vars['artist'] == 'Kandinsky':
                    player.assigned_group = True
                    player.Klee = False
                else:
                    player.assigned_group = False

                if player.assigned_group:
                    if player.Klee:
                        Klee_group.append(player)
                    else:
                        Kandinsky_group.append(player)
                else:
                    send_home.append(player)

            self.subsession.set_group_matrix([Klee_group, Kandinsky_group])


class Revelation(Page):
    def vars_for_template(self):
        purchase_list = []
        for player in self.group.get_players():
            purchase_list.append(player.participant.vars['item_purchased'])

        item_purchased = self.player.participant.vars['item_purchased']
        return {
            'artist': self.participant.vars['artist'],
            'assign_groups': self.session.config['assign_groups'],
            'own_group': "Klee" if self.player.Klee else "Kandinsky",
            'purchase_list': purchase_list,
            'made_purchase': item_purchased is not None,
            'own_purchase': item_purchased,
            'object_group': "Klee" if item_purchased == "Mug A" else "Kandinsky",
        }


class Results(Page):
    pass


page_sequence = [
    ResultsWaitPage,
    Revelation,
    # Results
]
