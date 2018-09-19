
import neovim
import codechef_cli


@neovim.plugin
class Codechef:
    contest = None

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.function('SelectContest')
    def select_contest(self, args):
        # TODO: status should be argument
        contests = codechef_cli.api.get_data('contests', params={
            'fields': 'code, name, startDate, endDate',
            'limit': 50,
            'status': 'past'
        })['contestList']
        contests = [contest['code'] + ' - ' + contest['name']
                    for contest in contests]
        self.nvim.call("fzf#run", {'source': contests,
                                   'sink': 'ContestPage',
                                   'down': '30%'})

    @neovim.command('ContestPage', range='', nargs='*', sync=True)
    def contest_page(self, args, range):
        contest_code = str(args[0].split('-')[0].strip())

        self.contest = codechef_cli.api.get_contest(contest_code)

        self.nvim.funcs.execute('vsplit')
        self.nvim.funcs.execute('e /tmp/codechef_vim' +
                                self.contest.contest_code)
        self.nvim.current.line = str(self.contest.problem_codes)
        self.nvim.funcs.execute('w')
